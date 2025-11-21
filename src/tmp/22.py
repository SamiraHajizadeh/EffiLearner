
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
    def generateParenthesis(self, n):
        def backtrack(s, open_count, close_count):
            if len(s) == 2 * n:
                result.append(s)
                return
            if open_count < n:
                backtrack(s + '(', open_count + 1, close_count)
            if close_count < open_count:
                backtrack(s + ')', open_count, close_count + 1)
        
        result = []
        backtrack('', 0, 0)
        return result

# Example usage
solution = Solution()
assert solution.generateParenthesis(3) == ["((()))", "(()())", "(())()", "()(())", "()()()"]
assert solution.generateParenthesis(1) == ["()"]

solution=Solution()

solution = Solution()
assert solution.generateParenthesis(3) == ["((()))", "(()())", "(())()", "()(())", "()()()"]
assert solution.generateParenthesis(1) == ["()"]
