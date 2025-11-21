#!/usr/bin/env python3
import json
import sys
sys.path.insert(0, 'src')
from code_efficiency_calculator import mbpp_add_string_to_py_file

# Test with entries that have different formats
with open('results/MBPP_Qwen2.5-0.5B.json', 'r') as f:
    data = json.load(f)

# Test entry 10 (has markdown)
print('Testing Entry 10 (with markdown):')
entry10 = data[9].copy()
print(f'Has markdown: {"```python" in entry10["completion"]}')
try:
    return_path, full_code = mbpp_add_string_to_py_file(entry10, evaluation_code=True, path='./tmp')
    if return_path:
        print('✓ Successfully extracted from markdown')
    else:
        print('✗ Failed')
except Exception as e:
    print(f'✗ Error: {e}')

print()
print('Testing Entry 1 (plain function):')
entry1 = data[0].copy()
print(f'Has markdown: {"```python" in entry1["completion"]}')
try:
    return_path, full_code = mbpp_add_string_to_py_file(entry1, evaluation_code=True, path='./tmp')
    if return_path:
        print('✓ Successfully extracted plain function')
    else:
        print('✗ Failed')
except Exception as e:
    print(f'✗ Error: {e}')

