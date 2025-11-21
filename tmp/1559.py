
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
    def detectCycle(self, grid):
        # Dimensions of the grid
        m, n = len(grid), len(grid[0])

        # Directions: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # Visited array to keep track of visited cells
        visited = [[False] * n for _ in range(m)]

        def is_within_bounds(x, y):
            return 0 <= x < m and 0 <= y < n

        def dfs(x, y, from_x, from_y, char, length):
            if visited[x][y]:
                return length >= 4

            # Mark the cell as visited
            visited[x][y] = True

            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if is_within_bounds(new_x, new_y) and (new_x, new_y) != (from_x, from_y) and grid[new_x][new_y] == char:
                    if dfs(new_x, new_y, x, y, char, length + 1):
                        return True

            # Unmark the cell as visited (necessary for other explorations)
            visited[x][y] = False
            return False

        # Start DFS from each cell
        for i in range(m):
            for j in range(n):
                if not visited[i][j]:  # Only start from unvisited cells
                    if dfs(i, j, -1, -1, grid[i][j], 0):
                        return True

        return False

# Test cases
solution = Solution()
assert solution.detectCycle([["a","a","a","a"], ["a","b","b","a"], ["a","b","b","a"], ["a","a","a","a"]]) == True
assert solution.detectCycle([["c","c","c","a"], ["c","d","c","c"], ["c","c","e","c"], ["f","c","c","c"]]) == True
assert solution.detectCycle([["a","b","b"], ["b","z","b"], ["b","b","a"]]) == False
solution=Solution()

solution = Solution()
# Test case 1
assert solution.detectCycle([["a","a","a","a"], ["a","b","b","a"], ["a","b","b","a"], ["a","a","a","a"]]) == True
# Test case 2
assert solution.detectCycle([["c","c","c","a"], ["c","d","c","c"], ["c","c","e","c"], ["f","c","c","c"]]) == True
# Test case 3
assert solution.detectCycle([["a","b","b"], ["b","z","b"], ["b","b","a"]]) == False
