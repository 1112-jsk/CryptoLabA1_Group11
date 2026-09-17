from shift_cipher import encrypt
from brute_force_dictionary import load_dictionary, brute_force_attack
from chi_square_attack import chi_square_attack
import os


# Find the project directory
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dictionary_file = os.path.join(
    base_dir,
    "dictionary",
    "english_words.txt"
)

ciphertext = "vkliw flskhu lv kljkob yxoqhudeoh wr dxwrpdwhg fubswdqdobvlv ehfdxvh lwv nhb vsdfh lv hafhswlrqdoob vpdoo"
dictionary = load_dictionary(dictionary_file)


# Test cases
test_cases = [
    {
        "name": "Test 1 - Short",
        "plaintext": "HELLO WORLD",
        "key": 3
    },

    {
        "name": "Test 2 - Medium",
        "plaintext": "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG",
        "key": 7
    },

    {
        "name": "Test 3 - Long",
        "plaintext": (
            "CRYPTOGRAPHY IS THE STUDY OF TECHNIQUES USED TO PROTECT "
            "INFORMATION FROM UNAUTHORIZED ACCESS. CLASSICAL CIPHERS "
            "ARE USEFUL FOR LEARNING THE BASIC PRINCIPLES OF ENCRYPTION "
            "AND CRYPTANALYSIS."
        ),
        "key": 12
    },

    {
        "name": "Test 4 - Different Key",
        "plaintext": (
            "THE PURPOSE OF CRYPTOGRAPHY IS TO PROVIDE CONFIDENTIALITY "
            "INTEGRITY AUTHENTICATION AND SECURITY FOR INFORMATION."
        ),
        "key": 17
    },

    {
        "name": "Test 5 - Very Short",
        "plaintext": "HELLO",
        "key": 22
    }
]


for test in test_cases:

    name = test["name"]
    plaintext = test["plaintext"]
    actual_key = test["key"]

    ciphertext = encrypt(plaintext, actual_key)

    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)

    print("Actual Key :", actual_key)
    print("Plaintext  :", plaintext)
    print("Ciphertext :", ciphertext)

    # Dictionary attack
    dictionary_key, dictionary_plaintext, dictionary_score = \
        brute_force_attack(ciphertext, dictionary)

    print("\nDictionary Attack")
    print("Predicted Key :", dictionary_key)
    print("Plaintext     :", dictionary_plaintext)
    print("Score         :", dictionary_score)

    # Chi-Square attack
    chi_key, chi_plaintext, chi_score = \
        chi_square_attack(ciphertext)

    print("\nChi-Square Attack")
    print("Predicted Key :", chi_key)
    print("Plaintext     :", chi_plaintext)
    print("Score         :", chi_score)

    # Correctness
    print("\nResults")
    print(
        "Dictionary Correct? ",
        dictionary_key == actual_key
    )

    print(
        "Chi-Square Correct? ",
        chi_key == actual_key
    )
