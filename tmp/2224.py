
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
    def convertTime(self, current: str, correct: str) -> int:
        # convert "HH:MM" to minutes since "00:00"
        def time_to_minutes(time: str) -> int:
            hours, minutes = map(int, time.split(':'))
            return hours * 60 + minutes

        # convert both times to minutes
        current_minutes = time_to_minutes(current)
        correct_minutes = time_to_minutes(correct)

        # calculate the difference in minutes
        diff = correct_minutes - current_minutes

        # count the number of operations needed
        operations = 0
        for increment in [60, 15, 5, 1]:
            operations += diff // increment  # number of full increments we can use
            diff %= increment  # remaining minutes after using the increments

        return operations

# Solution instance
solution = Solution()

# Test cases
assert solution.convertTime("02:30", "04:35") == 3
assert solution.convertTime("11:00", "11:01") == 1
solution=Solution()

solution = Solution()
assert solution.convertTime("02:30", "04:35") == 3
assert solution.convertTime("11:00", "11:01") == 1
