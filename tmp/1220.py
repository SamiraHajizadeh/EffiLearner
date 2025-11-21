
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
    def countVowelPermutation(self, n: int) -> int:
        MOD = 10**9 + 7
        
        # Initialize counts for one-character strings ending with each vowel
        counts = [1] * 5 # This represents counts of strings of length 1 ending in 'a', 'e', 'i', 'o', 'u'

        for _ in range(n - 1):
            # Temporary variables to store the new counts for the current iteration
            a_count = counts[1]  # can be preceded by 'e'
            e_count = (counts[0] + counts[2]) % MOD  # can be preceded by 'a', 'i'
            i_count = (counts[0] + counts[1] + counts[3] + counts[4]) % MOD  # can be preceded by 'a', 'e', 'o', 'u'
            o_count = (counts[2] + counts[4]) % MOD  # can be preceded by 'i', 'u'
            u_count = counts[0]  # can be preceded by 'a'
            
            # Update counts with new values
            counts = [a_count, e_count, i_count, o_count, u_count]
        
        # Result is the sum of all counts since strings can end in any of the vowels
        return sum(counts) % MOD

# Solution instance
solution = Solution()

# Test cases
print(solution.countVowelPermutation(1)) # Expected: 5
print(solution.countVowelPermutation(2)) # Expected: 10
print(solution.countVowelPermutation(5)) # Expected: 68
solution=Solution()

solution = Solution()
assert solution.countVowelPermutation(1) == 5
assert solution.countVowelPermutation(2) == 10
assert solution.countVowelPermutation(5) == 68
