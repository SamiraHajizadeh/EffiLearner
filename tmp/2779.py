
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
    def maximumBeauty(self, nums, k):
        # Sort nums to enable a sorted sliding window approach
        nums.sort()
        
        left = 0
        max_beauty = 0
        
        # Use a sliding window from 'left' to 'right'
        for right in range(len(nums)):
            # Move the left pointer to the right to maintain the valid range
            while nums[right] - nums[left] > 2 * k:
                left += 1
            # Calculate current window size
            max_beauty = max(max_beauty, right - left + 1)
        
        return max_beauty

# Test cases
solution = Solution()
assert solution.maximumBeauty([4,6,1,2], 2) == 3
assert solution.maximumBeauty([1,1,1,1], 10) == 4
solution=Solution()

solution = Solution()
assert solution.maximumBeauty([4,6,1,2], 2) == 3
assert solution.maximumBeauty([1,1,1,1], 10) == 4
