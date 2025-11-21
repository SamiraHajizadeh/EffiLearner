
#Assuming the input tuple is t = (t1, t2, t3, t4, t5)


def add_pairwise(t: tuple) -> tuple:
    s1: tuple = t[0] + t[1]
    s2: tuple = t[1] + t[2]
    s3: tuple = t[2] + t[3]
    s4: tuple = t[2] + t[4]
    s5: tuple = t[3] + t[4]
    
    return s1 + s2 + s3 + s4 + s5
assert add_pairwise((1, 5, 7, 8, 10)) == (6, 12, 15, 18)
assert add_pairwise((2, 6, 8, 9, 11)) == (8, 14, 17, 20)
assert add_pairwise((3, 7, 9, 10, 12)) == (10, 16, 19, 22)