
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
        def is_safe(row, col):
            # Check if it's safe to place a queen at board[row][col]
            return not (cols[col] or diag1[row - col] or diag2[row + col])

        def place_queen(row, col):
            # Mark the queen's position
            board[row][col] = 'Q'
            cols[col] = True
            diag1[row - col] = True
            diag2[row + col] = True

        def remove_queen(row, col):
            # Remove the queen's position
            board[row][col] = '.'
            cols[col] = False
            diag1[row - col] = False
            diag2[row + col] = False

        def backtrack(row):
            if row == n:
                # All n queens are placed
                solutions.append(["".join(board[i]) for i in range(n)])
                return
            
            for col in range(n):
                if is_safe(row, col):
                    place_queen(row, col)
                    backtrack(row + 1)
                    remove_queen(row, col)

        # Initialization
        solutions = []
        board = [['.' for _ in range(n)] for _ in range(n)]
        cols = [False] * n
        diag1 = [False] * (2 * n - 1)
        diag2 = [False] * (2 * n - 1)
        
        # Trigger the backtracking process from the first row
        backtrack(0)
        return solutions

# Example test cases:
solution = Solution()
assert solution.solveNQueens(4) == [[".Q..", "...Q", "Q...", "..Q."], ["..Q.", "Q...", "...Q", ".Q.."]]
assert solution.solveNQueens(1) == [["Q"]]

solution=Solution()

solution = Solution()
assert solution.solveNQueens(4) == [[".Q..","...Q","Q...","..Q."], ["..Q.","Q...","...Q",".Q.."]]
assert solution.solveNQueens(1) == [["Q"]]
