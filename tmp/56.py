
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
    def merge(self, intervals):
        # Early return for the empty intervals list
        if not intervals:
            return []

        # Sort the intervals based on start time
        intervals.sort(key=lambda x: x[0])

        # Initialize the list with the first interval
        merged_intervals = [intervals[0]]

        for current in intervals[1:]:
            last_merged = merged_intervals[-1]
            # If the current interval does not overlap with the last merged interval, add it
            if last_merged[1] < current[0]:
                merged_intervals.append(current)
            else:
                # There is overlap, so we merge
                last_merged[1] = max(last_merged[1], current[1])

        return merged_intervals

solution=Solution()

solution = Solution()
# Test case from the task description
assert solution.merge([[1,3],[2,6],[8,10],[15,18]]) == [[1,6],[8,10],[15,18]]
assert solution.merge([[1,4],[4,5]]) == [[1,5]]

# Additional Test cases
# Non-overlapping intervals
assert solution.merge([[1,2],[3,4],[5,6]]) == [[1,2],[3,4],[5,6]]
# Overlapping intervals at multiple points
assert solution.merge([[1,4],[2,3],[6,9],[7,10]]) == [[1,4],[6,10]]
# Single interval, should return the interval itself
assert solution.merge([[0,1]]) == [[0,1]]
# Empty list of intervals
assert solution.merge([]) == []
# Overlapping intervals that result in a single merged interval
assert solution.merge([[5,6],[1,3],[2,4]]) == [[1,4],[5,6]]
# Overlapping and adjacent intervals
assert solution.merge([[1,2],[2,3],[3,4]]) == [[1,4]]
