
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
        # Sort the intervals based on start time
        intervals.sort(key=lambda x: x[0])
        
        merged_intervals = []
        
        for interval in intervals:
            # If the list of merged intervals is empty or there is no overlap with the last interval, append the interval
            if not merged_intervals or merged_intervals[-1][1] < interval[0]:
                merged_intervals.append(interval)
            else:
                # There is an overlap so merge the current interval with the last merged interval
                merged_intervals[-1][1] = max(merged_intervals[-1][1], interval[1])
        
        return merged_intervals

# Solution instance
solution = Solution()

# Test case from the task description
assert solution.merge([[1,3],[2,6],[8,10],[15,18]]) == [[1,6],[8,10],[15,18]]
assert solution.merge([[1,4],[4,5]]) == [[1,5]]

# Additional Test cases
assert solution.merge([[1,2],[3,4],[5,6]]) == [[1,2],[3,4],[5,6]]
assert solution.merge([[1,4],[2,3],[6,9],[7,10]]) == [[1,4],[6,10]]
assert solution.merge([[0,1]]) == [[0,1]]
assert solution.merge([]) == []
assert solution.merge([[5,6],[1,3],[2,4]]) == [[1,4],[5,6]]
assert solution.merge([[1,2],[2,3],[3,4]]) == [[1,4]]

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
