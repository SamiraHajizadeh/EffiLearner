
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
    def divisorSubstrings(self, num: int, k: int) -> int:
        # Convert the number to a string to find substrings
        num_str = str(num)
        length = len(num_str)
        k_beauty_count = 0

        # Iterate over each substring of length k
        for i in range(length - k + 1):
            # Extract the k-length substring
            substring = num_str[i:i + k]
            # Convert it to an integer
            substring_num = int(substring)
            # Check if the substring is a divisor of num
            if substring_num != 0 and num % substring_num == 0:
                k_beauty_count += 1

        return k_beauty_count

# Test cases
solution = Solution()
assert solution.divisorSubstrings(240, 2) == 2
assert solution.divisorSubstrings(430043, 2) == 2
solution=Solution()

solution = Solution()
assert solution.divisorSubstrings(240, 2) == 2
assert solution.divisorSubstrings(430043, 2) == 2
