
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
    def uniquePaths(self, m: int, n: int) -> int:
        # Use a single array to store the path counts for the current row
        dp = [1] * n
        
        # Iterate over the grid excluding the first row as it's already initialized
        for i in range(1, m):
            for j in range(1, n):
                # Update the current cell value using the previous row's value and the left cell's value
                dp[j] += dp[j - 1]

        return dp[n - 1]

solution=Solution()

solution = Solution()
assert solution.uniquePaths(3, 7) == 28
assert solution.uniquePaths(3, 2) == 3
