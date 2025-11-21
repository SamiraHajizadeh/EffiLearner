
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
    def grayCode(self, n: int) -> list:
        if n == 0:
            return [0]
        
        # Base 1-bit Gray code sequence
        result = [0, 1]
        
        # Build up the sequence for n bits
        for i in range(2, n + 1):
            # Reflect the current sequence
            reflected = result[::-1]
            
            # Prefix '0' to the original, '1' to the reflected
            result = [x << 1 for x in result] + [(x << 1) | 1 for x in reflected]
        
        return result

# Test the solution
solution = Solution()
assert solution.grayCode(2) == [0, 1, 3, 2] or solution.grayCode(2) == [0, 2, 3, 1]
assert solution.grayCode(1) == [0, 1]
solution=Solution()

solution = Solution()
assert solution.grayCode(2) == [0, 1, 3, 2] or solution.grayCode(2) == [0, 2, 3, 1]
assert solution.grayCode(1) == [0, 1]
