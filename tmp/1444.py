
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

from functools import lru_cache

class Solution:
    def ways(self, pizza: List[str], k: int) -> int:
        mod = 10**9 + 7
        rows, cols = len(pizza), len(pizza[0])
        
        # Precompute the prefix sum of apples in the pizza
        apples = [[0] * (cols + 1) for _ in range(rows + 1)]
        
        for r in range(rows - 1, -1, -1):
            for c in range(cols - 1, -1, -1):
                apples[r][c] = (1 if pizza[r][c] == 'A' else 0) + \
                               apples[r + 1][c] + apples[r][c + 1] - apples[r + 1][c + 1]
        
        @lru_cache(None)
        def dp(r, c, k):
            # Base case: if we need just one piece
            if k == 1:
                return 1 if apples[r][c] > 0 else 0
            
            # Calculate the number of ways
            ways_to_cut = 0
            # Horizontal cuts
            for nr in range(r + 1, rows):
                if apples[r][c] - apples[nr][c] > 0:  # Apple's existence check in the top part
                    ways_to_cut = (ways_to_cut + dp(nr, c, k - 1)) % mod
            # Vertical cuts
            for nc in range(c + 1, cols):
                if apples[r][c] - apples[r][nc] > 0:  # Apple's existence check in the left part
                    ways_to_cut = (ways_to_cut + dp(r, nc, k - 1)) % mod
            
            return ways_to_cut
        
        return dp(0, 0, k)

# Example usage:
solution = Solution()
assert solution.ways(["A..","AAA","..."], 3) == 3
assert solution.ways(["A..","AA.","..."], 3) == 1
assert solution.ways(["A..","A..","..."], 1) == 1
solution=Solution()

solution = Solution()
assert solution.ways(["A..","AAA","..."], 3) == 3
assert solution.ways(["A..","AA.","..."], 3) == 1
assert solution.ways(["A..","A..","..."], 1) == 1
