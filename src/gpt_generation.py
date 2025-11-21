import json
import os
import argparse
import random
from pathlib import Path
from openai import OpenAI
from tqdm import tqdm
import copy
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

# Function to fetch completion
def fetch_completion(data_entry, model, client):
    test_case = data_entry["small_test_cases"]
    import time
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": f"Please complete Python code based on the task description and test cases. # Task description:\n{data_entry['markdown_description']}\n{test_case}\n#Solution:\n"},
                ],
                timeout=100,
            )
            data_entry["completion"] = response.choices[0].message.content
            return data_entry
        except Exception as e:
            error_str = str(e)
            error_type = type(e).__name__
            
            # Check for specific error types
            if "quota" in error_str.lower() or "insufficient_quota" in error_str.lower():
                print(f"\n❌ QUOTA ERROR: {error_str}")
                print("   This usually means:")
                print("   1. You've hit your usage limit (check https://platform.openai.com/usage)")
                print("   2. You're using a different API key than shown in dashboard")
                print("   3. Organization vs personal account mismatch")
                print("   4. Model-specific quota limit (e.g., GPT-4 has separate limits)")
                print(f"   Error details: {error_type}: {error_str}")
                data_entry["completion"] = f"Quota Error: {error_str[:100]}"
                return data_entry
            elif "rate_limit" in error_str.lower() or "429" in error_str:
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)
                    print(f"⚠️  Rate limit hit, retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"\n❌ RATE LIMIT ERROR after {max_retries} attempts: {error_str}")
                    data_entry["completion"] = f"Rate Limit Error: {error_str[:100]}"
                    return data_entry
            else:
                if attempt < max_retries - 1:
                    print(f"⚠️  Error (attempt {attempt + 1}/{max_retries}): {error_str[:100]}")
                    time.sleep(retry_delay)
                    continue
                else:
                    print(f"\n❌ API ERROR: {error_type}: {error_str}")
                    data_entry["completion"] = f"API Error: {error_str[:100]}"
                    return data_entry
    
    return data_entry


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate code completions using GPT models")
    parser.add_argument("--dataset", type=str, default="EffiBench", help="Dataset name (EffiBench, HumanEval, MBPP)")
    parser.add_argument("--model", type=str, default="gpt-4", help="Model name (e.g., gpt-4, gpt-4o)")
    parser.add_argument("--num_samples", type=int, default=0, help="Number of samples to process (0 = all samples)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for sampling")
    parser.add_argument("--no_shuffle", action="store_true", help="Use first N items instead of shuffling before sampling")
    parser.add_argument("--output_dir", type=str, default=".", help="Output directory for results")
    parser.add_argument("--profiler", type=str, default=None, help="Profiler tag for output filename (optional)")
    
    args = parser.parse_args()
    
    # Load dataset
    if args.dataset == "EffiBench":
        dataset_path = Path(__file__).parent.parent / "datasets" / "dataset.json"
        with open(dataset_path, "r") as f:
            dataset = json.load(f)
    elif args.dataset == "HumanEval":
        from datasets import load_dataset
        dataset = load_dataset("evalplus/humanevalplus", split="test")
        dataset = [dict(item) for item in dataset]
    elif args.dataset == "MBPP":
        from datasets import load_dataset
        dataset = load_dataset("evalplus/mbppplus", split="test")
        dataset = [dict(item) for item in dataset]
    else:
        raise ValueError(f"Unknown dataset: {args.dataset}")
    
    # Add dataset tag to each entry
    for entry in dataset:
        entry["dataset"] = args.dataset
    
    # Sample subset if requested
    if args.num_samples > 0 and len(dataset) > args.num_samples:
        if not args.no_shuffle:
            random.seed(args.seed)
            random.shuffle(dataset)
        dataset = dataset[:args.num_samples]
        print(f"Processing {len(dataset)} samples (sampled from total dataset)")
    else:
        print(f"Processing all {len(dataset)} samples")
    
    # Initialize OpenAI client
    api_key = os.getenv("OPENAI_API_KEY")
    api_base = os.getenv("OPENAI_API_BASE") if os.getenv("OPENAI_API_BASE") else None
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set!")
    
    # Show which API key is being used (first 10 chars for security)
    print(f"Using API key: {api_key[:10]}...{api_key[-4:]}")
    if api_base:
        print(f"Using API base URL: {api_base}")
    else:
        print("Using default OpenAI API (https://api.openai.com/v1)")
    
    client = OpenAI(
        api_key=api_key,
        base_url=api_base
    )
    
    # Process dataset
    model = args.model
    print(f"Using model: {model}")
    print("\n💡 Tip: If you get quota errors, check:")
    print("   1. https://platform.openai.com/usage - Your actual usage")
    print("   2. https://platform.openai.com/api-keys - Which key you're using")
    print("   3. Organization vs Personal account (check dropdown in top-right)")
    print()
    
    with ThreadPoolExecutor() as executor:
        future_to_entry = {executor.submit(fetch_completion, copy.deepcopy(entry), model, client): entry for entry in tqdm(dataset, desc="Submitting")}
        for future in tqdm(concurrent.futures.as_completed(future_to_entry), total=len(dataset), desc="Processing"):
            entry = future_to_entry[future]
            try:
                updated_entry = future.result()
                idx = dataset.index(entry)
                dataset[idx] = updated_entry
            except Exception as e:
                print(repr(e))
    
    # Prepare output filename
    model_name = model.replace("/", "_")
    profiler_suffix = f"_{args.profiler}" if args.profiler else ""
    output_filename = f"{args.dataset}_{model_name}{profiler_suffix}.json"
    
    # Create output directory if needed
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / output_filename
    
    # Save results
    with open(output_path, "w") as f:
        json.dump(dataset, f, indent=4)
    
    print(f"Results saved to: {output_path}")