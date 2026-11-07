cat << 'EOF' > main.py
import random
import time
import sympy

def miller_rabin_pass(n, a):
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    for k in range(1, s):
        x = pow(x, 2, n)
        if x == n - 1:
            return True
    return False

def is_probable_prime(n, bases):
    for a in bases:
        if n % a == 0:
            return n == a
        if not miller_rabin_pass(n, a):
            return False
    return True

def main():
    random.seed(42)
    bit_length = 512
    bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]

    start_time = time.perf_counter()
    candidates_tested = 0

    while True:
        candidates_tested += 1
        candidate = random.getrandbits(bit_length)
        candidate |= (1 << (bit_length - 1)) | 1
        if is_probable_prime(candidate, bases):
            break

    exec_time = time.perf_counter() - start_time

    print("=" * 70)
    print("  CRYPTOGRAPHIC PRIME GENERATION USING MILLER-RABIN (512-BIT)")
    print("=" * 70)
    print(f"Assigned bit length          : {bit_length}")
    print(f"Generated prime (Decimal)    : {candidate}")
    print(f"Generated prime (Hex)        : {hex(candidate)}")
    print(f"Actual bit length            : {candidate.bit_length()}")
    print(f"Number of candidates tested  : {candidates_tested}")
    print(f"Number of Miller-Rabin rounds: {len(bases)}")
    print(f"Bases used                   : {bases}")
    print(f"Total execution time         : {exec_time:.6f} seconds")
    print("-" * 70)
    print("VERIFICATION:")
    print(f"1. Exact 512-bit check (2^511 <= n < 2^512) : {2**511 <= candidate < 2**512}")
    print(f"2. Miller-Rabin passed for all 20 bases     : {is_probable_prime(candidate, bases)}")
    print(f"3. Independent SymPy isprime() verification : {sympy.isprime(candidate)}")
    print("=" * 70)

if __name__ == "__main__":
    main()
EOF
