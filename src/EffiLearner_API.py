#!/usr/bin/env python3
"""
EffiLearner using API-based models (Together AI, OpenAI, etc.)
This version doesn't require local GPU or large disk space.
"""

print("start")

import json
import os
from tqdm import tqdm
from openai import OpenAI
from code_efficiency_calculator import calculate_code_execution_efficiency
from datasets import load_dataset
import argparse
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import copy

batch_size = 8

def prompt_construction(task_description, test_case, completion, overhead_prompt):
    prompt = f"""
Optimize the efficiency of the following Python code based on the task, test case, and overhead analysis provided. Ensure the optimized code can pass the given test case.

Task Description:
{task_description}

Test Case:
{test_case}

Original Code:
```python
{completion}
```
Overhead Analysis:
{overhead_prompt}
Optimization Rules:
- Encapsulate the optimized code within a Python code block (i.e., ```python\n[Your Code Here]\n```).
- Do not include the test case within the code block.
- Focus solely on code optimization; test cases are already provided.
- Ensure the provided test case passes with your optimized solution.
"""
    return prompt


def fetch_completion(data_entry_lists, model, client):
    """Fetch completions using API (Together AI, OpenAI, etc.)"""
    results = []
    
    for data_entry in data_entry_lists:
        if "overhead" not in data_entry.keys():
            overhead = "The code execution failed."
        else:
            overhead = data_entry["overhead"]
        
        completion = data_entry["completion"]
        if data_entry["dataset"] == "EffiBench":
            test_case = data_entry["small_test_cases"]
            task_description = data_entry["markdown_description"]
        elif data_entry["dataset"] == "HumanEval":
            test_case = data_entry["open_test_cases"]
            task_description = data_entry["prompt"]
        elif data_entry["dataset"] == "MBPP":
            test_case = "\n".join(data_entry["test_list"])
            task_description = data_entry["prompt"]
        else:
            results.append(data_entry)
            continue
            
        prompt = prompt_construction(task_description, test_case, completion, overhead)
        
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a code optimization expert."},
                    {"role": "user", "content": prompt},
                ],
                timeout=100,
            )
            data_entry["tmp_completion"] = response.choices[0].message.content
        except Exception as e:
            print(f"API Error: {e}")
            data_entry["tmp_completion"] = "API Error"
        
        results.append(data_entry)
    
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True, 
                       help="Model name (e.g., 'meta-llama/Llama-3-8b-chat-hf' for Together AI, 'gpt-4o' for OpenAI)")
    parser.add_argument("--api_base", type=str, default=None,
                       help="API base URL (e.g., 'https://api.together.xyz/v1' for Together AI)")
    parser.add_argument("--api_key", type=str, default=None,
                       help="API key (or set TOGETHER_API_KEY or OPENAI_API_KEY env var)")
    parser.add_argument("--batch_size", type=int, default=8)
    parser.add_argument("--epoch", type=int, default=5)
    parser.add_argument("--dataset", type=str, required=True)
    args = parser.parse_args()

    batch_size = args.batch_size
    epoch = args.epoch
    model_name = args.model.replace("/", "_")
    
    print("Checkpoint: ", args.model)
    
    # Initialize API client
    api_key = args.api_key or os.getenv("TOGETHER_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key required. Set TOGETHER_API_KEY or OPENAI_API_KEY env var, or use --api_key")
    
    api_base = args.api_base or os.getenv("OPENAI_API_BASE")
    
    client = OpenAI(
        api_key=api_key,
        base_url=api_base
    )
    
    overhead_dict = {
        "overhead": [],
        "memory_usage": [],
        "execution_time": [],
        "max_memory_peak": [],
        "correct": [],
    }
    
    with open(f"src/../results/{args.dataset}_{model_name}.json", "r") as f:
        dataset = json.load(f)
    
    if args.dataset == "HumanEval":
        humaneval_open_testcases = load_dataset("openai_humaneval", split="test")
        tmp_open_test_cases = {}
        for i in range(len(humaneval_open_testcases)):
            tmp_open_test_cases[humaneval_open_testcases[i]["entry_point"]] = humaneval_open_testcases[i]["test"] + f"\ncheck{humaneval_open_testcases[i]['entry_point']}"
        for i in range(len(dataset)):
            dataset[i]["open_test_cases"] = tmp_open_test_cases[dataset[i]["entry_point"]]

    # Calculate initial overhead
    for i in tqdm(range(len(dataset))):
        overhead, memory_usage, execution_time, max_memory_peak, executable = calculate_code_execution_efficiency(dataset[i], evaluation_code=True)
        if executable:
            dataset[i]["overhead"] = overhead
            dataset[i]["memory_usage"] = memory_usage
            dataset[i]["execution_time"] = execution_time
            dataset[i]["max_memory_peak"] = max_memory_peak
            dataset[i]["executable"] = executable

    original_count = len(dataset)
    dataset = [entry for entry in dataset if "executable" in entry.keys() and entry["executable"]]
    if len(dataset) == 0:
        print(f"\n⚠️  WARNING: No executable code found in {original_count} entries!")
        print("   The script will exit as there are no entries to optimize.")
        print("   Please check that the generated code is executable.")
        exit(0)
    print(f"\n✓ Found {len(dataset)} executable entries to optimize (out of {original_count} total)")
    
    total_memory_usage = 0
    total_execution_time = 0
    total_max_memory_peak = 0
    normalize_total_memory_usage = 0
    normalize_total_execution_time = 0
    normalize_total_max_memory_peak = 0
    correct = 0
    for i in tqdm(range(len(dataset))):
        if "executable" in dataset[i].keys() and dataset[i]["executable"]:
            total_memory_usage += dataset[i]["memory_usage"]
            total_execution_time += dataset[i]["execution_time"]
            total_max_memory_peak += dataset[i]["max_memory_peak"]
            correct += 1

    if correct == 0:
        correct = 1
    total_overhead = f"""
The total memory usage during the code execution is: {round(total_memory_usage/correct,2)} MB*s.
The total execution time is: {round(total_execution_time/correct,2)} s.
The maximum memory peak requirement is: {round(total_max_memory_peak/correct,2)} MB.
"""
    overhead_dict["overhead"].append(total_overhead)
    overhead_dict["memory_usage"].append(round(total_memory_usage/correct,2))
    overhead_dict["execution_time"].append(round(total_execution_time/correct,2))
    overhead_dict["max_memory_peak"].append(round(total_max_memory_peak/correct,2))
    overhead_dict["correct"].append(correct)

    # Optimization epochs
    for current_epoch in range(1, epoch+1):
        print(f"\n=== Epoch {current_epoch}/{epoch} ===")
        
        # Process in batches with threading
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for i in range(0, len(dataset), batch_size):
                batch = dataset[i:i+batch_size]
                future = executor.submit(fetch_completion, copy.deepcopy(batch), args.model, client)
                futures.append((future, i, batch))
            
            for future, start_idx, batch in tqdm(futures, desc=f"Epoch {current_epoch}"):
                try:
                    results = future.result()
                    dataset[start_idx:start_idx+len(batch)] = results
                except Exception as e:
                    print(f"Error processing batch: {e}")

        total_memory_usage = 0
        total_execution_time = 0
        total_max_memory_peak = 0
        normalize_total_memory_usage = 0
        normalize_total_execution_time = 0
        normalize_total_max_memory_peak = 0
        correct = 0
        
        for i in range(len(dataset)):
            tmp_code = dataset[i]["completion"]
            dataset[i]["completion"] = dataset[i]["tmp_completion"]
            overhead, memory_usage, execution_time, max_memory_peak, executable = calculate_code_execution_efficiency(dataset[i], evaluation_code=True)
            if (("memory_usage" not in dataset[i].keys()) or (memory_usage < dataset[i]["memory_usage"])) and executable:
                dataset[i]["memory_usage"] = memory_usage
                dataset[i]["execution_time"] = execution_time
                dataset[i]["max_memory_peak"] = max_memory_peak
                dataset[i]["overhead"] = overhead
                dataset[i]["executable"] = executable
            else:
                dataset[i]["completion"] = tmp_code
            if "executable" in dataset[i].keys() and dataset[i]["executable"]:
                total_memory_usage += dataset[i]["memory_usage"]
                total_execution_time += dataset[i]["execution_time"]
                total_max_memory_peak += dataset[i]["max_memory_peak"]
                correct += 1
        
        if correct == 0:
            correct = 1
        total_overhead = f"""
The total memory usage during the code execution is: {round(total_memory_usage/correct,2)} MB*s.
The total execution time is: {round(total_execution_time/correct,2)} s.
The maximum memory peak requirement is: {round(total_max_memory_peak/correct,2)} MB.
"""
        overhead_dict["overhead"].append(total_overhead)
        overhead_dict["memory_usage"].append(round(total_memory_usage/correct,2))
        overhead_dict["execution_time"].append(round(total_execution_time/correct,2))
        overhead_dict["max_memory_peak"].append(round(total_max_memory_peak/correct,2))
        overhead_dict["correct"].append(correct)

        with open(f"src/../results/{args.dataset}_{model_name}_{current_epoch}.json", "w") as f:
            json.dump(dataset, f, indent=4)

    with open(f"src/../results/overhead_{model_name}.json", "w") as f:
        json.dump(overhead_dict, f, indent=4)

