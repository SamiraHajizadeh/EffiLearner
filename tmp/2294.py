
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
    def partitionArray(self, nums, k):
        nums.sort()  # Sort the array to ensure we can efficiently partition it
        subsequences_count = 0
        start = 0  # Start index of the current subsequence

        i = 0
        while i < len(nums):
            # Count the current subsequence
            subsequences_count += 1
            
            # Find the maximal subsequence from the current start
            while i < len(nums) and nums[i] - nums[start] <= k:
                i += 1
            
            # The next element will be the start of a new subsequence
            start = i

        return subsequences_count

# Testing the solution
solution = Solution()
assert solution.partitionArray([3, 6, 1, 2, 5], 2) == 2
assert solution.partitionArray([1, 2, 3], 1) == 2
assert solution.partitionArray([2, 2, 4, 5], 0) == 3
solution=Solution()

solution = Solution()
assert solution.partitionArray([3,6,1,2,5], 2) == 2
assert solution.partitionArray([1,2,3], 1) == 2
assert solution.partitionArray([2,2,4,5], 0) == 3
