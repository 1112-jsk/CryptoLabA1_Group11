from shift_cipher import decrypt


def load_dictionary(filename):
    words = set()

    with open(filename, "r") as file:
        for line in file:
            word = line.strip().lower()

            if word:
                words.add(word)

    return words


def score_text(text, dictionary):
    words = text.lower().split()
    score = 0

    for word in words:
        word = word.strip(".,!?;:\"'()")

        if word in dictionary:
            score += 1

    return score


def brute_force_attack(ciphertext, dictionary):
    best_key = 0
    best_score = -1
    best_plaintext = ""

    for key in range(26):
        plaintext = decrypt(ciphertext, key)
        score = score_text(plaintext, dictionary)

        print(f"Key: {key:2} | Score: {score:2} | {plaintext}")

        if score > best_score:
            best_score = score
            best_key = key
            best_plaintext = plaintext

    return best_key, best_plaintext, best_score
