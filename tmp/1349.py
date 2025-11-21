
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
    def maxStudents(self, seats):
        m, n = len(seats), len(seats[0])
        
        def valid_mask(rmask):
            # Check if the mask only places students at available seats
            for j in range(n):
                if (rmask & (1 << j)) and seats[i][j] == '#':
                    return False
            return True
        
        def can_place(prev_mask, cur_mask):
            # Ensure current mask does not cheat with previous mask
            if (cur_mask & (cur_mask >> 1)) != 0: return False
            if (cur_mask & (prev_mask << 1)) != 0: return False
            if (cur_mask & (prev_mask >> 1)) != 0: return False
            return True
        
        dp = [[-1] * (1 << n) for _ in range(m + 1)]
        dp[0][0] = 0
        
        for i in range(m):
            for j in range(1 << n):
                if dp[i][j] == -1: continue
                for k in range(1 << n):
                    if valid_mask(k) and can_place(j, k):
                        cnt = bin(k).count('1')
                        dp[i+1][k] = max(dp[i+1][k], dp[i][j] + cnt)
        
        return max(dp[m])

# Test case validation
solution = Solution()
assert solution.maxStudents([
    ['#', '.', '#', '#', '.', '#'],
    ['.', '#', '#', '#', '#', '.'],
    ['#', '.', '#', '#', '.', '#']
]) == 4

assert solution.maxStudents([
    ['.', '#'],
    ['#', '#'],
    ['#', '.'],
    ['#', '#'],
    ['.', '#']
]) == 3

assert solution.maxStudents([
    ['#', '.', '.', '.', '#'],
    ['.', '#', '.', '#', '.'],
    ['.', '.', '#', '.', '.'],
    ['.', '#', '.', '#', '.'],
    ['#', '.', '.', '.', '#']
]) == 10
solution=Solution()

solution = Solution()
assert solution.maxStudents([
    ['#', '.', '#', '#', '.', '#'],
    ['.', '#', '#', '#', '#', '.'],
    ['#', '.', '#', '#', '.', '#']
]) == 4

assert solution.maxStudents([
    ['.', '#'],
    ['#', '#'],
    ['#', '.'],
    ['#', '#'],
    ['.', '#']
]) == 3

assert solution.maxStudents([
    ['#', '.', '.', '.', '#'],
    ['.', '#', '.', '#', '.'],
    ['.', '.', '#', '.', '.'],
    ['.', '#', '.', '#', '.'],
    ['#', '.', '.', '.', '#']
]) == 10
