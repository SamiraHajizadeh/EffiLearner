
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
    def lengthOfLongestSubstring(self, s: str) -> int:
        # Set to store the characters in current window
        char_set = set()
        # Initialize pointers for the sliding window
        left = 0
        # Variable to store the maximum length of substring found
        max_length = 0
        
        # Iterate through the string using another pointer `right`
        for right in range(len(s)):
            # If the character s[right] is in the set, slide the window from the left
            while s[right] in char_set:
                char_set.remove(s[left])
                left += 1
            # Add the character s[right] to the set
            char_set.add(s[right])
            # Update the maximum length of substring without repeating characters
            max_length = max(max_length, right - left + 1)
        
        return max_length

# Testing the solution with the given test cases
solution = Solution()
assert solution.lengthOfLongestSubstring("abcabcbb") == 3
assert solution.lengthOfLongestSubstring("bbbbb") == 1
assert solution.lengthOfLongestSubstring("pwwkew") == 3

solution=Solution()

solution = Solution()
assert solution.lengthOfLongestSubstring("abcabcbb") == 3
assert solution.lengthOfLongestSubstring("bbbbb") == 1
assert solution.lengthOfLongestSubstring("pwwkew") == 3
