
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
        def backtrack(start, end):
            if start == end:
                # If we reach the end, add the current permutation to the result
                result.append(nums[:])
            for i in range(start, end):
                # Swap the current element with the start
                nums[start], nums[i] = nums[i], nums[start]
                # Recurse with the next element as the starting point
                backtrack(start + 1, end)
                # Backtrack by reverting the swap
                nums[start], nums[i] = nums[i], nums[start]
        
        result = []
        backtrack(0, len(nums))
        return result

# Test cases
solution = Solution()
assert solution.permute([1, 2, 3]) == [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
assert solution.permute([0, 1]) == [[0, 1], [1, 0]]
assert solution.permute([1]) == [[1]]

solution=Solution()

solution = Solution()
assert solution.permute([1,2,3]) == [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
assert solution.permute([0,1]) == [[0,1],[1,0]]
assert solution.permute([1]) == [[1]]
