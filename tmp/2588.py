
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

from collections import defaultdict

class Solution:
    def beautifulSubarrays(self, nums):
        # Initialize with the XOR value of zero occurring once
        xor_dict = defaultdict(int)
        xor_dict[0] = 1
        
        current_xor = 0
        beautiful_count = 0
        
        for num in nums:
            # Compute the cumulative XOR up to this point
            current_xor ^= num
            # If current_xor has occurred before, it means there is a subarray which is beautiful
            beautiful_count += xor_dict[current_xor]
            # Record the occurrence of this current_xor value
            xor_dict[current_xor] += 1
        
        return beautiful_count

# Test cases
solution = Solution()
assert solution.beautifulSubarrays([4,3,1,2,4]) == 2
assert solution.beautifulSubarrays([1,10,4]) == 0
solution=Solution()

solution = Solution()
assert solution.beautifulSubarrays([4,3,1,2,4]) == 2
assert solution.beautifulSubarrays([1,10,4]) == 0
