import os

from brute_force_dictionary import load_dictionary, brute_force_attack
from chi_square_attack import chi_square_attack


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dictionary_file = os.path.join(
    base_dir,
    "dictionary",
    "english_words.txt"
)

ciphertext = "KHOOR ZRUOG"

dictionary = load_dictionary(dictionary_file)

dictionary_key, dictionary_plaintext, dictionary_score = \
    brute_force_attack(ciphertext, dictionary)

print("\nDictionary Result")
print("Predicted Key :", dictionary_key)
print("Plaintext     :", dictionary_plaintext)
print("Score         :", dictionary_score)


chi_key, chi_plaintext, chi_score = \
    chi_square_attack(ciphertext)

print("\nChi-Square Result")
print("Predicted Key :", chi_key)
print("Plaintext     :", chi_plaintext)
print("Score         :", chi_score)
