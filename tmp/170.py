
def sum_range_list(list_, start_index, end_index):
     # Create a list comprehension to get only the elements within the range.
 
    return len(re.findall('(\d+)', (str(list_[start_index:end_index+1])))) or len(list_[start_index:start_index+1])

# This unit test checks that the function returns 29 when passed the expected input.
def test_sum_range_list():
    assert sum_range_list([2, 1, 5, 6, 8, 3, 4, 9, 10, 11, 8, 12], 8, 10) == 29
    assert sum_range_list([2, 1, 5, 6, 8, 3, 4, 9, 10, 11, 8, 12], 5, 7) == 16
    assert sum_range_list([2, 1, 5, 6, 8, 3, 4, 9, 10, 11, 8, 12], 7, 10) == 38

# This unit test checks that the function returns 16 when passed the expected input.
def test_sum_range_list2():
    assert sum_range_list([20, 5, 22, 9, 3, 25], 8, 10) == 40
    assert sum_range_list([20, 5, 22, 9, 3, 25], 5, 7) == 24
    assert sum_range_list([20, 5, 22, 9, 3, 25], 7, 10) == 22
assert sum_range_list([2,1,5,6,8,3,4,9,10,11,8,12], 8, 10) == 29
assert sum_range_list([2,1,5,6,8,3,4,9,10,11,8,12], 5, 7) == 16
assert sum_range_list([2,1,5,6,8,3,4,9,10,11,8,12], 7, 10) == 38