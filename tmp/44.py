
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
        # We only need two rows in our DP table to store current and previous results
        previous = [False] * (len(p) + 1)
        current = [False] * (len(p) + 1)
        
        # Base case, both strings are empty
        previous[0] = True
        
        # Initialize first row (case when s is an empty string)
        for j in range(1, len(p) + 1):
            if p[j-1] == '*':
                previous[j] = previous[j-1]
        
        # Fill the DP table using just two rows
        for i in range(1, len(s) + 1):
            current[0] = False
            
            for j in range(1, len(p) + 1):
                if p[j-1] == '*':
                    current[j] = previous[j] or current[j-1]
                elif p[j-1] == '?' or s[i-1] == p[j-1]:
                    current[j] = previous[j-1]
                else:
                    current[j] = False

            # Prepare for the next iteration
            previous, current = current, previous
        
        return previous[len(p)]

solution=Solution()

solution = Solution()
assert solution.isMatch("aa", "a") == False
assert solution.isMatch("aa", "*") == True
assert solution.isMatch("cb", "?a") == False
