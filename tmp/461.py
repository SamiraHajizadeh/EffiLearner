
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
    def hammingDistance(self, x: int, y: int) -> int:
        # XOR the two numbers, the result will have 1s where the bits differ
        xor_result = x ^ y
        
        # Count the number of 1s in the binary representation of xor_result
        hamming_distance = bin(xor_result).count('1')
        
        return hamming_distance

# Create an object of Solution
solution = Solution()

# Test cases
assert solution.hammingDistance(1, 4) == 2
assert solution.hammingDistance(3, 1) == 1
solution=Solution()

solution = Solution()
assert solution.hammingDistance(1, 4) == 2
assert solution.hammingDistance(3, 1) == 1
