
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
    def maximumUniqueSubarray(self, nums):
        left = 0
        current_sum = 0
        max_score = 0
        seen = {}

        for right in range(len(nums)):
            if nums[right] in seen and seen[nums[right]] >= left:
                left = seen[nums[right]] + 1
            seen[nums[right]] = right
            current_sum = sum(nums[left:right + 1])
            max_score = max(max_score, current_sum)

        return max_score

# Test cases to verify the solution
solution = Solution()
assert solution.maximumUniqueSubarray([4, 2, 4, 5, 6]) == 17
assert solution.maximumUniqueSubarray([5, 2, 1, 2, 5, 2, 1, 2, 5]) == 8
solution=Solution()

solution = Solution()
assert solution.maximumUniqueSubarray([4,2,4,5,6]) == 17
assert solution.maximumUniqueSubarray([5,2,1,2,5,2,1,2,5]) == 8
