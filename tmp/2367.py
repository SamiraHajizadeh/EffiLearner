
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
    def arithmeticTriplets(self, nums, diff):
        nums_set = set(nums)
        count = 0
        for num in nums:
            if (num - diff in nums_set) and (num + diff in nums_set):
                count += 1
        return count

# Tests
solution = Solution()
assert solution.arithmeticTriplets([0, 1, 4, 6, 7, 10], 3) == 2
assert solution.arithmeticTriplets([4, 5, 6, 7, 8, 9], 2) == 2
solution=Solution()

solution = Solution()
assert solution.arithmeticTriplets([0, 1, 4, 6, 7, 10], 3) == 2
assert solution.arithmeticTriplets([4, 5, 6, 7, 8, 9], 2) == 2
