#!/usr/bin/env python3
"""
Analyze generated code to identify specific errors.
"""

import json
import sys
from pathlib import Path

def analyze_code(completion, problem_idx):
    """Analyze a code completion and identify errors."""
    print(f"\n{'='*70}")
    print(f"Problem {problem_idx}")
    print(f"{'='*70}")
    print(f"\nGenerated Code:\n{completion}\n")
    
    errors = []
    warnings = []
    
    # Check for common issues
    if "class Solution" not in completion:
        warnings.append("Code is not wrapped in 'class Solution'")
    
    if "def " in completion and "class Solution" not in completion:
        errors.append("Function defined outside of class (needs to be a method)")
    
    # Check for undefined variables
    if "for i in s:" in completion or "for i in s " in completion:
        errors.append("Uses undefined variable 's' (should be 'nums' or 'range(len(nums))')")
    
    if "nums[j]" in completion and "j" not in completion[:completion.find("nums[j]")]:
        errors.append("Uses undefined variable 'j'")
    
    if "List[" in completion and "from typing import List" not in completion:
        errors.append("Uses 'List' type hint but missing import: 'from typing import List'")
    
    if "rowCountInRow" in completion:
        # Check if it's used before definition
        first_use = completion.find("rowCountInRow")
        if "rowCountInRow = " not in completion[:first_use] and "def rowCountInRow" not in completion[:first_use]:
            errors.append("Uses 'rowCountInRow' before it's defined")
    
    # Check for syntax issues
    if completion.count("def ") > completion.count("class "):
        if "class Solution" in completion:
            warnings.append("Multiple functions defined (may need to be methods)")
    
    # Check for incomplete logic
    if "return" not in completion:
        errors.append("Missing return statement")
    
    if "pass" in completion and completion.count("pass") > 2:
        warnings.append("Multiple 'pass' statements (incomplete implementation)")
    
    # Print results
    if errors:
        print("❌ ERRORS:")
        for error in errors:
            print(f"   • {error}")
    
    if warnings:
        print("⚠️  WARNINGS:")
        for warning in warnings:
            print(f"   • {warning}")
    
    if not errors and not warnings:
        print("✅ No obvious errors detected (but code may still be incorrect)")
    
    return len(errors), len(warnings)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_generated_code.py <input_json_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    if not Path(input_file).exists():
        print(f"Error: File not found: {input_file}")
        sys.exit(1)
    
    with open(input_file, 'r') as f:
        dataset = json.load(f)
    
    print(f"Analyzing {len(dataset)} generated code completions...")
    
    total_errors = 0
    total_warnings = 0
    
    for entry in dataset:
        completion = entry.get("completion", "")
        problem_idx = entry.get("problem_idx", "unknown")
        
        errors, warnings = analyze_code(completion, problem_idx)
        total_errors += errors
        total_warnings += warnings
    
    print(f"\n{'='*70}")
    print("OVERALL SUMMARY")
    print(f"{'='*70}")
    print(f"Total entries analyzed: {len(dataset)}")
    print(f"Total errors found: {total_errors}")
    print(f"Total warnings found: {total_warnings}")
    print(f"\nConclusion: {'❌ Generated code has errors' if total_errors > 0 else '⚠️  Generated code has warnings' if total_warnings > 0 else '✅ No obvious issues detected'}")

