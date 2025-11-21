
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
    def groupAnagrams(self, strs):
        anagrams = defaultdict(list)
        
        for s in strs:
            # Count the frequency of each character and create a key based on that
            char_count = [0] * 26  # Assuming only lowercase English letters
            for char in s:
                char_count[ord(char) - ord('a')] += 1
            # Use the tuple of counts as a key
            anagrams[tuple(char_count)].append(s)
        
        # Return the groups of anagrams
        return list(anagrams.values())

solution=Solution()

solution = Solution()
assert solution.groupAnagrams(["eat","tea","tan","ate","nat","bat"]) == [["bat"],["nat","tan"],["ate","eat","tea"]]
assert solution.groupAnagrams([""]) == [[""]]
assert solution.groupAnagrams(["a"]) == [["a"]]
