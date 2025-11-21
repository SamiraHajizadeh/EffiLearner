
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
        # Create a 2D DP table with False as the default value.
        dp = [[False] * (len(p) + 1) for _ in range(len(s) + 1)]
        
        # Base case: empty string and empty pattern match.
        dp[0][0] = True
        
        # Handle patterns like a*, a*b*, a*b*c* which can match an empty string.
        for j in range(2, len(p) + 1):
            if p[j - 1] == '*':
                dp[0][j] = dp[0][j - 2]

        # Fill the DP table.
        for i in range(1, len(s) + 1):
            for j in range(1, len(p) + 1):
                if p[j - 1] == '.' or p[j - 1] == s[i - 1]:
                    # Current characters match, inherit the value from top-left diagonal.
                    dp[i][j] = dp[i - 1][j - 1]
                elif p[j - 1] == '*':
                    # '*' can match zero occurrence of preceding element.
                    dp[i][j] = dp[i][j - 2]
                    # If the character before '*' matches s[i-1], use the result above.
                    if p[j - 2] == '.' or p[j - 2] == s[i - 1]:
                        dp[i][j] = dp[i][j] or dp[i - 1][j]

        # The final result is in the bottom-right corner of the table.
        return dp[len(s)][len(p)]

# Testing the solution with the provided test cases
solution = Solution()
assert solution.isMatch("aa", "a") == False
assert solution.isMatch("aa", "a*") == True
assert solution.isMatch("ab", ".*") == True

solution=Solution()

solution = Solution()
assert solution.isMatch("aa", "a") == False
assert solution.isMatch("aa", "a*") == True
assert solution.isMatch("ab", ".*") == True
