#!/usr/bin/env python3
"""
Test the generated code from the output file to see if it works.
"""

import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))
from code_efficiency_calculator import calculate_code_execution_efficiency

def test_generated_code(input_file):
    """Test all generated code in the input file."""
    with open(input_file, 'r') as f:
        dataset = json.load(f)
    
    print(f"Testing {len(dataset)} entries...\n")
    
    results = []
    for i, entry in enumerate(dataset):
        print(f"\n{'='*60}")
        print(f"Entry {i+1}: Problem {entry.get('problem_idx', 'unknown')}")
        print(f"{'='*60}")
        
        if "completion" not in entry:
            print("❌ No completion found")
            results.append({"idx": entry.get('problem_idx'), "status": "no_completion"})
            continue
        
        # Test the code
        try:
            overhead, memory_usage, execution_time, max_memory_peak, executable = calculate_code_execution_efficiency(
                entry,
                evaluation_code=True,
                path="./tmp"
            )
            
            if executable:
                print(f"✅ Code is executable!")
                print(f"   Memory usage: {memory_usage:.2f} MB*s")
                print(f"   Execution time: {execution_time:.2f} s")
                print(f"   Max memory peak: {max_memory_peak:.2f} MB")
                results.append({
                    "idx": entry.get('problem_idx'),
                    "status": "executable",
                    "memory": memory_usage,
                    "time": execution_time
                })
            else:
                print(f"❌ Code execution failed")
                print(f"   Overhead: {overhead[:200]}...")
                results.append({"idx": entry.get('problem_idx'), "status": "failed"})
        except Exception as e:
            print(f"❌ Error testing code: {e}")
            results.append({"idx": entry.get('problem_idx'), "status": "error", "error": str(e)})
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    executable_count = sum(1 for r in results if r.get("status") == "executable")
    failed_count = sum(1 for r in results if r.get("status") == "failed")
    error_count = sum(1 for r in results if r.get("status") == "error")
    no_completion_count = sum(1 for r in results if r.get("status") == "no_completion")
    
    print(f"Total entries: {len(results)}")
    print(f"✅ Executable: {executable_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"⚠️  Errors: {error_count}")
    print(f"📝 No completion: {no_completion_count}")
    
    if executable_count > 0:
        avg_memory = sum(r.get("memory", 0) for r in results if r.get("status") == "executable") / executable_count
        avg_time = sum(r.get("time", 0) for r in results if r.get("status") == "executable") / executable_count
        print(f"\nAverage metrics (executable only):")
        print(f"  Memory: {avg_memory:.2f} MB*s")
        print(f"  Time: {avg_time:.2f} s")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_generated_code.py <input_json_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    if not Path(input_file).exists():
        print(f"Error: File not found: {input_file}")
        sys.exit(1)
    
    test_generated_code(input_file)

