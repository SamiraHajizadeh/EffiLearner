
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
    def solveNQueens(self, n):
        def backtrack(row, hills, next_row, dales):
            if row == n:
                solutions.append(["".join(board[r]) for r in range(n)])
                return

            for col in range(n):
                if not (hills & (1 << (row - col + n - 1)) or next_row & (1 << col) or dales & (1 << (row + col))):
                    board[row][col] = 'Q'
                    backtrack(row + 1, hills | (1 << (row - col + n - 1)), next_row | (1 << col), dales | (1 << (row + col)))
                    board[row][col] = '.'

        solutions = []
        board = [['.' for _ in range(n)] for _ in range(n)]
        backtrack(0, 0, 0, 0)
        return solutions

solution=Solution()

solution = Solution()
assert solution.solveNQueens(4) == [[".Q..","...Q","Q...","..Q."], ["..Q.","Q...","...Q",".Q.."]]
assert solution.solveNQueens(1) == [["Q"]]
