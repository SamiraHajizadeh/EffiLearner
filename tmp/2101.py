
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

from typing import List
import math

class Solution:
    def maximumDetonation(self, bombs: List[List[int]]) -> int:
        def is_in_range(bomb1, bomb2):
            """Check if bomb2 is within range of bomb1."""
            x1, y1, r1 = bomb1
            x2, y2, _ = bomb2
            # Calculate the square of the distance and compare with square of radius
            return (x2 - x1) ** 2 + (y2 - y1) ** 2 <= r1 ** 2
        
        n = len(bombs)
        # Construct adjacency list for the graph
        graph = [[] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j and is_in_range(bombs[i], bombs[j]):
                    graph[i].append(j)
        
        def dfs(node, visited):
            """Perform DFS from the given node."""
            count = 1
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    count += dfs(neighbor, visited)
            return count
        
        max_detonated = 0
        # Try detonating each bomb and calculate the total number detonated
        for i in range(n):
            visited = set([i])
            max_detonated = max(max_detonated, dfs(i, visited))
        
        return max_detonated

# Examples
solution = Solution()
assert solution.maximumDetonation([[2,1,3],[6,1,4]]) == 2
assert solution.maximumDetonation([[1,1,5],[10,10,5]]) == 1
assert solution.maximumDetonation([[1,2,3],[2,3,1],[3,4,2],[4,5,3],[5,6,4]]) == 5
solution=Solution()

solution = Solution()
assert solution.maximumDetonation([[2,1,3],[6,1,4]]) == 2
assert solution.maximumDetonation([[1,1,5],[10,10,5]]) == 1
assert solution.maximumDetonation([[1,2,3],[2,3,1],[3,4,2],[4,5,3],[5,6,4]]) == 5
