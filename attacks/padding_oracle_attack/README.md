# Crypto Lab 11 — Assignment 7
## AES-CBC Padding Oracle Attack

### 1. Overview

This project demonstrates a Padding Oracle Attack against AES-CBC encrypted messages using Python and the PyCryptodome library.

The attack recovers plaintext without directly accessing the AES encryption key. It exploits a padding oracle that indicates whether decrypted ciphertext contains valid PKCS#7 padding.

### 2. Objectives

- Understand AES-CBC encryption.
- Understand PKCS#7 padding.
- Implement a padding oracle attack without using a ready-made attack library.
- Modify the previous ciphertext block to recover plaintext bytes.
- Recover the complete plaintext.
- Measure the total number of oracle queries.
- Understand how padding oracle vulnerabilities can be prevented.

### 3. Technologies Used

- **Programming Language:** Python
- **Cryptographic Library:** PyCryptodome
- **Encryption Algorithm:** AES-128
- **Encryption Mode:** CBC
- **Padding Scheme:** PKCS#7

### 4. Project Structure

Crypto-Lab-11-Assignment-7/ │ ├── paddingoracleattack.py └── README.md


### 5. Requirements

- Python 3.x
- PyCryptodome

Install the required dependency:

pip install pycryptodome


### 6. How to Run

**Step 1:** Save the Python implementation as:

paddingoracleattack.py


**Step 2:** Open a terminal in the project directory.

**Step 3:** Execute the program:

python paddingoracleattack.py


**Step 4:** Enter a plaintext message when prompted.

Example:

Enter plaintext: Hello Cryptography


The program encrypts the message, simulates a padding oracle, and performs the attack.

### 7. How the Attack Works

The attack uses the mathematical properties of CBC decryption.

For a ciphertext block, CBC decryption is defined as:

P[i] = D(K, C[i]) XOR C[i-1]


Where:

- `P[i]` is the plaintext block.
- `C[i]` is the current ciphertext block.
- `C[i-1]` is the previous ciphertext block or IV.
- `D(K, C[i])` is AES decryption using key `K`.
- `XOR` represents the exclusive OR operation.

The attack follows these steps:

1. Select a ciphertext block to recover.
2. Modify the preceding ciphertext block.
3. Submit the modified ciphertext to the padding oracle.
4. Observe whether the resulting plaintext has valid PKCS#7 padding.
5. Recover plaintext bytes from right to left.
6. Repeat the process for every ciphertext block.
7. Remove the final padding to obtain the original plaintext.

The attack function does not access the AES key. The key is used only by the simulated encryption and oracle functions.

### 8. Oracle Query Count

The program maintains a counter that records the number of oracle calls.

The counter is displayed at the end of execution:

Total oracle queries: <actual_count>


Each AES block contains 16 bytes. The attack may test up to 256 candidate values for each byte.

The basic upper bound for candidate testing is:

16 × 256 = 4096 queries per block


Additional verification queries may be required.

The actual query count depends on the plaintext length, candidate search order, and oracle responses.

Record the actual value printed by the program when documenting the experiment.

### 9. Expected Output

The program displays results in the following format:

Encryption completed. Ciphertext (hex): <generatedciphertext> IV (hex): <generatediv>

Attacking padding oracle...

--- RESULTS --- Original plaintext : <yourinput> Recovered plaintext: <recoveredplaintext> Total oracle queries: <actual_count> Verification: SUCCESS


The ciphertext, IV, and query count vary between executions.

The recovered plaintext should match the original input.

### 10. Security Recommendations

Padding oracle vulnerabilities can be prevented or mitigated through the following practices:

- **Use authenticated encryption:** Prefer AES-GCM or ChaCha20-Poly1305.
- **Verify authentication:** Validate the authentication tag before releasing decrypted plaintext.
- **Avoid distinguishable errors:** Do not expose different responses for padding failures and other decryption errors.
- **Authenticate ciphertext:** If CBC must be retained, use a correctly implemented Encrypt-then-MAC construction and verify the MAC before decryption.
- **Use established libraries:** Avoid designing custom cryptographic protocols.
- **Perform security testing:** Test malformed ciphertext and error-handling behavior.

### 11. Limitations

This project uses a simulated padding oracle in a controlled educational environment.

The demonstration illustrates the vulnerability but does not automatically imply that every AES-CBC implementation is vulnerable.

A practical attack requires access to an oracle whose responses reveal useful information about padding validity.

The program also generates its own encryption key and ciphertext for each execution.

### 12. Conclusion

This project demonstrates that plaintext can be recovered from AES-CBC ciphertext without directly knowing the encryption key when a padding oracle vulnerability exists.

By modifying the preceding ciphertext block and analyzing the oracle's responses, the attack recovers plaintext one byte at a time.

The experiment highlights the importance of authenticated encryption, ciphertext integrity, and secure error handling.

### 13. References

1. NIST FIPS 197 — Advanced Encryption Standard (AES).
2. NIST SP 800-38A — Recommendation for Block Cipher Modes of Operation.
3. RFC 5652 — Cryptographic Message Syntax.
4. PyCryptodome Documentation: https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html

---

**Assignment:** Crypto Lab 11 — Assignment 7  
**Topic:** AES-CBC Padding Oracle Attack  
**Language:** Python

Save it as README.md
