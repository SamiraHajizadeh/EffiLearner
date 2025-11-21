
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
    def permute(self, nums):
        result = []
        
        # Helper function for backtracking
        def backtrack(first=0):
            # If we've completed a permutation
            if first == len(nums):
                result.append(nums[:])
                return

            for i in range(first, len(nums)):
                # Swap
                nums[first], nums[i] = nums[i], nums[first]
                # Recursive call
                backtrack(first + 1)
                # Backtrack (revert swap)
                nums[first], nums[i] = nums[i], nums[first]
        
        # Start backtracking
        backtrack()
        return result

solution=Solution()

solution = Solution()
assert solution.permute([1,2,3]) == [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
assert solution.permute([0,1]) == [[0,1],[1,0]]
assert solution.permute([1]) == [[1]]
