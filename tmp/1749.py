
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
    def maxAbsoluteSum(self, nums):
        max_ending_here = 0
        min_ending_here = 0
        max_so_far = 0
        min_so_far = 0
        
        for num in nums:
            # Calculate max subarray sum ending at current position
            max_ending_here = max(max_ending_here + num, num)
            max_so_far = max(max_so_far, max_ending_here)
            
            # Calculate min subarray sum ending at current position
            min_ending_here = min(min_ending_here + num, num)
            min_so_far = min(min_so_far, min_ending_here)
        
        return max(abs(max_so_far), abs(min_so_far))

# Example Test Cases
solution = Solution()
assert solution.maxAbsoluteSum([247]) == 247
assert solution.maxAbsoluteSum([596]) == 596
# Test Cases from Task Description
assert solution.maxAbsoluteSum([1,-3,2,3,-4]) == 5
assert solution.maxAbsoluteSum([2,-5,1,-4,3,-2]) == 8
solution=Solution()

solution = Solution()
# Example Test Cases
assert solution.maxAbsoluteSum([247]) == 247
assert solution.maxAbsoluteSum([596]) == 596
# Test Cases from Task Description
assert solution.maxAbsoluteSum([1,-3,2,3,-4]) == 5
assert solution.maxAbsoluteSum([2,-5,1,-4,3,-2]) == 8
