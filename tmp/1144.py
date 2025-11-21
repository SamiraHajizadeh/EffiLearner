
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
    def movesToMakeZigzag(self, nums):
        def moves_to_convert(expected_greater):
            moves = 0
            for i in range(len(nums)):
                # Check if the current index follows the expected pattern
                if (i % 2 == 0 and expected_greater) or (i % 2 == 1 and not expected_greater):
                    # num is an even index and should be greater or
                    # num is an odd index and should be less
                    if i > 0 and nums[i] <= nums[i - 1]:
                        moves += nums[i - 1] - nums[i] + 1
                    if i < len(nums) - 1 and nums[i] <= nums[i + 1]:
                        moves += nums[i + 1] - nums[i] + 1
                else:
                    # num is an even index and should be less or
                    # num is an odd index and should be greater
                    if i > 0 and nums[i] >= nums[i - 1]:
                        moves += nums[i] - nums[i - 1] + 1
                    if i < len(nums) - 1 and nums[i] >= nums[i + 1]:
                        moves += nums[i] - nums[i + 1] + 1
            return moves
        
        # Calculate moves for both possible zigzag patterns
        moves_even_greater = moves_to_convert(True)   # Pattern 1: nums[0] > nums[1] < nums[2] > ...
        moves_odd_greater = moves_to_convert(False)   # Pattern 2: nums[0] < nums[1] > nums[2] < ...
        
        return min(moves_even_greater, moves_odd_greater)

# Testing the solution with the provided test cases
solution = Solution()
assert solution.movesToMakeZigzag([1, 2, 3]) == 2
assert solution.movesToMakeZigzag([9, 6, 1, 6, 2]) == 4
solution=Solution()

solution = Solution()
assert solution.movesToMakeZigzag([1,2,3]) == 2
assert solution.movesToMakeZigzag([9,6,1,6,2]) == 4
