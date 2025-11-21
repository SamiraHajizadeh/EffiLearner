
def next_smallest_palindrome(n):
    if n<100:
        return n
    else:
        x = int(str(n)[::-1])
        return n + x
assert next_smallest_palindrome(99)==101
assert next_smallest_palindrome(1221)==1331
assert next_smallest_palindrome(120)==121