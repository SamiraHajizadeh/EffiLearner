
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

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def maximumAverageSubtree(self, root: TreeNode) -> float:
        max_average = [0]  # Using a list to store the maximum average found so far, as lists are mutable
        
        def dfs(node) -> (int, int):
            # Return (sum of subtree, number of nodes in subtree)
            if not node:
                return (0, 0)
            
            left_sum, left_count = dfs(node.left)
            right_sum, right_count = dfs(node.right)
            
            current_sum = left_sum + right_sum + node.val
            current_count = left_count + right_count + 1
            current_average = current_sum / current_count
            
            # Update the maximum average found so far
            max_average[0] = max(max_average[0], current_average)
            
            return (current_sum, current_count)
        
        # Start DFS traversal with the root
        dfs(root)
        
        return max_average[0]
solution=Solution()

solution = Solution()
assert abs(solution.maximumAverageSubtree(TreeNode(5, TreeNode(6), TreeNode(1))) - 6.00000) < 1e-5
assert abs(solution.maximumAverageSubtree(TreeNode(0, None, TreeNode(1))) - 1.00000) < 1e-5
