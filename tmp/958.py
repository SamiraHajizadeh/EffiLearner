
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

from collections import deque

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def isCompleteTree(self, root: TreeNode) -> bool:
        if not root:
            return True
        
        # Initialize a queue for level-order traversal
        queue = deque([root])
        found_none = False
        
        while queue:
            node = queue.popleft()
            
            if node is None:
                found_none = True
            else:
                if found_none:
                    # If we've found a null before and we find a node,
                    # then it's not a complete tree
                    return False
                # Otherwise, continue with the level-order traversal
                queue.append(node.left)
                queue.append(node.right)
        
        return True

# Test cases (illustrative only, cannot be run directly due to custom TreeNode object references)
# Example:
# solution = Solution()
# assert solution.isCompleteTree(<__main__.TreeNode object containing [1,2,3,4,5,6]>) == True
# assert solution.isCompleteTree(<__main__.TreeNode object containing [1,2,3,4,5,null,7]>) == False
solution=Solution()

solution = Solution()
assert solution.isCompleteTree(<__main__.TreeNode object at 0x7fe65d8a6810>) == True
assert solution.isCompleteTree(<__main__.TreeNode object at 0x7fe65d8a6850>) == False
