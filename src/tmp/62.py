
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
    def uniquePaths(self, m: int, n: int) -> int:
        # Create a 2D DP array with all elements initialized to 0
        dp = [[0] * n for _ in range(m)]
        
        # Initialize the first row and first column with 1s
        for i in range(m):
            dp[i][0] = 1
        for j in range(n):
            dp[0][j] = 1
        
        # Fill the rest of the dp array
        for i in range(1, m):
            for j in range(1, n):
                dp[i][j] = dp[i-1][j] + dp[i][j-1]
        
        return dp[m-1][n-1]

# Create instance of Solution
solution = Solution()

# Test cases
assert solution.uniquePaths(3, 7) == 28
assert solution.uniquePaths(3, 2) == 3

solution=Solution()

solution = Solution()
assert solution.uniquePaths(3, 7) == 28
assert solution.uniquePaths(3, 2) == 3
