
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
    def reverseOnlyLetters(self, s: str) -> str:
        # Convert the string into a list to modify characters
        chars = list(s)
        # Pointers for the two ends of the list
        left, right = 0, len(chars) - 1
        
        # Helper function to check if a character is an English letter
        def is_letter(c):
            return c.isalpha()

        while left < right:
            # Move left pointer to the right as long as it points to non-letter characters
            while left < right and not is_letter(chars[left]):
                left += 1
            # Move right pointer to the left as long as it points to non-letter characters
            while left < right and not is_letter(chars[right]):
                right -= 1
            
            # Swap the letters at left and right pointers
            chars[left], chars[right] = chars[right], chars[left]

            # Move both pointers
            left += 1
            right -= 1

        # Join the list back into a string and return it
        return ''.join(chars)

# Examples of usage:
solution = Solution()
assert solution.reverseOnlyLetters("ab-cd") == "dc-ba"
assert solution.reverseOnlyLetters("a-bC-dEf-ghIj") == "j-Ih-gfE-dCba"
assert solution.reverseOnlyLetters("Test1ng-Leet=code-Q!") == "Qedo1ct-eeLg=ntse-T!"
solution=Solution()

solution = Solution()
assert solution.reverseOnlyLetters("ab-cd") == "dc-ba"
assert solution.reverseOnlyLetters("a-bC-dEf-ghIj") == "j-Ih-gfE-dCba"
assert solution.reverseOnlyLetters("Test1ng-Leet=code-Q!") == "Qedo1ct-eeLg=ntse-T!"
