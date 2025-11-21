
def is_Sub_Array(a,b):
    n1 = len(a)
    n2 = len(b)
    if n1 >= n2:
        temp = []
        for i in range(n1):
            if a[i] in b:
                temp.append(a[i])
            else:
                return False
        for i in temp:
            if i not in b:
                return False
    else:
        return False
print(is_Sub_Array([1,10,8,7], [1,3,5,7] )) #True
print(is_Sub_Array([1,10,8,7], [1,3,5,7] )) #False
assert is_Sub_Array([1,4,3,5],[1,2]) == False
assert is_Sub_Array([1,2,1],[1,2,1]) == True
assert is_Sub_Array([1,0,2,2],[2,2,0]) ==False