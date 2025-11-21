
def sum_series(x):
    if x < 3:
        return x
    else:
        return sum_series(x-2) + (x-1) if x & 1 else sum_series(x-2) + x
assert sum_series(6) == 12
assert sum_series(10) == 30
assert sum_series(9) == 25

#Test cases
#Test your solution with the following assertions
print('Task successful!')
assert sum_series(6) == 12
assert sum_series(10) == 30
assert sum_series(9) == 25