
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

from collections import deque

class Solution:
    def highestPeak(self, isWater):
        m, n = len(isWater), len(isWater[0])
        heights = [[-1] * n for _ in range(m)]
        queue = deque()

        # Start with all water cells
        for i in range(m):
            for j in range(n):
                if isWater[i][j] == 1:
                    heights[i][j] = 0
                    queue.append((i, j))

        # Directions for north, east, south, west
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        # BFS to assign heights
        while queue:
            x, y = queue.popleft()
            current_height = heights[x][y]

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n and heights[nx][ny] == -1:
                    heights[nx][ny] = current_height + 1
                    queue.append((nx, ny))

        return heights

# Test cases
solution = Solution()
assert solution.highestPeak([[0,1],[0,0]]) == [[1,0],[2,1]]
assert solution.highestPeak([[0,0,1],[1,0,0],[0,0,0]]) == [[1,1,0],[0,1,1],[1,2,2]]
solution=Solution()

solution = Solution()
assert solution.highestPeak([[0,1],[0,0]]) == [[1,0],[2,1]]
assert solution.highestPeak([[0,0,1],[1,0,0],[0,0,0]]) == [[1,1,0],[0,1,1],[1,2,2]]
