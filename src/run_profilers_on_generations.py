#!/usr/bin/env python3
"""
Run both profilers (Scalene and default) on generated code from a results JSON file.
Saves profiler outputs to results/profiler/{filename}_{profiler}.json
"""

import argparse
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path
from tqdm import tqdm

# Import helper functions
from code_efficiency_calculator import calculate_code_execution_efficiency
from RunSmallEffi import generate_scalene_overhead, PROFILE_TMP_DIR, get_completion_file_path


def extract_code_from_completion(completion):
    """Extract Python code from completion string, removing markdown code blocks if present."""
    code = completion.strip()
    
    # Remove markdown code blocks
    if "```python" in code:
        start_idx = code.find("```python")
        code = code[start_idx + len("```python"):]
        if "```" in code:
            end_idx = code.find("```")
            code = code[:end_idx]
    elif "```" in code:
        start_idx = code.find("```")
        code = code[start_idx + 3:]
        if "```" in code:
            end_idx = code.find("```")
            code = code[:end_idx]
    
    return code.strip()




def process_entry(entry, temp_dir, scalene_output_dir, profiler_timeout=30):
    """
    Process a single entry: run both profilers following the pattern from EffiLearnerScalen.py
    """
    results = {
        "problem_idx": entry.get("problem_idx", entry.get("task_id", "unknown")),
        "scalene_output": None,
        "default_profiler_output": None,
        "error": None
    }
    
    try:
        # Prepare entry for profiling - preserve all original fields
        entry_copy = entry.copy()
        
        # Extract and clean completion code if needed
        if "completion" in entry_copy:
            completion_code = extract_code_from_completion(entry_copy["completion"])
            entry_copy["completion"] = completion_code
        
        # Ensure dataset field is set (required by calculate_code_execution_efficiency)
        if "dataset" not in entry_copy:
            entry_copy["dataset"] = "EffiBench"  # Default to EffiBench if not specified
        
        # Run default profiler using calculate_code_execution_efficiency (same as EffiLearner.py)
        # This writes the file, runs profiling, and returns overhead
        overhead, memory_usage, execution_time, max_memory_peak, executable = calculate_code_execution_efficiency(
            entry_copy,
            evaluation_code=True,
            path=temp_dir
        )
        
        results["default_profiler_output"] = overhead
        
        if not executable:
            results["error"] = "Code execution failed"
            # Still try to get Scalene output if script exists
            script_path = get_completion_file_path(entry_copy, temp_dir)
            if script_path and os.path.exists(script_path):
                scalene_output = generate_scalene_overhead(
                    script_path,
                    scalene_output_dir,
                    timeout=profiler_timeout,
                    runs=1
                )
                results["scalene_output"] = scalene_output
            return results
        
        # Get the script path that was created by calculate_code_execution_efficiency
        script_path = get_completion_file_path(entry_copy, temp_dir)
        
        # Run Scalene profiler if script exists (same as EffiLearnerScalen.py)
        if script_path and os.path.exists(script_path):
            scalene_output = generate_scalene_overhead(
                script_path,
                scalene_output_dir,
                timeout=profiler_timeout,
                runs=1
            )
            results["scalene_output"] = scalene_output
        else:
            results["scalene_output"] = f"Script path not found for Scalene profiling (path: {script_path})"
            
    except Exception as e:
        results["error"] = f"Error processing entry: {str(e)}"
        import traceback
        results["error"] += f"\n{traceback.format_exc()}"
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Run profilers on generated code from a results JSON file"
    )
    parser.add_argument(
        "--input_file",
        type=str,
        required=True,
        help="Path to input JSON file with generated code (e.g., results/EffiBench_gpt-4o_none.json)"
    )
    parser.add_argument(
        "--profiler_timeout",
        type=int,
        default=30,
        help="Timeout for profiler execution in seconds (default: 30)"
    )
    parser.add_argument(
        "--num_samples",
        type=int,
        default=0,
        help="Number of samples to process (0 = all samples)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for sampling"
    )
    
    args = parser.parse_args()
    
    # Load input file
    input_path = Path(args.input_file)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    print(f"Loading input file: {input_path}")
    with open(input_path, 'r') as f:
        dataset = json.load(f)
    
    # Sample if requested
    if args.num_samples > 0 and len(dataset) > args.num_samples:
        import random
        random.seed(args.seed)
        random.shuffle(dataset)
        dataset = dataset[:args.num_samples]
        print(f"Processing {len(dataset)} samples (sampled from total dataset)")
    else:
        print(f"Processing all {len(dataset)} samples")
    
    # Setup directories
    input_filename = input_path.stem  # e.g., "EffiBench_gpt-4o_none"
    results_dir = Path("results") / "profiler"
    results_dir.mkdir(parents=True, exist_ok=True)
    
    temp_dir = Path(PROFILE_TMP_DIR)
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    scalene_output_dir = results_dir / "scalene_reports"
    scalene_output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process each entry
    profiler_results = {
        "scalene": [],
        "default": []
    }
    
    print("\nRunning profilers on generated code...")
    for entry in tqdm(dataset, desc="Processing entries"):
        result = process_entry(
            entry,
            str(temp_dir),
            str(scalene_output_dir),
            profiler_timeout=args.profiler_timeout
        )
        
        # Add entry metadata
        entry_result_scalene = {
            "problem_idx": result["problem_idx"],
            "profiler_output": result["scalene_output"],
            "error": result.get("error")
        }
        entry_result_default = {
            "problem_idx": result["problem_idx"],
            "profiler_output": result["default_profiler_output"],
            "error": result.get("error")
        }
        
        profiler_results["scalene"].append(entry_result_scalene)
        profiler_results["default"].append(entry_result_default)
    
    # Save results
    scalene_output_path = results_dir / f"{input_filename}_scalene.json"
    default_output_path = results_dir / f"{input_filename}_default.json"
    
    with open(scalene_output_path, 'w') as f:
        json.dump(profiler_results["scalene"], f, indent=2)
    print(f"\nScalene profiler results saved to: {scalene_output_path}")
    
    with open(default_output_path, 'w') as f:
        json.dump(profiler_results["default"], f, indent=2)
    print(f"Default profiler results saved to: {default_output_path}")
    
    # Print summary
    scalene_success = sum(1 for r in profiler_results["scalene"] if r.get("profiler_output") and not r.get("error"))
    default_success = sum(1 for r in profiler_results["default"] if r.get("profiler_output") and not r.get("error"))
    
    print(f"\nSummary:")
    print(f"  Scalene profiler: {scalene_success}/{len(dataset)} successful")
    print(f"  Default profiler: {default_success}/{len(dataset)} successful")


if __name__ == "__main__":
    main()

