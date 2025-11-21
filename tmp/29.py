
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
        # Handling special cases
        if divisor == 0:
            raise ValueError("Divisor cannot be zero.")
        if dividend == 0:
            return 0
        
        # Handle overflow case
        if dividend == -2**31 and divisor == -1:
            return 2**31 - 1
        
        # Determine the sign of the result
        sign = -1 if (dividend < 0) ^ (divisor < 0) else 1
        
        # Use absolute values for dividend and divisor
        dividend, divisor = abs(dividend), abs(divisor)
        
        # Calculate quotient
        quotient = 0
        while dividend >= divisor:
            temp, multiple = divisor, 1
            while dividend >= (temp << 1):
                temp <<= 1
                multiple <<= 1
            dividend -= temp
            quotient += multiple
        
        # Apply the sign to the quotient
        quotient = sign * quotient
        
        # Clamp to 32-bit signed integer range
        return max(-2**31, min(quotient, 2**31 - 1))

solution=Solution()

solution = Solution()
assert solution.divide(10, 3) == 3
assert solution.divide(7, -3) == -2
