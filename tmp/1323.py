
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
    def maximum69Number(self, num: int) -> int:
        # Convert the number to a list of characters to allow modification
        num_list = list(str(num))
        
        # Iterate over the list
        for i in range(len(num_list)):
            # Change the first '6' to '9' and break after this change
            if num_list[i] == '6':
                num_list[i] = '9'
                break
        
        # Join the list back to a string and convert to integer
        return int(''.join(num_list))

# Testing the function
solution = Solution()
assert solution.maximum69Number(9669) == 9969
assert solution.maximum69Number(9996) == 9999
assert solution.maximum69Number(9999) == 9999
solution=Solution()

solution = Solution()
assert solution.maximum69Number(9669) == 9969
assert solution.maximum69Number(9996) == 9999
assert solution.maximum69Number(9999) == 9999
