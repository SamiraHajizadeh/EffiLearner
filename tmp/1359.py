
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
    def countOrders(self, n: int) -> int:
        MOD = 10**9 + 7
        # dp[i] represents the number of valid sequences for i pairs
        dp = [0] * (n + 1)
        dp[0] = 1  # Base case: 1 way to arrange 0 orders
        
        for i in range(1, n + 1):
            # Calculate the dp value for dp[i]
            dp[i] = dp[i - 1] * (2 * i - 1) * i % MOD
        
        return dp[n]

# Testing the solution
solution = Solution()
assert solution.countOrders(1) == 1
assert solution.countOrders(2) == 6
assert solution.countOrders(3) == 90
solution=Solution()

solution = Solution()
assert solution.countOrders(1) == 1
assert solution.countOrders(2) == 6
assert solution.countOrders(3) == 90
