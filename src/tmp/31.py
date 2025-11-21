
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
    def nextPermutation(self, nums):
        # Step 1: Find the rightmost "peak"
        i = len(nums) - 2
        while i >= 0 and nums[i] >= nums[i + 1]:
            i -= 1
        
        # Step 2: If such a number is found, find the number which is to be replaced
        if i >= 0:
            j = len(nums) - 1
            while nums[j] <= nums[i]:
                j -= 1
            # Swap numbers at i and j
            nums[i], nums[j] = nums[j], nums[i]
        
        # Step 3: Reverse the sequence from i + 1 till end
        self.reverse(nums, i + 1, len(nums) - 1)
    
    def reverse(self, nums, start, end):
        while start < end:
            nums[start], nums[end] = nums[end], nums[start]
            start, end = start + 1, end - 1

solution=Solution()

solution = Solution()
nums = [1,2,3]
solution.nextPermutation(nums)
assert nums == [1,3,2]

nums = [3,2,1]
solution.nextPermutation(nums)
assert nums == [1,2,3]

nums = [1,1,5]
solution.nextPermutation(nums)
assert nums == [1,5,1]
