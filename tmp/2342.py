
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
    def maximumSum(self, nums) -> int:
        def sum_of_digits(n):
            total = 0
            while n > 0:
                total += n % 10
                n //= 10
            return total
        
        sum_map = {}
        for num in nums:
            digit_sum = sum_of_digits(num)
            if digit_sum not in sum_map:
                sum_map[digit_sum] = []
            sum_map[digit_sum].append(num)
        
        max_sum = -1
        for num_list in sum_map.values():
            if len(num_list) > 1:
                num_list.sort(reverse=True)  # Sort in descending order
                max_sum = max(max_sum, num_list[0] + num_list[1])
        
        return max_sum

# Testing the implementation
solution = Solution()
assert solution.maximumSum([18, 43, 36, 13, 7]) == 54
assert solution.maximumSum([10, 12, 19, 14]) == -1
solution=Solution()

solution = Solution()
assert solution.maximumSum([18, 43, 36, 13, 7]) == 54
assert solution.maximumSum([10, 12, 19, 14]) == -1
