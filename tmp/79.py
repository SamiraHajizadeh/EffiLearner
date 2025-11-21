
def word_len(my_str):
    return my_str is not None and len(my_str) % 2 == 0
print(word_len("Hadoop")) # should return False
print(word_len("great")) # should return True
print(word_len("structure")) # should return True

#Testcases:
assert word_len("Hadoop") == False
assert word_len("great") == True
assert word_len("structure") == True

import pytest
def word_len(my_str):
    return my_str is not None and len(my_str) % 2 == 0
def test_word_len():
    assert word_len("Hadoop") == False
    assert word_len("great") == True
    assert word_len("structure") == True
assert word_len("Hadoop") == False
assert word_len("great") == True
assert word_len("structure") == True