#!/usr/bin/env python3
"""
Standalone script to optimize code with profiling feedback.
Takes baseline code, profiles it, and sends to LLM for optimization.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from tqdm import tqdm
from openai import OpenAI

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from code_efficiency_calculator import calculate_code_execution_efficiency
from RunSmallEffi import (
    prompt_construction,
    get_completion_file_path,
    generate_scalene_overhead,
    PROFILE_TMP_DIR,
)


def optimize_entry(entry, client, model_name, use_scalene=False, scalene_runs=1, scalene_output_dir=None):
    """
    Optimize a single entry:
    1. Profile baseline code
    2. Send to LLM for optimization
    3. Profile optimized code
    4. Return best version
    """
    # Step 1: Profile baseline code
    print(f"  Profiling baseline code...")
    overhead, memory_usage, execution_time, max_memory_peak, executable = calculate_code_execution_efficiency(
        entry, evaluation_code=True, path=PROFILE_TMP_DIR
    )
    
    if not executable:
        print(f"  ✗ Baseline code is not executable")
        return entry, False
    
    baseline_metrics = {
        "memory_usage": memory_usage,
        "execution_time": execution_time,
        "max_memory_peak": max_memory_peak,
    }
    
    # Optionally get Scalene overhead
    scalene_overhead = None
    if use_scalene:
        script_path = get_completion_file_path(entry, PROFILE_TMP_DIR)
        if script_path and os.path.exists(script_path):
            print(f"  Running Scalene profiling...")
            scalene_overhead = generate_scalene_overhead(
                script_path, output_dir=scalene_output_dir, runs=scalene_runs
            )
    
    # Use Scalene overhead if available, otherwise use regular overhead
    overhead_text = scalene_overhead if (use_scalene and scalene_overhead) else overhead
    
    # Step 2: Get task description and test cases
    if entry.get("dataset") == "EffiBench":
        test_case = entry.get("small_test_cases", "")
        task_description = entry.get("markdown_description", "")
    elif entry.get("dataset") == "HumanEval":
        test_case = entry.get("open_test_cases", "")
        task_description = entry.get("prompt", "")
    elif entry.get("dataset") == "MBPP":
        test_case = "\n".join(entry.get("test_list", []))
        task_description = entry.get("prompt", "")
    else:
        test_case = ""
        task_description = ""
    
    # Step 3: Construct optimization prompt
    completion = entry.get("completion", "")
    prompt = prompt_construction(task_description, test_case, completion, overhead_text)
    
    # Step 4: Send to LLM for optimization
    print(f"  Requesting optimization from LLM...")
    try:
        resp = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            timeout=100,
        )
        optimized_code = resp.choices[0].message.content
    except Exception as e:
        print(f"  ✗ LLM request failed: {e}")
        return entry, False
    
    # Step 5: Profile optimized code
    print(f"  Profiling optimized code...")
    entry["completion"] = optimized_code
    overhead_opt, memory_usage_opt, execution_time_opt, max_memory_peak_opt, executable_opt = calculate_code_execution_efficiency(
        entry, evaluation_code=True, path=PROFILE_TMP_DIR
    )
    
    if not executable_opt:
        print(f"  ✗ Optimized code is not executable, reverting")
        return entry, False
    
    # Step 6: Compare and return best
    if memory_usage_opt < baseline_metrics["memory_usage"]:
        print(f"  ✓ Optimization improved memory: {baseline_metrics['memory_usage']:.4f} → {memory_usage_opt:.4f} MB*s")
        entry["memory_usage"] = memory_usage_opt
        entry["execution_time"] = execution_time_opt
        entry["max_memory_peak"] = max_memory_peak_opt
        entry["overhead"] = overhead_opt
        entry["executable"] = True
        return entry, True
    else:
        print(f"  ✗ Optimization did not improve (reverting)")
        # Revert to original
        entry["completion"] = completion
        entry["memory_usage"] = baseline_metrics["memory_usage"]
        entry["execution_time"] = baseline_metrics["execution_time"]
        entry["max_memory_peak"] = baseline_metrics["max_memory_peak"]
        entry["overhead"] = overhead
        entry["executable"] = True
        return entry, False


def main():
    parser = argparse.ArgumentParser(
        description="Optimize code with profiling feedback"
    )
    parser.add_argument("--input_file", type=str, required=True, help="Input JSON file with generated code")
    parser.add_argument("--output_file", type=str, required=True, help="Output JSON file")
    parser.add_argument("--checkpoint", type=str, default="gpt-4o", help="Model name (e.g., gpt-4o)")
    parser.add_argument("--use_scalene", action="store_true", help="Use Scalene profiling")
    parser.add_argument("--scalene_runs", type=int, default=1, help="Number of Scalene runs")
    parser.add_argument("--scalene_output_dir", type=str, default=None, help="Directory for Scalene reports")
    parser.add_argument("--sample_size", type=int, default=0, help="Process only first N entries (0 = all)")
    
    args = parser.parse_args()
    
    # Setup
    os.makedirs(PROFILE_TMP_DIR, exist_ok=True)
    
    if args.scalene_output_dir:
        scalene_output_dir = args.scalene_output_dir
    else:
        scalene_output_dir = os.path.join(os.path.dirname(args.output_file), "scalene_reports")
    os.makedirs(scalene_output_dir, exist_ok=True)
    
    # Initialize OpenAI client
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE") if os.getenv("OPENAI_API_BASE") else None
    )
    
    # Load input
    print(f"Loading input from: {args.input_file}")
    with open(args.input_file, 'r') as f:
        dataset = json.load(f)
    
    if args.sample_size > 0:
        dataset = dataset[:args.sample_size]
        print(f"Processing first {args.sample_size} entries")
    
    # Process each entry
    optimized_count = 0
    for i, entry in enumerate(tqdm(dataset, desc="Optimizing")):
        problem_id = entry.get("problem_idx") or entry.get("task_id", f"entry_{i}")
        print(f"\n[{i+1}/{len(dataset)}] Processing {problem_id}...")
        
        if "completion" not in entry:
            print(f"  ✗ No completion found, skipping")
            continue
        
        entry, improved = optimize_entry(
            entry,
            client,
            args.checkpoint,
            use_scalene=args.use_scalene,
            scalene_runs=args.scalene_runs,
            scalene_output_dir=scalene_output_dir
        )
        
        if improved:
            optimized_count += 1
    
    # Save results
    print(f"\nSaving results to: {args.output_file}")
    os.makedirs(os.path.dirname(args.output_file) if os.path.dirname(args.output_file) else ".", exist_ok=True)
    with open(args.output_file, 'w') as f:
        json.dump(dataset, f, indent=4)
    
    print(f"\n✓ Complete!")
    print(f"  Total entries: {len(dataset)}")
    print(f"  Optimized: {optimized_count}")
    print(f"  Improvement rate: {optimized_count/len(dataset)*100:.1f}%")


if __name__ == "__main__":
    main()

