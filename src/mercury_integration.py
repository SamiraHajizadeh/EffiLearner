#!/usr/bin/env python3
"""
Mercury dataset integration for EffiLearner.
Mercury is specifically designed for code efficiency evaluation - perfect for this project!
"""

import json
import os
import re
from datasets import load_dataset


def mercury_add_string_to_py_file(data, evaluation_code=False, path="./tmp/"):
    """
    Convert Mercury entry to executable Python file.
    Mercury structure:
    - prompt: The function signature and docstring
    - entry_point: Function name
    - test_cases: List of test cases with input/expected
    - generator_code: Code to generate more test cases
    - solutions: List of reference solutions
    """
    problem_id = str(data.get("id", data.get("task_id", "unknown")))
    return_path, full_code = "", ""
    
    try:
        # Get the code (completion or first solution)
        if "completion" in data:
            code = data["completion"]
        elif "solutions" in data and len(data["solutions"]) > 0:
            # Use first solution as reference
            code = data["solutions"][0]
        else:
            code = data.get("code", "")
        
        # Extract code from markdown if needed
        if "```python" in code:
            start_idx = code.find("```python")
            code = code[start_idx + len("```python"):]
            if "```" in code:
                end_idx = code.find("```")
                code = code[:end_idx]
        
        # Get entry point
        entry_point = data.get("entry_point", "")
        
        # Get test cases
        test_code = ""
        if evaluation_code:
            # Use test_cases from dataset
            test_cases = data.get("test_cases", [])
            if test_cases:
                # Convert test cases to assertions
                test_lines = []
                for test_case in test_cases[:10]:  # Limit to first 10 for execution
                    inputs = test_case.get("input", [])
                    expected = test_case.get("expected", None)
                    
                    if entry_point:
                        # Format: solution.entry_point(*inputs) == expected
                        if isinstance(inputs, list) and len(inputs) > 0:
                            # Handle nested lists (like [[[1,2,3]]])
                            if isinstance(inputs[0], list) and len(inputs) == 1:
                                input_str = str(inputs[0])
                            else:
                                input_str = ", ".join([str(inp) for inp in inputs])
                        else:
                            input_str = str(inputs)
                        
                        if expected is not None:
                            test_lines.append(f"assert solution.{entry_point}({input_str}) == {expected}")
                        else:
                            test_lines.append(f"solution.{entry_point}({input_str})")
                
                test_code = "\n".join(test_lines)
        else:
            # Use generator_code to generate test cases
            generator_code = data.get("generator_code", "")
            test_code = generator_code
        
        # Combine everything
        # Mercury uses class Solution pattern
        if "class Solution" in code or entry_point:
            if "class Solution" not in code:
                # Wrap in Solution class if needed
                class_code = f"class Solution:\n    {code.replace(chr(10), chr(10) + '    ')}"
            else:
                class_code = code
            
            full_code = f"{class_code}\n\nsolution = Solution()\n{test_code}"
        else:
            full_code = f"{code}\n{test_code}"
        
        # Write to file
        os.makedirs(path, exist_ok=True)
        file_path = f"./{path}/{problem_id}.py"
        with open(file_path, "w") as f:
            f.write(full_code)
        return_path = file_path
        
    except Exception as e:
        print(f"Error creating Mercury file: {e}")
        import traceback
        traceback.print_exc()
        return_path = None
    
    return return_path, full_code


def load_mercury_dataset(split="eval"):
    """
    Load Mercury dataset from HuggingFace.
    Splits: 'train' (1,633 samples) or 'eval' (256 samples)
    """
    try:
        dataset = load_dataset("Elfsong/Mercury", split=split)
        # Convert to list of dicts
        dataset_list = [dict(item) for item in dataset]
        # Add dataset identifier
        for item in dataset_list:
            item["dataset"] = "Mercury"
            if "task_id" not in item:
                item["task_id"] = f"mercury_{item.get('id', 'unknown')}"
        return dataset_list
    except Exception as e:
        print(f"Error loading Mercury: {e}")
        return None


def mercury_prompt_construction(data_entry):
    """
    Construct prompt for Mercury similar to other datasets.
    """
    prompt_text = data_entry.get("prompt", "")
    entry_point = data_entry.get("entry_point", "")
    
    # Mercury prompts are usually class-based
    full_prompt = f"Please complete Python code based on the task description.\n# Task description:\n{prompt_text}"
    if entry_point:
        full_prompt += f"\n# Function name: {entry_point}"
    full_prompt += "\n#Solution:\n"
    
    return full_prompt


# Example usage
if __name__ == "__main__":
    print("Loading Mercury dataset...")
    dataset = load_mercury_dataset(split="eval")
    
    if dataset:
        print(f"Loaded {len(dataset)} samples")
        sample = dataset[0]
        print(f"\nSample keys: {list(sample.keys())}")
        print(f"\nTask ID: {sample.get('id')}")
        print(f"Difficulty: {sample.get('difficulty')}")
        print(f"Entry point: {sample.get('entry_point')}")
        print(f"Number of solutions: {len(sample.get('solutions', []))}")
        print(f"\nPrompt preview: {sample['prompt'][:200]}...")
        
        # Test file creation
        print("\nTesting file creation...")
        script_path, full_code = mercury_add_string_to_py_file(
            sample,
            evaluation_code=True,
            path="./tmp/"
        )
        
        if script_path:
            print(f"Created file: {script_path}")
            print(f"\nCode preview (first 500 chars):\n{full_code[:500]}...")
        else:
            print("Failed to create file")
    else:
        print("Failed to load dataset")

