
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
            if height[left] < height[right]:
                current_area = (right - left) * height[left]
                left += 1
            else:
                current_area = (right - left) * height[right]
                right -= 1
            max_area = max(max_area, current_area)
                
        return max_area

solution=Solution()

solution = Solution()
assert solution.maxArea([1,8,6,2,5,4,8,3,7]) == 49
assert solution.maxArea([1,1]) == 1
