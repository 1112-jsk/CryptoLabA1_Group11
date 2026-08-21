from collections import Counter
from shift_cipher import decrypt


# Expected frequencies of A-Z in English
ENGLISH_FREQUENCIES = [
    0.0812,  # A
    0.0149,  # B
    0.0271,  # C
    0.0432,  # D
    0.1202,  # E
    0.0230,  # F
    0.0203,  # G
    0.0592,  # H
    0.0731,  # I
    0.0010,  # J
    0.0069,  # K
    0.0398,  # L
    0.0261,  # M
    0.0695,  # N
    0.0768,  # O
    0.0182,  # P
    0.0011,  # Q
    0.0602,  # R
    0.0628,  # S
    0.0910,  # T
    0.0288,  # U
    0.0111,  # V
    0.0209,  # W
    0.0017,  # X
    0.0211,  # Y
    0.0007   # Z
]


def calculate_chi_square(text):
    letters = [
        char.lower()
        for char in text
        if char.isalpha()
    ]

    total = len(letters)

    if total == 0:
        return float("inf")

    counts = Counter(letters)

    chi_square = 0

    for i in range(26):
        letter = chr(ord('a') + i)

        observed = counts.get(letter, 0)
        expected = ENGLISH_FREQUENCIES[i] * total

        chi_square += (observed - expected) ** 2 / expected

    return chi_square


def chi_square_attack(ciphertext):
    best_key = 0
    best_score = float("inf")
    best_plaintext = ""

    for key in range(26):
        plaintext = decrypt(ciphertext, key)

        score = calculate_chi_square(plaintext)

        print(
            f"Key: {key:2} | "
            f"Chi-Square: {score:8.2f} | "
            f"{plaintext}"
        )

        if score < best_score:
            best_score = score
            best_key = key
            best_plaintext = plaintext

    return best_key, best_plaintext, best_score
