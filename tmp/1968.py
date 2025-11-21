
from typing import *
from bisect import *
from collections import *
from copy import *
from datetime import *
from heapq import *
from math import *
from re import *
from string import *
from random import *
from itertools import *
from functools import *
from operator import *

import string
import re
import datetime
import collections
import heapq
import bisect
import copy
import math
import random
import itertools
import functools
import operator


class TreeNode:
    def __init__(self, val=0, left=None, right=None, next=None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def rearrangeArray(self, nums):
        nums.sort()  # Step 1: Sort the array
        
        # Step 2: Split the array into two halves
        half = len(nums) // 2
        first_half = nums[:half]  # Lower half
        second_half = nums[half:]  # Upper half
        
        result = []
        
        # Step 3: Interleave the arrays
        for fh, sh in zip(first_half, second_half):
            result.append(fh)
            result.append(sh)
        
        # If the length of nums is odd, add the remaining element
        if len(nums) % 2 == 1:
            result.append(second_half[-1])
        
        return result

# Example Test Cases
solution = Solution()
print(solution.rearrangeArray([1,2,3,4,5]))  # Output: [1, 3, 2, 5, 4] or another valid configuration
print(solution.rearrangeArray([6,2,0,9,7]))  # Output: [0, 6, 2, 9, 7] or another valid configuration
solution=Solution()

solution = Solution()
assert solution.rearrangeArray([1,2,3,4,5]) == [1,3,2,5,4]
assert solution.rearrangeArray([6,2,0,9,7]) == [9,0,7,2,6]
