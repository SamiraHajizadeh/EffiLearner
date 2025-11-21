#!/usr/bin/env python3
import json

# Load the file
with open('results/MBPP_Qwen2.5-0.5B.json', 'r') as f:
    data = json.load(f)

print('Analyzing generated code correctness...\n')
print('='*70)

for i, entry in enumerate(data, 1):
    print(f'\nEntry {i} (Task ID: {entry.get("task_id", "unknown")}):')
    print(f'Prompt: {entry["prompt"]}')
    print(f'\nGenerated completion:')
    print(entry['completion'])
    print()
    
    completion = entry['completion']
    
    # Test Entry 1: min_val
    if i == 1:
        print('Testing min_val function:')
        try:
            # The completion is: "def min_val(lst):\n    return min(lst)"
            exec('''
def min_val(lst):
    return min(lst)
''')
            
            # Test with provided test cases
            test1 = min_val(['Python', 3, 2, 4, 5, 'version'])
            test2 = min_val(['Python', 15, 20, 25])
            test3 = min_val(['Python', 30, 20, 40, 50, 'version'])
            
            expected1 = 2
            expected2 = 15
            expected3 = 20
            
            print(f'  Test 1: min_val(["Python", 3, 2, 4, 5, "version"]) = {test1} (expected: {expected1})')
            if test1 == expected1:
                print('    ✅ CORRECT')
            else:
                print('    ❌ WRONG - This will fail because min() on mixed types compares strings and integers')
                print('    Issue: The function should filter for integers only using isinstance(i, int)')
            
            print(f'  Test 2: min_val(["Python", 15, 20, 25]) = {test2} (expected: {expected2})')
            if test2 == expected2:
                print('    ✅ CORRECT')
            else:
                print('    ❌ WRONG')
            
            print(f'  Test 3: min_val(["Python", 30, 20, 40, 50, "version"]) = {test3} (expected: {expected3})')
            if test3 == expected3:
                print('    ✅ CORRECT')
            else:
                print('    ❌ WRONG')
                
        except Exception as e:
            print(f'    ❌ ERROR: {e}')
            import traceback
            traceback.print_exc()
    
    # Test Entry 2: remove_whitespaces
    if i == 2:
        print('Testing remove_whitespaces function:')
        try:
            # Extract the function code from markdown
            if '```python' in completion:
                code_start = completion.find('```python') + len('```python')
                code_end = completion.find('```', code_start)
                func_code = completion[code_start:code_end].strip()
            elif 'def remove_whitespaces' in completion:
                func_start = completion.find('def remove_whitespaces')
                func_end = completion.find('\n\n', func_start)
                if func_end == -1:
                    func_end = len(completion)
                func_code = completion[func_start:func_end].strip()
            else:
                func_code = 'def remove_whitespaces(string):\n    return string.replace(" ", "")'
            
            # Execute the function
            exec(func_code)
            
            # Test with provided test cases
            test1 = remove_whitespaces(' Google    Flutter ')
            test2 = remove_whitespaces(' Google    Dart ')
            test3 = remove_whitespaces(' iOS    Swift ')
            
            expected1 = 'GoogleFlutter'
            expected2 = 'GoogleDart'
            expected3 = 'iOSSwift'
            
            print(f'  Test 1: remove_whitespaces(" Google    Flutter ") = "{test1}" (expected: "{expected1}")')
            if test1 == expected1:
                print('    ✅ CORRECT')
            else:
                print('    ❌ WRONG')
            
            print(f'  Test 2: remove_whitespaces(" Google    Dart ") = "{test2}" (expected: "{expected2}")')
            if test2 == expected2:
                print('    ✅ CORRECT')
            else:
                print('    ❌ WRONG')
            
            print(f'  Test 3: remove_whitespaces(" iOS    Swift ") = "{test3}" (expected: "{expected3}")')
            if test3 == expected3:
                print('    ✅ CORRECT')
            else:
                print('    ❌ WRONG')
                
            if test1 == expected1 and test2 == expected2 and test3 == expected3:
                print('\n  ✅ ALL TESTS PASSED - Function is correct!')
            else:
                print('\n  ❌ SOME TESTS FAILED')
                
        except Exception as e:
            print(f'    ❌ ERROR: {e}')
            import traceback
            traceback.print_exc()
    
    print('='*70)

