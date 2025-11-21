
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
    def strWithout3a3b(self, a: int, b: int) -> str:
        result = []
        
        while a > 0 or b > 0:
            if a > b:
                if a >= 2:
                    result.append('aa')
                    a -= 2
                else:
                    result.append('a')
                    a -= 1
                if b > 0:
                    result.append('b')
                    b -= 1
            elif b > a:
                if b >= 2:
                    result.append('bb')
                    b -= 2
                else:
                    result.append('b')
                    b -= 1
                if a > 0:
                    result.append('a')
                    a -= 1
            else:  # a == b
                result.append('ab')
                a -= 1
                b -= 1
        
        return ''.join(result)

# Testing against provided test cases
solution = Solution()
assert solution.strWithout3a3b(1, 2) == "abb" or solution.strWithout3a3b(1, 2) == "bab" or solution.strWithout3a3b(1, 2) == "bba"
assert solution.strWithout3a3b(4, 1) == "aabaa" or solution.strWithout3a3b(4, 1) == "abaaa"

# Here, we handled cases by always ensuring that two same characters only appear when possible
# and if any opposing character can be placed, it is added in between to avoid triple repetition.
solution=Solution()

solution = Solution()
assert solution.strWithout3a3b(1, 2) == "abb" or solution.strWithout3a3b(1, 2) == "bab" or solution.strWithout3a3b(1, 2) == "bba"
assert solution.strWithout3a3b(4, 1) == "aabaa"
