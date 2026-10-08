from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

BLOCK_SIZE = 16
queries = 0

# The secret key is generated here
key = get_random_bytes(16)


# ORACLE & HELPER FUNCTIONS

def valid_padding(data):
    """Checks if the PKCS#7 padding is mathematically valid."""
    if len(data) == 0 or len(data) % BLOCK_SIZE != 0:
        return False
    
    n = data[-1]
    if n < 1 or n > BLOCK_SIZE:
        return False
        
    if data[-n:] != bytes([n]) * n:
        return False
        
    return True


def decrypt_data(iv, cipher_text):
    """Internal decryption used only by the oracle."""
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.decrypt(cipher_text)


def oracle(data):
    """Simulates the padding oracle. Returns True if padding is valid."""
    global queries
    queries += 1
    
    iv = data[:BLOCK_SIZE]
    cipher_text = data[BLOCK_SIZE:]
    
    plain_text = decrypt_data(iv, cipher_text)
    return valid_padding(plain_text)


def pad(data):
    """Applies PKCS#7 padding."""
    n = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([n]) * n


def unpad(data):
    """Removes PKCS#7 padding."""
    n = data[-1]
    if n < 1 or n > BLOCK_SIZE or data[-n:] != bytes([n]) * n:
        raise Exception("Invalid padding")
    return data[:-n]


# THE ATTACK IMPLEMENTATION

def decrypt_block(prev, curr):
    """Recovers a 16-byte plaintext block from right to left."""
    intermediate = [0] * BLOCK_SIZE
    plain = [0] * BLOCK_SIZE

    for pos in range(BLOCK_SIZE - 1, -1, -1):
        padding_val = BLOCK_SIZE - pos
        
        modified = bytearray(prev)

        # Set known bytes to the current padding value
        for j in range(pos + 1, BLOCK_SIZE):
            modified[j] = intermediate[j] ^ padding_val

        found = False

        # Try every possible value for the target byte
        for guess in range(256):
            modified[pos] = guess
            test = bytes(modified) + curr

            if not oracle(test):
                continue

            # Handle the false positive edge case on the very first byte
            if pos == BLOCK_SIZE - 1:
                check = bytearray(modified)
                check[pos - 1] ^= 1 
                test2 = bytes(check) + curr
                if not oracle(test2):
                    continue

            # correct guess
            intermediate[pos] = guess ^ padding_val
            plain[pos] = intermediate[pos] ^ prev[pos]
            found = True
            break

        if not found:
            raise Exception(f"Could not recover byte at position {pos}")

    return bytes(plain)

if __name__ == "__main__":
    message = input("Enter plaintext: ").encode()
    iv = get_random_bytes(BLOCK_SIZE)
    padded = pad(message)
    
    # Encrypt
    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(padded)

    # Split ciphertext into 16-byte chunks
    blocks = [cipher_text[i:i + BLOCK_SIZE] for i in range(0, len(cipher_text), BLOCK_SIZE)]

    # Recover every plaintext block
    plain_text = b""
    prev = iv

    print("\n[*] Attacking Oracle...")
    
    for curr in blocks:
        block = decrypt_block(prev, curr)
        plain_text += block
        prev = curr

    # Remove the final padding
    plain_text = unpad(plain_text)

    print("\n--- RESULTS ---")
    print("Original plaintext :", message.decode())
    print("Recovered plaintext:", plain_text.decode())
    print("Total oracle queries:", queries)