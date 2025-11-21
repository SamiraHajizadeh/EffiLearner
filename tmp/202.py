
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
    def isHappy(self, n: int) -> bool:
        seen = set()
        while n != 1 and n not in seen:
            seen.add(n)
            n = sum(int(digit) ** 2 for digit in str(n))
        return n == 1

# Test cases
solution = Solution()
assert solution.isHappy(19) == True
assert solution.isHappy(2) == False

# You can add more test cases to verify the solution
print(solution.isHappy(7))   # Output should be True since 7 is a happy number
print(solution.isHappy(13))  # Output should be True since 13 is a happy number
print(solution.isHappy(20))  # Output should be False since 20 is not a happy number
solution=Solution()

solution = Solution()
assert solution.isHappy(19) == True
assert solution.isHappy(2) == False
