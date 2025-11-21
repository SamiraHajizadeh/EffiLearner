
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
    def minIncrementForUnique(self, nums):
        nums.sort()
        moves = 0
        # The smallest possible number that the current value must be
        expected = 0
        
        for num in nums:
            # If the current number is less than expected, we need to increment
            if num < expected:
                moves += expected - num
            # Set the next expected number to current + 1
            expected = max(expected, num) + 1
        
        return moves

# Solution setup
solution = Solution()

# Test cases
assert solution.minIncrementForUnique([1, 2, 2]) == 1
assert solution.minIncrementForUnique([3, 2, 1, 2, 1, 7]) == 6
solution=Solution()

solution = Solution()
assert solution.minIncrementForUnique([1, 2, 2]) == 1
assert solution.minIncrementForUnique([3, 2, 1, 2, 1, 7]) == 6
