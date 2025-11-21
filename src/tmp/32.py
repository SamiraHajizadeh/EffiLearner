
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
    def longestValidParentheses(self, s: str) -> int:
        # Initialize stack with a base index of -1
        stack = [-1]
        max_length = 0

        for i, char in enumerate(s):
            if char == '(':
                # Push the index of the '(' onto the stack
                stack.append(i)
            else:
                # Pop the top index for a completed pair
                stack.pop()
                if not stack:
                    # If stack is empty after popping, push the current index as a new base
                    stack.append(i)
                else:
                    # Calculate the length of the valid substring
                    max_length = max(max_length, i - stack[-1])

        return max_length

# Testing the solution
solution = Solution()
assert solution.longestValidParentheses("(()") == 2
assert solution.longestValidParentheses(")()())") == 4
assert solution.longestValidParentheses("") == 0

print("All test cases passed.")

solution=Solution()

solution = Solution()
assert solution.longestValidParentheses("(()") == 2
assert solution.longestValidParentheses(")()())") == 4
assert solution.longestValidParentheses("") == 0
