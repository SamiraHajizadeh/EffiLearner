
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
    def minimumCost(self, s: str) -> int:
        n = len(s)
        total_cost = 0
        
        # Traverse through the string to accumulate cost based on flipping decisions
        for i in range(n - 1):
            if s[i] != s[i + 1]:  # there's a transition from '0' to '1' or '1' to '0'
                # Calculate minimum cost using either left flip or right flip
                left_flip_cost = i + 1
                right_flip_cost = n - i - 1
                total_cost += min(left_flip_cost, right_flip_cost)
        
        return total_cost

# Tests
solution = Solution()
assert solution.minimumCost("0011") == 2  # Example 1
assert solution.minimumCost("010101") == 9  # Example 2
solution=Solution()

solution = Solution()
assert solution.minimumCost("0011") == 2
assert solution.minimumCost("010101") == 9
