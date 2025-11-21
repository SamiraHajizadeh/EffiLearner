#!/usr/bin/env python3
"""
Run both Scalene and non-Scalene optimizations for 5 epochs each and compare results.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def find_generation_file(dataset, model, output_dir):
    """Find generation file in various possible locations."""
    possible_locations = [
        Path(output_dir) / "generation" / f"{dataset}_{model}_none.json",
        Path(output_dir) / f"{dataset}_{model}_none.json",
        Path(f"./{dataset}_{model}.json"),
        Path(f"results/generation/{dataset}_{model}_none.json"),
        Path(f"results/{dataset}_{model}_none.json"),
    ]
    
    for loc in possible_locations:
        if loc.exists():
            return str(loc)
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Run 5-epoch optimization comparison: Scalene vs Non-Scalene"
    )
    parser.add_argument("--dataset", type=str, default="EffiBench", help="Dataset name")
    parser.add_argument("--checkpoint", type=str, default="gpt-4o", help="Model name")
    parser.add_argument("--output_dir", type=str, default="results", help="Output directory")
    parser.add_argument("--sample_size", type=int, default=20, help="Number of samples")
    parser.add_argument("--batch_size", type=int, default=8, help="Batch size for optimization")
    parser.add_argument("--input_file", type=str, default=None, help="Path to generation file (if not provided, will search)")
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("5-Epoch Optimization Comparison: Scalene vs Non-Scalene")
    print("=" * 80)
    print(f"Dataset: {args.dataset}")
    print(f"Model: {args.checkpoint}")
    print(f"Output Directory: {args.output_dir}")
    print(f"Sample Size: {args.sample_size}")
    print(f"Iterations: 5 for each profiler")
    print("=" * 80)
    print()
    
    # Find or use provided generation file
    if args.input_file:
        gen_file = args.input_file
        if not Path(gen_file).exists():
            print(f"✗ Provided input file not found: {gen_file}")
            return 1
    else:
        gen_file = find_generation_file(args.dataset, args.checkpoint, args.output_dir)
        if not gen_file:
            print("⚠️  Generation file not found!")
            print(f"   Searched in:")
            for loc in [
                f"{args.output_dir}/generation/{args.dataset}_{args.checkpoint}_none.json",
                f"./{args.dataset}_{args.checkpoint}.json",
            ]:
                print(f"     - {loc}")
            print()
            print("   Please provide --input_file or generate baseline code first")
            return 1
    
    print(f"✓ Using generation file: {gen_file}")
    print()
    
    # Step 1: Non-Scalene optimization (5 epochs)
    print("=" * 80)
    print("Step 1: Running Non-Scalene optimization (5 epochs)")
    print("=" * 80)
    print()
    
    cmd_none = [
        sys.executable, "src/RunSmallEffi.py",
        "--dataset", args.dataset,
        "--checkpoint", args.checkpoint,
        "--epoch", "5",
        "--output_dir", args.output_dir,
        "--input_file", gen_file,
        "--sample_size", str(args.sample_size),
        "--no_shuffle",
        "--batch_size", str(args.batch_size),
    ]
    
    print(f"Running: {' '.join(cmd_none)}")
    result_none = subprocess.run(cmd_none)
    
    if result_none.returncode != 0:
        print(f"✗ Non-Scalene optimization failed with exit code {result_none.returncode}")
        return 1
    
    none_output = Path(args.output_dir) / "optimization" / f"{args.dataset}_{args.checkpoint}_none_5.json"
    print(f"✓ Non-Scalene optimization complete")
    print(f"  Output: {none_output}")
    print()
    
    # Step 2: Scalene optimization (5 epochs)
    print("=" * 80)
    print("Step 2: Running Scalene optimization (5 epochs)")
    print("=" * 80)
    print()
    
    cmd_scalene = [
        sys.executable, "src/RunSmallEffi.py",
        "--dataset", args.dataset,
        "--checkpoint", args.checkpoint,
        "--epoch", "5",
        "--output_dir", args.output_dir,
        "--input_file", gen_file,
        "--sample_size", str(args.sample_size),
        "--no_shuffle",
        "--batch_size", str(args.batch_size),
        "--use_scalene",
        "--scalene_runs", "1",
    ]
    
    print(f"Running: {' '.join(cmd_scalene)}")
    result_scalene = subprocess.run(cmd_scalene)
    
    if result_scalene.returncode != 0:
        print(f"✗ Scalene optimization failed with exit code {result_scalene.returncode}")
        return 1
    
    scalene_output = Path(args.output_dir) / "optimization" / f"{args.dataset}_{args.checkpoint}_scalene_5.json"
    print(f"✓ Scalene optimization complete")
    print(f"  Output: {scalene_output}")
    print()
    
    # Step 3: Compare results
    print("=" * 80)
    print("Step 3: Comparing results after 5 iterations")
    print("=" * 80)
    print()
    
    cmd_compare = [
        sys.executable, "src/compare_scalene_vs_none.py",
        "--dataset", args.dataset,
        "--model", args.checkpoint,
        "--output_dir", args.output_dir,
        "--epoch", "5",
    ]
    
    print(f"Running: {' '.join(cmd_compare)}")
    result_compare = subprocess.run(cmd_compare)
    
    print()
    print("=" * 80)
    print("Comparison complete!")
    print("=" * 80)
    print()
    print("Results saved to:")
    print(f"  Non-Scalene: {none_output}")
    print(f"  Scalene: {scalene_output}")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

