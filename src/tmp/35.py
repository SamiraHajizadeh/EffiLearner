
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
    def searchInsert(self, nums, target):
        left, right = 0, len(nums) - 1
        
        while left <= right:
            mid = (left + right) // 2
            
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        # If we don't find the target, left will be the insertion point
        return left

# Testing the solution with given test cases
solution = Solution()
assert solution.searchInsert([1, 3, 5, 6], 5) == 2
assert solution.searchInsert([1, 3, 5, 6], 2) == 1
assert solution.searchInsert([1, 3, 5, 6], 7) == 4

solution=Solution()

solution = Solution()
assert solution.searchInsert([1, 3, 5, 6], 5) == 2
assert solution.searchInsert([1, 3, 5, 6], 2) == 1
assert solution.searchInsert([1, 3, 5, 6], 7) == 4
