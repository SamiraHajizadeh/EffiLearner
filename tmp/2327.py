
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
    def peopleAwareOfSecret(self, n: int, delay: int, forget: int) -> int:
        MOD = 10**9 + 7
        dp = [0] * (n + 1)
        dp[1] = 1  # On day 1, one person knows the secret
        
        peopleSharing = [0] * (n + 1)
        peopleSharing[1] = 1  # On day 1, one person can potentially share the secret after delay days
        
        for i in range(2, n + 1):
            # People who start sharing the secret today
            if i - delay >= 1:
                peopleSharing[i] = (peopleSharing[i - delay] + dp[i - delay]) % MOD
            
            # Update new people knowing the secret today
            dp[i] = peopleSharing[i]
            
            # People forgetting the secret today (i - forget)
            if i - forget >= 1:
                peopleSharing[i] = (peopleSharing[i] - dp[i - forget] + MOD) % MOD
        
        # The result is the number of people who can currently share the secret
        return sum(dp[-forget:]) % MOD

# Testing the solution with the provided test cases
solution = Solution()
assert solution.peopleAwareOfSecret(6, 2, 4) == 5
assert solution.peopleAwareOfSecret(4, 1, 3) == 6
solution=Solution()

solution = Solution()
assert solution.peopleAwareOfSecret(6, 2, 4) == 5
assert solution.peopleAwareOfSecret(4, 1, 3) == 6
