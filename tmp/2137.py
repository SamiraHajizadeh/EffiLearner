
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
    def equalizeWater(self, buckets, loss):
        low, high = 0, max(buckets)
        eps = 1e-6
        
        def feasible(x):
            gain, loss_water = 0, 0
            for water in buckets:
                if water < x:
                    gain += (x - water)  # need to add this much
                else:
                    loss_water += (water - x) * (1 - loss / 100)
            
            return loss_water >= gain
        
        while high - low > eps:
            mid = (low + high) / 2
            if feasible(mid):
                low = mid
            else:
                high = mid
        
        return low

# Test cases
solution = Solution()
assert abs(solution.equalizeWater([1, 2, 7], 80) - 2.0) < 1e-5
assert abs(solution.equalizeWater([2, 4, 6], 50) - 3.5) < 1e-5
assert abs(solution.equalizeWater([3, 3, 3, 3], 40) - 3.0) < 1e-5
solution=Solution()

solution = Solution()
assert abs(solution.equalizeWater([1, 2, 7], 80) - 2.0) < 1e-5
assert abs(solution.equalizeWater([2, 4, 6], 50) - 3.5) < 1e-5
assert abs(solution.equalizeWater([3, 3, 3, 3], 40) - 3.0) < 1e-5
