
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
    def minExtraChar(self, s: str, dictionary: list) -> int:
        n = len(s)
        word_set = set(dictionary)
        
        # dp[i] will store the minimum number of extra characters if partitioning s[i:] optimally
        dp = [float('inf')] * (n + 1)
        dp[n] = 0  # If there's no string to partition, there are no extra characters
        
        for i in range(n - 1, -1, -1):
            dp[i] = dp[i + 1] + 1  # assume the character at i is extra
            for j in range(i + 1, n + 1):
                if s[i:j] in word_set:
                    dp[i] = min(dp[i], dp[j])
        
        return dp[0]

# Test cases
solution = Solution()
assert solution.minExtraChar(s = "leetscode", dictionary = ["leet", "code", "leetcode"]) == 1
assert solution.minExtraChar(s = "sayhelloworld", dictionary = ["hello", "world"]) == 3
solution=Solution()

solution = Solution()
assert solution.minExtraChar(s = "leetscode", dictionary = ["leet", "code", "leetcode"]) == 1
assert solution.minExtraChar(s = "sayhelloworld", dictionary = ["hello", "world"]) == 3
