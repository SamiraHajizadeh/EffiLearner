
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
    def totalNQueens(self, n: int) -> int:
        def backtrack(row=0, cols=0, hill_diag=0, dale_diag=0):
            nonlocal solutions
            if row == n:
                solutions += 1
                return
            available_positions = ((1 << n) - 1) & ~(cols | hill_diag | dale_diag)
            while available_positions:
                position = available_positions & -available_positions  # Get the rightmost 1
                available_positions &= available_positions - 1  # Turn off the rightmost 1
                backtrack(row + 1,
                          cols | position,
                          (hill_diag | position) << 1,
                          (dale_diag | position) >> 1)

        solutions = 0
        backtrack()
        return solutions

solution=Solution()

solution = Solution()
assert solution.totalNQueens(4) == 2
assert solution.totalNQueens(1) == 1
