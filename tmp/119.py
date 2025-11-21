
def search(nums):
    low, high = 0, len(nums)
    while low < high:
        mid = low + (high-low) // 2
        if mid == len(nums[mid]):
            # If mid is already at its correct position
            low = mid+1
        else:
            # If middle value is already found. Skip to next number
            high = mid
    # Return the first unique element
    return nums[low]
assert search([1,1,2,2,3]) == 3
assert search([1,1,3,3,4,4,5,5,7,7,8]) == 8
assert search([1,2,2,3,3,4,4]) == 1