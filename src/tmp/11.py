
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
    def maxArea(self, height):
        max_area = 0
        left, right = 0, len(height) - 1
        
        while left < right:
            # Calculate the current area
            width = right - left
            current_height = min(height[left], height[right])
            current_area = width * current_height
            
            # Update max_area if current_area is larger
            max_area = max(max_area, current_area)
            
            # Move the pointer of the shorter line
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
                
        return max_area

# Test cases
solution = Solution()
assert solution.maxArea([1,8,6,2,5,4,8,3,7]) == 49
assert solution.maxArea([1,1]) == 1

solution=Solution()

solution = Solution()
assert solution.maxArea([1,8,6,2,5,4,8,3,7]) == 49
assert solution.maxArea([1,1]) == 1
