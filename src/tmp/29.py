
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
    def divide(self, dividend: int, divisor: int) -> int:
        if dividend == 0:
            return 0
        if divisor == 1:
            return min(max(-2**31, dividend), 2**31 - 1)
        if divisor == -1:
            return min(max(-2**31, -dividend), 2**31 - 1)
        
        # Determine the sign of the quotient
        negative = (dividend < 0) ^ (divisor < 0)
        
        # Work with absolute values
        dividend, divisor = abs(dividend), abs(divisor)
        
        quotient = 0
        # Shift divisor until it is just less than dividend
        for i in range(31, -1, -1):
            if (divisor << i) <= dividend:
                dividend -= divisor << i
                quotient += 1 << i
        
        if negative:
            quotient = -quotient
          
        # Clamp to 32-bit signed integer range
        return min(max(-2**31, quotient), 2**31 - 1)

# Testing 
solution = Solution()
assert solution.divide(10, 3) == 3
assert solution.divide(7, -3) == -2

solution=Solution()

solution = Solution()
assert solution.divide(10, 3) == 3
assert solution.divide(7, -3) == -2
