def clean_ciphertext(ciphertext):
    return ''.join(c for c in ciphertext.upper() if c.isalpha())


ciphertext = open("classical/vigenere/ciphertext.txt").read()

cleaned = clean_ciphertext(ciphertext)

print(cleaned)
print("Length:", len(cleaned))

def find_repeated_patterns(ciphertext, min_length=3, max_length=5):
    patterns = {}

    for length in range(min_length, max_length + 1):
        for i in range(len(ciphertext) - length + 1):
            pattern = ciphertext[i:i + length]
            patterns.setdefault(pattern, []).append(i)

    repeated = {}

    for pattern, positions in patterns.items():
        if len(positions) > 1:
            repeated[pattern] = positions

    return repeated
repeated = find_repeated_patterns(cleaned)

for pattern, positions in repeated.items():
    print(pattern, positions)
def calculate_distances(pattern_positions):
    distances = {}

    for pattern, positions in pattern_positions.items():
        curr = []

        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                curr.append(positions[j] - positions[i])

        if curr:
            distances[pattern] = curr

    return distances
distances = calculate_distances(repeated)

for pattern, values in distances.items():
    print(pattern, values)
def find_factors(distances):
    factor_count = {}

    for values in distances.values():
        for distance in values:
            for i in range(2, distance + 1):
                if distance % i == 0:
                    factor_count[i] = factor_count.get(i, 0) + 1

    return factor_count
factors = find_factors(distances)

for factor, count in sorted(factors.items(), key=lambda x: (-x[1], x[0])):
    print(factor, count)
def kasiski_analysis(ciphertext):
    repeated = find_repeated_patterns(ciphertext)
    distances = calculate_distances(repeated)
    factors = find_factors(distances)

    return repeated, distances, factors
ciphertext = open("classical/vigenere/ciphertext.txt").read()
cleaned = clean_ciphertext(ciphertext)

repeated, distances, factors = kasiski_analysis(cleaned)

print("Repeated patterns:")
for pattern, positions in repeated.items():
    print(pattern, positions)

print("\nDistances:")
for pattern, values in distances.items():
    print(pattern, values)

print("\nFactor frequencies:")
for factor, count in sorted(factors.items(), key=lambda x: (-x[1], x[0])):
    print(factor, count)
def calculate_ic(text):
    n = len(text)

    if n <= 1:
        return 0

    freq = [0] * 26

    for c in text:
        freq[ord(c) - ord('A')] += 1

    total = 0

    for f in freq:
        total += f * (f - 1)

    return total / (n * (n - 1))
def split_into_groups(ciphertext, key_length):
    groups = ['' for _ in range(key_length)]

    for i, c in enumerate(ciphertext):
        groups[i % key_length] += c

    return groups
candidates = sorted(factors, key=lambda x: factors[x], reverse=True)[:10]

print("\nIC analysis:")

for key_length in candidates:
    groups = split_into_groups(cleaned, key_length)

    values = []

    for group in groups:
        values.append(calculate_ic(group))

    average_ic = sum(values) / len(values)

    print(key_length, average_ic)
def frequency_analysis(groups):
    result = []

    for group in groups:
        freq = [0] * 26

        for c in group:
            freq[ord(c) - ord('A')] += 1

        result.append(freq)

    return result
key_length = candidates[0]

groups = split_into_groups(cleaned, key_length)
frequencies = frequency_analysis(groups)

print("\nFrequency tables:")

for i, freq in enumerate(frequencies):
    print("Group", i + 1)

    for j in range(26):
        print(chr(ord('A') + j), freq[j], end="  ")

    print()

def find_shift(group):
    english = [
        0.082, 0.015, 0.028, 0.043, 0.127, 0.022, 0.020,
        0.061, 0.070, 0.0015, 0.0077, 0.040, 0.024, 0.067,
        0.075, 0.019, 0.00095, 0.060, 0.063, 0.091, 0.028,
        0.0098, 0.024, 0.0015, 0.020, 0.00074
    ]

    n = len(group)
    best_shift = 0
    best_score = float('inf')

    for shift in range(26):
        freq = [0] * 26

        for c in group:
            x = (ord(c) - ord('A') - shift) % 26
            freq[x] += 1

        score = 0

        for i in range(26):
            expected = n * english[i]

            if expected > 0:
                score += (freq[i] - expected) ** 2 / expected

        if score < best_score:
            best_score = score
            best_shift = shift

    return best_shift
print("\nShifts:")

for i, group in enumerate(groups):
    shift = find_shift(group)
    print("Group", i + 1, "shift:", shift)
def find_key(groups):
    key = ""

    for group in groups:
        shift = find_shift(group)
        key += chr(ord('A') + shift)

    return key
key = find_key(groups)

print("\nRecovered key:", key)
def vigenere_decrypt(ciphertext, key):
    plaintext = ""

    for i, c in enumerate(ciphertext):
        c_value = ord(c) - ord('A')
        k_value = ord(key[i % len(key)]) - ord('A')

        p_value = (c_value - k_value) % 26

        plaintext += chr(ord('A') + p_value)

    return plaintext
plaintext = vigenere_decrypt(cleaned, key)

print("\nRecovered plaintext:")
print(plaintext)

def vigenere_encrypt(plaintext, key):
    ciphertext = ""

    for i, c in enumerate(plaintext):
        p_value = ord(c) - ord('A')
        k_value = ord(key[i % len(key)]) - ord('A')

        c_value = (p_value + k_value) % 26

        ciphertext += chr(ord('A') + c_value)

    return ciphertext
def verify(ciphertext, plaintext, key):
    encrypted = vigenere_encrypt(plaintext, key)
    return encrypted == ciphertext
encrypted = vigenere_encrypt(plaintext, key)

print("\nVerification:", verify(cleaned, plaintext, key))
candidates = sorted(factors, key=lambda x: factors[x], reverse=True)[:10]

key_length = candidates[0]
def select_key_length(ciphertext, factors):
    candidates = sorted(factors, key=lambda x: factors[x], reverse=True)[:10]

    results = []

    for key_length in candidates:
        if key_length <= 1 or key_length > len(ciphertext):
            continue

        groups = split_into_groups(ciphertext, key_length)

        ics = []

        for group in groups:
            ics.append(calculate_ic(group))

        average_ic = sum(ics) / len(ics)

        results.append((key_length, average_ic))

    results.sort(key=lambda x: x[1], reverse=True)

    return results
ic_results = select_key_length(cleaned, factors)

print("\nCandidate key lengths:")

for key_length, ic in ic_results:
    print("Key length:", key_length, "Average IC:", ic)
key_length = ic_results[0][0]
groups = split_into_groups(cleaned, key_length)
frequencies = frequency_analysis(groups)
key = find_key(groups)
ciphertext = open("classical/vigenere/ciphertext.txt").read()

cleaned = clean_ciphertext(ciphertext)

repeated, distances, factors = kasiski_analysis(cleaned)

ic_results = select_key_length(cleaned, factors)

key_length = ic_results[0][0]

groups = split_into_groups(cleaned, key_length)

frequencies = frequency_analysis(groups)

key = find_key(groups)

plaintext = vigenere_decrypt(cleaned, key)

print("Estimated key length:", key_length)
print("Recovered key:", key)
print("Recovered plaintext:", plaintext)
print("Verification:", verify(cleaned, plaintext, key))

def print_frequency_tables(frequencies):
    for i, freq in enumerate(frequencies):
        print("\nGroup", i + 1)

        for j in range(26):
            print(chr(ord('A') + j), freq[j], end="  ")

        print()
ciphertext = open("classical/vigenere/ciphertext.txt").read()

cleaned = clean_ciphertext(ciphertext)

repeated, distances, factors = kasiski_analysis(cleaned)

ic_results = select_key_length(cleaned, factors)

key_length = ic_results[0][0]

groups = split_into_groups(cleaned, key_length)

frequencies = frequency_analysis(groups)

key = find_key(groups)

plaintext = vigenere_decrypt(cleaned, key)

print("========== VIGENERE CRYPTANALYSIS ==========")

print("\nEstimated key length:", key_length)

print("\n========== FREQUENCY TABLES ==========")
print_frequency_tables(frequencies)

print("\n========== RECOVERED KEY ==========")
print(key)

print("\n========== RECOVERED PLAINTEXT ==========")
print(plaintext)

print("\n========== VERIFICATION ==========")
print("Verification:", verify(cleaned, plaintext, key))
ic_results = select_key_length(cleaned, factors)
print("\n========== KASISKI ANALYSIS ==========")

for factor, count in sorted(factors.items(), key=lambda x: (-x[1], x[0]))[:10]:
    print("Factor:", factor, "Frequency:", count)

print("\n========== IC ANALYSIS ==========")

for key_length, ic in ic_results:
    print("Key length:", key_length, "Average IC:", ic)
print(plaintext)
for i in range(0, len(plaintext), 80):
    print(plaintext[i:i + 80])

