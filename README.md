# CryptoLabA1_Group11

A modular cryptography and cryptanalysis toolkit developed as part of the **Cryptography Laboratory Course**. The project is designed to gradually evolve into a complete framework for implementing classical ciphers, cryptanalysis attacks, mathematical utilities, and text analysis tools.

## Team members

| Name                | Role                                                                   |
| ------------------- | ---------------------------------------------------------------------- |
| Krishna             | File analysis module (Task 4), datasets (Task 6), documentation        |
| Japneet Singh Kohli | Command-line interface (Task 3), logging (Task 5), project integration |

## Project objectives

* Build a reusable cryptography toolkit.
* Maintain a modular software architecture.
* Use Git and GitHub for collaborative development.
* Prepare a foundation for future encryption, decryption, attack, and analysis modules.

## Project structure

```text
CryptoLabA1_Group11/
├── classical/
├── attacks/
├── math/
├── modern/
├── analysis/
│   └── file_analysis.py
├── datasets/
│   ├── sample1.txt
│   ├── sample2.txt
│   ├── sample3.txt
│   ├── sample4.txt
│   └── sample5.txt
├── outputs/
├── docs/
├── tests/
├── utils/
├── main.py
├── README.md
└── requirements.txt
```

## Features implemented in week 1

### Project setup

* Organized modular directory structure.
* Git repository initialization.
* GitHub version control workflow.

### File analysis module

The `analysis/file_analysis.py` module reads text files from the `datasets` folder and displays:

* Number of characters
* Number of words
* Number of lines
* Number of unique characters
* Letter frequency distribution (A–Z)

### Dataset collection

Five sample text files have been included for future cryptography experiments such as:

* Caesar cipher
* Vigenère cipher
* Playfair cipher
* Hill cipher
* Frequency analysis
* Cryptanalysis attacks

## Sample output

```text
===== File Analysis =====
File: sample1.txt
Characters       : 156
Words            : 23
Lines            : 2
Unique Characters: 28

Letter Frequency:
A : 12
B : 1
C : 8
...
Z : 0
```

## Future modules

The toolkit will be expanded in future assignments with:

* Classical encryption algorithms
* Decryption modules
* Frequency analysis attacks
* Dictionary attacks
* Statistical cryptanalysis
* Modular arithmetic utilities
* Matrix operations
* Cipher comparison and analysis tools

## Technologies used

* Python 3
* Git
* GitHub

## How to run

Clone the repository:

```bash
git clone https://github.com/1112-jsk/CryptoLabA1_Group11.git
cd CryptoLabA1_Group11
```

Run the file analysis module:

```bash
python3 analysis/file_analysis.py
```

Enter a filename from the `datasets` folder when prompted.

## Version control

Development is carried out using Git feature branches and pull requests to ensure collaborative and organized project development.

## Conclusion

Week 1 establishes the foundation of CryptoLabA1_Group11 through project organization, modular design, dataset preparation, and text analysis functionality. The repository is now ready for implementing cryptographic algorithms and cryptanalysis techniques in future laboratory assignments.
