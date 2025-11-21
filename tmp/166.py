
def find_even_pair(nums):
    xor = 0
    count = 0
    for i in range(len(nums)-1):
        xor ^= nums[i]
        for j in range(i+1, len(nums)) :
            if xor & nums[j]==0 and i!=j:
                count += 1
    return count
#Test cases
assert find_even_pair([5, 4, 7, 2, 1]) == 4
assert find_even_pair([7, 2, 8, 1, 0, 5, 11]) == 9
assert find_even_pair([1, 2, 3]) == 1
def find_even_pair(nums):
    xor = 0
    count = 0
    for i in range(len(nums)-1):
        xor ^= nums[i]
        for j in range(i+1, len(nums)): 
            if xor & nums[j]==0 and i!=j:
                count += 1
    return count
assert find_even_pair([5, 4, 7, 2, 1]) == 4
assert find_even_pair([7, 2, 8, 1, 0, 5, 11]) == 9
assert find_even_pair([1, 2, 3]) == 1