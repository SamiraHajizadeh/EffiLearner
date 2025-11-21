
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
    def combinationSum2(self, candidates, target):
        def backtrack(start, target, path):
            if target == 0:
                result.append(list(path))
                return
            if target < 0:
                return

            for i in range(start, len(candidates)):
                # Skip duplicate elements.
                if i > start and candidates[i] == candidates[i - 1]:
                    continue
                
                # Include the number in the path.
                path.append(candidates[i])
                # Recurse with reduced target and the next starting index.
                backtrack(i + 1, target - candidates[i], path)
                # Backtrack, remove the number from the path.
                path.pop()

        candidates.sort()
        result = []
        backtrack(0, target, [])
        return result

# Testing the provided test cases
solution = Solution()
assert solution.combinationSum2([10, 1, 2, 7, 6, 1, 5], 8) == [
    [1, 1, 6],
    [1, 2, 5],
    [1, 7],
    [2, 6]
]
assert solution.combinationSum2([2, 5, 2, 1, 2], 5) == [
    [1, 2, 2],
    [5]
]

solution=Solution()

solution = Solution()
assert solution.combinationSum2([10, 1, 2, 7, 6, 1, 5], 8) == [
    [1, 1, 6],
    [1, 2, 5],
    [1, 7],
    [2, 6]
]
assert solution.combinationSum2([2, 5, 2, 1, 2], 5) == [
    [1, 2, 2],
    [5]
]
