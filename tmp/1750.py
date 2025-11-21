
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
    def minimumLength(self, s: str) -> int:
        left = 0
        right = len(s) - 1
        
        while left < right and s[left] == s[right]:
            current_char = s[left]
            
            while left <= right and s[left] == current_char:
                left += 1
            while right >= left and s[right] == current_char:
                right -= 1
        
        return right - left + 1

# Example Usage and Test Cases
solution = Solution()
assert solution.minimumLength("ca") == 2
assert solution.minimumLength("cabaabac") == 0
assert solution.minimumLength("aabccabba") == 3
solution=Solution()

solution = Solution()
assert solution.minimumLength("ca") == 2
assert solution.minimumLength("cabaabac") == 0
assert solution.minimumLength("aabccabba") == 3
