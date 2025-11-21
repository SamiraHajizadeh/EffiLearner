#!/usr/bin/env python3
"""Check if completions contain extractable code wrapped in text/markdown"""

import json
import re

# Load the file
with open('results/MBPP_Qwen2.5-0.5B.json', 'r') as f:
    data = json.load(f)

print('Checking if completions contain extractable code...\n')
print('='*70)

extractable_count = 0
for i, entry in enumerate(data, 1):
    print(f'\nEntry {i} (Task ID: {entry.get("task_id", "unknown")}):')
    completion = entry.get('completion', '')
    
    extracted_code = None
    
    # Check for code blocks
    if '```python' in completion:
        print('  ✓ Contains ```python code block')
        code_start = completion.find('```python') + len('```python')
        code_end = completion.find('```', code_start)
        if code_end != -1:
            extracted_code = completion[code_start:code_end].strip()
            print(f'  Extracted code ({len(extracted_code)} chars)')
    elif '```' in completion:
        print('  ✓ Contains ``` code block')
        code_start = completion.find('```') + 3
        code_end = completion.find('```', code_start)
        if code_end != -1:
            extracted_code = completion[code_start:code_end].strip()
            print(f'  Extracted code ({len(extracted_code)} chars)')
    elif 'def ' in completion:
        print('  ✓ Contains function definition')
        # Try to extract function - look for def ... : followed by code
        func_match = re.search(r'def\s+\w+\([^)]*\):.*', completion, re.DOTALL)
        if func_match:
            extracted_code = func_match.group(0)
            # Try to clean up - remove trailing text
            lines = extracted_code.split('\n')
            cleaned_lines = []
            for line in lines:
                if line.strip() and not line.strip().startswith('#') and '```' not in line:
                    # Stop if we hit explanatory text (all caps, long sentences)
                    if len(line) > 100 and line.isupper():
                        break
                    cleaned_lines.append(line)
                elif line.strip().startswith('#'):
                    cleaned_lines.append(line)
            extracted_code = '\n'.join(cleaned_lines).strip()
            print(f'  Extracted function ({len(extracted_code)} chars)')
    
    if extracted_code:
        print(f'  Code preview: {extracted_code[:150]}...' if len(extracted_code) > 150 else f'  Code: {extracted_code}')
        extractable_count += 1
        
        # Check if it looks like valid Python
        if 'def ' in extracted_code and ('return' in extracted_code or 'print' in extracted_code or 'pass' in extracted_code):
            print('  ✓ Looks like valid Python function')
        else:
            print('  ⚠️  May not be complete function')
    else:
        print('  ✗ No extractable code found')
        print(f'  First 200 chars: {completion[:200]}...')
    
    print('='*70)

print(f'\n\nSUMMARY:')
print(f'Total entries: {len(data)}')
print(f'Entries with extractable code: {extractable_count}')
print(f'Entries without extractable code: {len(data) - extractable_count}')

