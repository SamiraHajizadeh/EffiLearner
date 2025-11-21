
def list_tuple(lista):
    num = ()
    for x in lista: 
        if x not in num:
            num += (x,)
    return num
assert list_tuple([5, 10, 7, 4, 15, 3])==(5, 10, 7, 4, 15, 3)
assert list_tuple([2, 4, 5, 6, 2, 3, 4, 4, 7])==(2, 4, 5, 6, 2, 3, 4, 4, 7)
assert list_tuple([58,44,56])==(58,44,56)