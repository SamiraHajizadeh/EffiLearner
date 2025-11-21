
def sum_digits(n):
    if n < 10:
        return n
    else:
        half = n // 10
        dig_sum = sum_digits(half) + n % 10
        return dig_sum

# Test the function with the provided assertions
assert sum_digits(345) == 12
assert sum_digits(12) == 3
assert sum_digits(97) == 16

# Function to verify the correctness of the total
def verify_solution(func):
    # Test cases for each test case to ensure that the function works as expected
    assert func(345) == 12, "Sum of digits of 345 should be 12"
    assert func(12) == 3, "Sum of digits of 12 should be 3"
    assert func(97) == 16, "Sum of digits of 97 should be 16"
    
# Verify the solution
verify_solution(sum_digits)
assert sum_digits(345)==12
assert sum_digits(12)==3
assert sum_digits(97)==16