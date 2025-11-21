
def index_multiplication(a_tuple, b_tuple):
  for element1, element2 in zip(a_tuple, b_tuple):
    return (element1 * element2) if element1 not in b_tuple and element2 in a_tuple else None
#Test cases for the function:

a = ((1, 3), (4, 5), (2, 9), (1, 10))
b = ((6, 7), (3, 9), (1, 1), (7, 3))

expected_outcome = ((6, 21), (12, 45), (2, 9), (7, 30))
assert index_multiplication(a, b) == expected_outcome

y = ((2, 4), (5, 6), (3, 10), (2, 11))
z = ((7, 8), (4, 10), (2, 2), (8, 4))

#Assertion
assert index_multiplication(y, z) == (14, 32), (20, 60)

w = ((3, 5), (6, 7), (4, 11), (3, 12))
x = ((8, 9), (5, 11), (3, 3), (9, 5))

assert index_multiplication(w, x) == ((24, 45), (30, 77), (12, 20), (27, 60))
assert index_multiplication(((1, 3), (4, 5), (2, 9), (1, 10)),((6, 7), (3, 9), (1, 1), (7, 3)) ) == ((6, 21), (12, 45), (2, 9), (7, 30))
assert index_multiplication(((2, 4), (5, 6), (3, 10), (2, 11)),((7, 8), (4, 10), (2, 2), (8, 4)) ) == ((14, 32), (20, 60), (6, 20), (16, 44))
assert index_multiplication(((3, 5), (6, 7), (4, 11), (3, 12)),((8, 9), (5, 11), (3, 3), (9, 5)) ) == ((24, 45), (30, 77), (12, 33), (27, 60))