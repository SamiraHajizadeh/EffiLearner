
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
    def maxNumberOfFamilies(self, n: int, reservedSeats: List[List[int]]) -> int:
        #create a hashmap of already reserved seats
        reservedSeatMap = dict()

        for reserved in reservedSeats:
            seatIndex = reserved[0] - 1
            rowNumber = reserved[1] - 1
            reservedSeatMap[seatIndex] = rowNumber
        
        #create a dictionary with the maximum number of seats in each row
        #use floor division to get a list of row numbers with the maximum number of seats
        rowNumbersWithMaxSeats = list()
        for rowNumber in range(1,n+1):
            if rowCountInRow[rowNumber] + 1 in reservedSeatMap.keys():
                maxNumberOfSeats = rowNumber -1
                rowCountInRow[rowNumber] = maxNumberOfSeats
        maxRowNumberWithMaxSeats = [max(rowNumber) for rowNumber in rowCountInRow.values()]

        #use sort and reduce to calculate the total number of people on the cinema
        totalPersonsOnTheCinema = sum(rowCountInRow.values()) * maxRowNumberWithMaxSeats
        totalPersonsOnTheCinema = self.calculateForNumberOnEachRow(totalPersonsOnTheCinema,sum(rowCountInRow.values())) 
        return totalPersonsOnTheCinema

    #create a dict for max number of seats of a row as a key
    def calculateForNumberOnEachRow(self,totalNumberOfPerson,numberOfPeopleOnEachRow):
        maxNumberOfSeatsInEachRow = 0
        for rowNumber in range(1,11):
            return (totalNumberOfPerson // numberOfPeopleOnEachRow) * maxNumberOfSeatsInEachRow
        return totalNumberOfPerson

        #defining row numbers for the max number of seats in each row
    def rowCountInRow(self,rowNumber):
        rowOfPeople = self.getRowOfPeopleInRow(rowNumber)
        return sum(rowOfPeople)

        #defining an empty dictionary to store number of already reserved seats in each row and total number of seated people from that row
        numberOfRow = 0
        rowCountInRow = dict()
        if numberOfRow in rowCountInRow.keys():
            rowCountInRow[numberOfRow] = rowCountInRow[numberOfRow] + rowCountInRow[rowNumber]
            numberOfRow += 1
        else:
            rowCountInRow[numberOfRow] = rowCountInRow[rowNumber]
solution=Solution()

solution = Solution()
assert solution.maxNumberOfFamilies(3, [[1,2],[1,3],[1,8],[2,6],[3,1],[3,10]]) == 4
assert solution.maxNumberOfFamilies(2, [[2,1],[1,8],[2,6]]) == 2
assert solution.maxNumberOfFamilies(4, [[4,3],[1,4],[4,6],[1,7]]) == 4
