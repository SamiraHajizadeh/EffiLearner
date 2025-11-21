
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
    def isMatch(self, s: str, p: str) -> bool:
        # Initialize the DP table 
        dp = [[False] * (len(p) + 1) for _ in range(len(s) + 1)]
        
        # Base case, both strings are empty
        dp[0][0] = True
        
        # Initialize first row (case when s is an empty string)
        for j in range(1, len(p) + 1):
            if p[j-1] == '*':
                dp[0][j] = dp[0][j-1]
        
        # Fill the DP table
        for i in range(1, len(s) + 1):
            for j in range(1, len(p) + 1):
                if p[j-1] == '*':
                    dp[i][j] = dp[i-1][j] or dp[i][j-1]
                elif p[j-1] == '?' or s[i-1] == p[j-1]:
                    dp[i][j] = dp[i-1][j-1]
        
        return dp[len(s)][len(p)]

# Tests
solution = Solution()
assert solution.isMatch("aa", "a") == False
assert solution.isMatch("aa", "*") == True
assert solution.isMatch("cb", "?a") == False

solution=Solution()

solution = Solution()
assert solution.isMatch("aa", "a") == False
assert solution.isMatch("aa", "*") == True
assert solution.isMatch("cb", "?a") == False
