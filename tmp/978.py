
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
    def maxTurbulenceSize(self, arr):
        if len(arr) == 1:
            return 1
        
        max_len = 1
        start = 0
        
        for end in range(1, len(arr)):
            if end % 2 == 0:
                if arr[end] > arr[end-1]:
                    # Continue the turbulent pattern
                    if end - start + 1 > max_len:
                        max_len = end - start + 1
                else:
                    # Reset the window start position
                    if arr[end] != arr[end-1]:  # Avoid considering equal elements
                        start = end - 1
                    else:
                        start = end
            else:
                if arr[end] < arr[end-1]:
                    # Continue the turbulent pattern
                    if end - start + 1 > max_len:
                        max_len = end - start + 1
                else:
                    # Reset the window start position
                    if arr[end] != arr[end-1]:  # Avoid considering equal elements
                        start = end - 1
                    else:
                        start = end
        
        return max_len

# Test the solution with the provided test cases
solution = Solution()
assert solution.maxTurbulenceSize([9, 4, 2, 10, 7, 8, 8, 1, 9]) == 5
assert solution.maxTurbulenceSize([4, 8, 12, 16]) == 2
assert solution.maxTurbulenceSize([100]) == 1
solution=Solution()

solution = Solution()
assert solution.maxTurbulenceSize([9, 4, 2, 10, 7, 8, 8, 1, 9]) == 5
assert solution.maxTurbulenceSize([4, 8, 12, 16]) == 2
assert solution.maxTurbulenceSize([100]) == 1
