
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
        def is_not_under_attack(row, col):
            if cols[col] or hill_diag[row - col] or dale_diag[row + col]:
                return False
            return True
        
        def place_queen(row, col):
            cols[col] = 1
            hill_diag[row - col] = 1
            dale_diag[row + col] = 1
        
        def remove_queen(row, col):
            cols[col] = 0
            hill_diag[row - col] = 0
            dale_diag[row + col] = 0
            
        def backtrack(row = 0):
            for col in range(n):
                if is_not_under_attack(row, col):
                    place_queen(row, col)
                    if row + 1 == n:
                        nonlocal solutions
                        solutions += 1
                    else:
                        backtrack(row + 1)
                    remove_queen(row, col)
        
        cols = [0] * n
        hill_diag = [0] * (2 * n - 1)
        dale_diag = [0] * (2 * n - 1)
        solutions = 0
        backtrack()
        return solutions

# Test cases
solution = Solution()
assert solution.totalNQueens(4) == 2
assert solution.totalNQueens(1) == 1

solution=Solution()

solution = Solution()
assert solution.totalNQueens(4) == 2
assert solution.totalNQueens(1) == 1
