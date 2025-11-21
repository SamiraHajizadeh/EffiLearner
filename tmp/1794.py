
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
    def countQuadruples(self, firstString: str, secondString: str) -> int:
        # Substring to list of (end, start) pairs for firstString.
        substrings_first = {}
        
        # Create all substrings from firstString
        for start in range(len(firstString)):
            current_substring = ""
            for end in range(start, len(firstString)):
                current_substring += firstString[end]  # Extend the substring
                if current_substring not in substrings_first:
                    substrings_first[current_substring] = []
                substrings_first[current_substring].append((end, start))
        
        min_j_minus_a = float('inf')
        valid_quadruples = []
        
        # Now create all substrings from secondString and check against firstString substrings
        for a in range(len(secondString)):
            current_substring = ""
            for b in range(a, len(secondString)):
                current_substring += secondString[b]  # Extend the substring
                if current_substring in substrings_first:
                    for j, i in substrings_first[current_substring]:
                        # Calculate j - a
                        difference = j - a
                        if difference < min_j_minus_a:
                            min_j_minus_a = difference
                            valid_quadruples = [(i, j, a, b)]
                        elif difference == min_j_minus_a:
                            valid_quadruples.append((i, j, a, b))
        
        # Return the number of quadruples with the minimum j - a difference
        return len(valid_quadruples)

# Test cases
solution = Solution()
assert solution.countQuadruples("abcd", "bccda") == 1
assert solution.countQuadruples("ab", "cd") == 0
solution=Solution()

solution = Solution()
assert solution.countQuadruples("abcd", "bccda") == 1
assert solution.countQuadruples("ab", "cd") == 0
