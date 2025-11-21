
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
    def canJump(self, nums):
        max_reachable = 0
        target = len(nums) - 1
        for i, num in enumerate(nums):
            if i > max_reachable:
                return False
            max_reachable = max(max_reachable, i + num)
            if max_reachable >= target:
                return True
        return False

# Test cases
solution = Solution()
assert solution.canJump([2, 3, 1, 1, 4]) == True  # True because we can reach the last index
assert solution.canJump([3, 2, 1, 0, 4]) == False # False because we get stuck at index 3

solution=Solution()

solution = Solution()
assert solution.canJump([2, 3, 1, 1, 4]) == True
assert solution.canJump([3, 2, 1, 0, 4]) == False
