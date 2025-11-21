import math

def slow_compute_primes(n):
    """Very naive prime finder, with redundant work."""
    primes = []
    for x in range(2, n):
        is_prime = True
        # computing sqrt(n) every time
        limit = int(math.sqrt(x)) + 1
        for d in range(2, limit):
            if x % d == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(x)
    return primes

if __name__ == "__main__":
    for _ in range(3):
        result = slow_compute_primes(100000)
    print(f"Found {len(result)} primes")