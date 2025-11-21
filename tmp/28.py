
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
    def strStr(self, haystack: str, needle: str) -> int:
        def kmp_table(pattern):
            """ Preprocess pattern to create jump table (also known as partial match table)."""
            table = [0] * len(pattern)
            j = 0  # length of previous longest prefix suffix
            for i in range(1, len(pattern)):
                while j > 0 and pattern[i] != pattern[j]:
                    j = table[j - 1]
                if pattern[i] == pattern[j]:
                    j += 1
                    table[i] = j
            return table
        
        if not needle:
            return 0
        
        table = kmp_table(needle)
        j = 0  # index for needle
        for i in range(len(haystack)):
            while j > 0 and haystack[i] != needle[j]:
                j = table[j - 1]
            if haystack[i] == needle[j]:
                j += 1
            if j == len(needle):
                return i - j + 1
        
        return -1

solution=Solution()

solution = Solution()
assert solution.strStr("sadbutsad", "sad") == 0
assert solution.strStr("leetcode", "leeto") == -1
