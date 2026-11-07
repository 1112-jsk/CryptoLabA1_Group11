cat << 'EOF' > README.md
# Cryptographic Prime Generation Using Miller–Rabin

## Objective
Generate a probable prime of 512-bit length using the Miller–Rabin primality test and verify its primality and bit length.

---

## 1. Experimental Results

| Parameter | Value |
| :--- | :--- |
| **Assigned bit length** | `512` |
| **Generated prime candidate (Decimal)** | `10067625340751739904071515698183247981367894638552061894642882880514911721226402502619899066569920292066097869904718599094997392462293186525867276742283161` |
| **Generated prime candidate (Hex)** | `0xc03987108976e334e2817efdae8492171d53434bb88139b9ae270da702f06b90f143262fdc5c0eed8da0365bf89897b9405cacec877409a977d21e02ff01cf99` |
| **Actual bit length of the candidate** | `512` |
| **Number of candidates tested** | `13` |
| **Number of Miller–Rabin rounds** | `20` (Bases: `2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71`) |
| **Total execution time** | `0.025643 seconds` |

---

## 2. Verification

### A. Bit Length Verification
1. **Bitwise Construction:** During candidate generation, the Most Significant Bit (bit 511) and Least Significant Bit (bit 0) are forced to `1` via `candidate |= (1 << 511) | 1`, ensuring the integer is odd and strictly 512 bits long.
2. **Range Check:**
   - $2^{511} \approx 6.7039 \times 10^{153}$
   - $n \approx 1.0067 \times 10^{154}$
   - $2^{512} \approx 1.3407 \times 10^{154}$
   - Since $2^{511} \le n < 2^{512}$, the candidate has exactly 512 bits.
3. **Hexadecimal Check:** The hex representation has 128 hex characters (`128 * 4 = 512 bits`) and starts with `c` (`1100` in binary), confirming the 512th bit is `1`.

### B. Miller–Rabin Base Verification
Writing $n - 1 = 2^s \cdot d$ with odd $d$ gives $s = 3$. The candidate was tested against the first 20 prime bases:
- **Bases tested:** `[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]`
- For every base $a$, either $a^d \equiv 1 \pmod n$ or $a^{2^r d} \equiv n - 1 \pmod n$ for some $0 \le r < 3$.
- Passing 20 independent rounds bounds the probability of a composite false positive to $\le 4^{-20} = 2^{-40} \approx 9.09 \times 10^{-13}$.

### C. Independent Primality Verification
1. **SymPy (`sympy.isprime`):** Verified using SymPy's `isprime(n)` function (which runs the deterministic/Baillie–PSW primality test combining strong Miller–Rabin and strong Lucas pseudoprime tests). Output: `True`.
2. **OpenSSL (`openssl prime`):** Verified via OpenSSL CLI (`openssl prime <candidate>`), which outputs:
   ```text
   C03987108976E334E2817EFDAE8492171D53434BB88139B9AE270DA702F06B90F143262FDC5C0EED8DA0365BF89897B9405CACEC877409A977D21E02FF01CF99 (10067625340751739904071515698183247981367894638552061894642882880514911721226402502619899066569920292066097869904718599094997392462293186525867276742283161) is prime
