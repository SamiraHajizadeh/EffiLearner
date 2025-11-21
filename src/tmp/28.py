
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
        return haystack.find(needle)

# Testing the solution with the given test cases
solution = Solution()
assert solution.strStr("sadbutsad", "sad") == 0
assert solution.strStr("leetcode", "leeto") == -1

solution=Solution()

solution = Solution()
assert solution.strStr("sadbutsad", "sad") == 0
assert solution.strStr("leetcode", "leeto") == -1
