
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
    def generate(self, numRows):
        # Initialize Pascal's triangle with the first row
        result = [[1]]
        
        # Build each row from 1 to numRows-1 (since index starts at 0)
        for i in range(1, numRows):
            # Start each row with a '1'
            row = [1]
            # Fill the current row where each element is the sum of elements from the previous row
            for j in range(1, i):
                row.append(result[i - 1][j - 1] + result[i - 1][j])
            # End each row with a '1'
            row.append(1)
            # Append the current row to the result
            result.append(row)
        
        return result

# Test cases
solution = Solution()
assert solution.generate(5) == [[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]
assert solution.generate(1) == [[1]]
solution=Solution()

solution = Solution()
assert solution.generate(5) == [[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]
assert solution.generate(1) == [[1]]
