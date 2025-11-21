
def find_dissimilar(a, b):
    a_set = set(a)
    b_set = set(b)
    result = []
    
    for i in a_set:
        if i not in b_set:
            result.append(i)
            
    for i in b_set:
        if i not in a_set:
            result.append(i)
            
    result.sort()
    return result
assert find_dissimilar((3, 4, 5, 6), (5, 7, 4, 10)) == (3, 6, 7, 10)
assert find_dissimilar((1, 2, 3, 4), (7, 2, 3, 9)) == (1, 4, 7, 9)
assert find_dissimilar((21, 11, 25, 26), (26, 34, 21, 36)) == (34, 36, 11, 25)