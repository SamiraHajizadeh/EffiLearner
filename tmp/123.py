
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
    def maxProfit(self, prices):
        if not prices:
            return 0
        
        first_buy = float('-inf')
        first_sell = 0
        second_buy = float('-inf')
        second_sell = 0
        
        for price in prices:
            first_buy = max(first_buy, -price)           # Buy first stock
            first_sell = max(first_sell, first_buy + price) # Sell first stock
            second_buy = max(second_buy, first_sell - price) # Buy second stock
            second_sell = max(second_sell, second_buy + price) # Sell second stock
        
        return second_sell

# Testing the implemented solution with the provided test cases
solution = Solution()
assert solution.maxProfit([3,3,5,0,0,3,1,4]) == 6
assert solution.maxProfit([1,2,3,4,5]) == 4
assert solution.maxProfit([7,6,4,3,1]) == 0
solution=Solution()

solution = Solution()
assert solution.maxProfit([3,3,5,0,0,3,1,4]) == 6
assert solution.maxProfit([1,2,3,4,5]) == 4
assert solution.maxProfit([7,6,4,3,1]) == 0
