
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
    def pathsWithMaxScore(self, board):
        MOD = 10**9 + 7
        n = len(board)
        
        # Initialize DP tables
        max_sum = [[None] * n for _ in range(n)]
        count = [[0] * n for _ in range(n)]
        
        # Start condition
        max_sum[n-1][n-1] = 0
        count[n-1][n-1] = 1
        
        # Traverse the board
        for i in range(n-1, -1, -1):
            for j in range(n-1, -1, -1):
                if board[i][j] == 'X':
                    continue
                
                new_sum = 0 if board[i][j] in 'SE' else int(board[i][j])

                candidates = []
                if i < n-1 and max_sum[i+1][j] is not None:
                    candidates.append((max_sum[i+1][j] + new_sum, count[i+1][j]))
                if j < n-1 and max_sum[i][j+1] is not None:
                    candidates.append((max_sum[i][j+1] + new_sum, count[i][j+1]))
                if i < n-1 and j < n-1 and max_sum[i+1][j+1] is not None:
                    candidates.append((max_sum[i+1][j+1] + new_sum, count[i+1][j+1]))
                
                # Find max sum and initialize paths count
                max_here = -1
                paths_here = 0
                
                for value, cnt in candidates:
                    if value > max_here:
                        max_here = value
                        paths_here = cnt
                    elif value == max_here:
                        paths_here = (paths_here + cnt) % MOD
                
                if max_here != -1:
                    max_sum[i][j] = max_here
                    count[i][j] = paths_here
        
        if max_sum[0][0] is None:
            return [0, 0]
        else:
            return [max_sum[0][0], count[0][0]]

#Solution Tests
solution = Solution()
assert solution.pathsWithMax
solution=Solution()

solution = Solution()
assert solution.pathsWithMaxScore(["E23","2X2","12S"]) == [7, 1]
assert solution.pathsWithMaxScore(["E12","1X1","21S"]) == [4, 2]
assert solution.pathsWithMaxScore(["E11","XXX","11S"]) == [0, 0]
