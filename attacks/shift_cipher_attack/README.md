# Assignment 4: Shift Cipher Cryptanalysis

## Project Details
* **Group:** 11
* **Group Members:** Japneet, Krishna

---

## Objective
This module performs automated cryptanalysis on Shift Cipher ciphertexts to recover both the encryption key and the underlying plaintext without prior key knowledge. Two distinct recovery techniques are implemented:

* **Brute Force with Dictionary Scoring**
* **Chi-Square ($\chi^2$) Frequency Analysis**

---

## Cryptographic Foundation
The Shift Cipher operates on a 26-letter alphabet space ($K \in \{0, 1, \dots, 25\}$).

* **Encryption:** $C = (P + K) \pmod{26}$
* **Decryption:** $P = (C - K + 26) \pmod{26}$

*Where $P$ represents the plaintext character position, $C$ represents the ciphertext character position, and $K$ represents the shift key.*

---

## Cryptanalysis Algorithms

### 1. Brute Force & Dictionary Scoring
This method systematically tests every possible key in the key space and evaluates the output against an English word list:

1. Decrypt the ciphertext using each key $K \in [0, 25]$.
2. Tokenize each candidate plaintext into individual words.
3. Cross-reference each word against a dictionary of valid English words.
4. Calculate a match score based on the count of recognized words.
5. Select the key corresponding to the **highest** dictionary score as the predicted key.

### 2. Chi-Square ($\chi^2$) Analysis
This technique measures how closely the letter distribution of a decrypted candidate matches standard English monograph frequencies:

1. Decrypt the ciphertext using each key $K \in [0, 25]$.
2. Compute the observed letter frequencies ($O$) for $A$–$Z$ in the candidate plaintext.
3. Determine expected letter frequencies ($E$) based on standard English statistical distributions.
4. Compute the Chi-Square statistic for each candidate key:

$$\chi^2 = \sum \frac{(O - E)^2}{E}$$

5. Select the key corresponding to the **lowest** $\chi^2$ score as the predicted key (indicating the smallest statistical deviation from standard English).

---

## File & Module Structure

```text
attacks/
└── shift_cipher/
    ├── dictionary_attack.py  # Dictionary scoring implementation
    ├── chisquare_attack.py   # Chi-Square frequency analyzer
    └── wordlist.txt          # Reference English dictionary
