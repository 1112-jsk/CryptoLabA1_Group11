from collections import Counter
import os
import string

def analyze_file(filename):
    filepath = os.path.join('datasets', filename)

    if not os.path.exists(filepath):
        print('File not found!')
        return

    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    char_count = len(content)
    word_count = len(content.split())
    line_count = len(content.splitlines())
    unique_characters = len(set(content))

    letters = [ch.lower() for ch in content if ch.isalpha()]
    frequency = Counter(letters)

    print('\n===== File Analysis =====')
    print(f'File: {filename}')
    print(f'Characters       : {char_count}')
    print(f'Words            : {word_count}')
    print(f'Lines            : {line_count}')
    print(f'Unique Characters: {unique_characters}')

    print('\nLetter Frequency:')
    for letter in string.ascii_lowercase:
        print(f'{letter.upper()} : {frequency.get(letter, 0)}')