
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
    def removeDuplicates(self, nums):
        # Edge case where the list is empty or has one element
        if not nums:
            return 0
        
        # Initialize the first pointer
        i = 0
        
        # Iterate over the array with the second pointer
        for j in range(1, len(nums)):
            # When a different element is encountered
            if nums[i] != nums[j]:
                # Increment the first pointer
                i += 1
                # Update the unique element position
                nums[i] = nums[j]
        
        # The return value should be the number of unique elements, i.e., length of unique array part
        return i + 1

# Test cases
solution = Solution()
assert solution.removeDuplicates([1, 1, 2]) == 2
assert solution.removeDuplicates([0, 0, 1, 1, 1, 2, 2, 3, 3, 4]) == 5

solution=Solution()

solution = Solution()
assert solution.removeDuplicates([1, 1, 2]) == 2  # Because the first two elements after removing duplicates should be 1 and 2 respectively.
assert solution.removeDuplicates([0, 0, 1, 1, 1, 2, 2, 3, 3, 4]) == 5  # Because the first five elements after removing duplicates should be 0, 1, 2, 3, and 4 respectively.
