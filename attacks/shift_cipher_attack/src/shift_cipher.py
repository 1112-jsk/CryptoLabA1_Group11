def encrypt(text, key):
    result = ""

    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + key) % 26 + base)
        else:
            result += char

    return result


def decrypt(text, key):
    return encrypt(text, -key)


if __name__ == "__main__":
    plaintext = "HELLO WORLD"
    key = 3

    ciphertext = encrypt(plaintext, key)
    decrypted = decrypt(ciphertext, key)

    print("Plaintext :", plaintext)
    print("Key       :", key)
    print("Ciphertext:", ciphertext)
    print("Decrypted :", decrypted)
