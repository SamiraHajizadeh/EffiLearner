
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
    def maximumTop(self, nums, k):
        n = len(nums)
        
        # If k == 0, no moves can be made, return the top element
        if k == 0:
            return nums[0]
        
        # If we cannot perform any moves and it's the only element, return -1
        if n == 1:
            return -1 if k % 2 == 1 else nums[0]
        
        # Collect maximum from first k-1 elements
        max_top = max(nums[:min(k-1, n)])
        
        # Check k-th element if exists, because it could be a candidate after k moves
        if k < n:
            max_top = max(max_top, nums[k])
        
        return max_top

# Example usage:
solution = Solution()
assert solution.maximumTop([5,2,2,4,0,6], 4) == 5
assert solution.maximumTop([2], 1) == -1
solution=Solution()

solution = Solution()
assert solution.maximumTop([5,2,2,4,0,6], 4) == 5
assert solution.maximumTop([2], 1) == -1
