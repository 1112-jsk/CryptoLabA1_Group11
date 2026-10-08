# CryptoLabX

Originally built as a C++ cryptography lab for studying encryption algorithms and cryptanalysis, this project was expanded for the Secure Applications assignment. It now includes a console-based C++ ATM simulator designed to highlight both core banking features and intentional security flaws. To evaluate these vulnerabilities, the source code was scanned using Flawfinder for Static Application Security Testing (SAST).

# Group Number
11

#Group Members
Japneet Singh Kohli
Krishna Devanshu

## Part 1 — Cryptography Laboratory

### Cryptography Features
The original cryptography laboratory project includes modules designed for learning and breaking classical encryption schemes. Key features developed in this module include:

**Cryptanalysis & Attacks**
* **Monoalphabetic Substitution Cipher Analysis:** Includes interactive tools for letter frequency analysis, word frequency analysis, and isomorphic pattern analysis.
* **Shift Cipher Cryptanalysis:** Features automated cracking using Brute Force, Dictionary Scoring (cross-referencing an `english_words.txt` vocabulary), and Chi-Square statistical analysis.

**Cryptographic Modules**
The repository is organized into distinct categories for future expansion:
* Classical Cryptography
* Modern Cryptography
* Cryptanalysis / Attacks
* Text Analysis

### Project Structure (Part 1)

```text

CryptoLabX/
│
├── analysis/
│   └── text_analysis.cpp
│
├── attacks/
│
├── classical/
│
├── modern/
│
├── math/
│
├── utils/
│   ├── logger.cpp
│   ├── logger.h
│   └── logs.txt
│
├── datasets/
│   ├── sample_text1.txt
│   ├── sample_text2.txt
│   ├── sample_text3.txt
│   ├── sample_text4.txt
│   └── sample_text5.txt
│
├── outputs/
│
├── tests/
│
├── docs/
│
├── main.cpp
├── README.md
└── requirements.txt
```

### Compilation
```
g++ main.cpp utils/logger.cpp analysis/text_analysis.cpp -o CryptoLabX
```

## Part 2 — Secure Applications (ATM System)

### ATM Application
For the Secure Applications assignment, CryptoLabX was extended with a console-based ATM System. The application was designed according to the assigned application prompt: **Application 1 — ATM System**.

The objective of this module is to implement core banking functionalities to demonstrate C++ application security concepts, specifically focusing on how insecure coding practices can compromise software, rather than developing a complete commercial banking product.

### Core Functionalities
1. **Login:** Users authenticate using a 4-digit PIN.
2. **Balance Inquiry:** Users can view their current account balance.
3. **Withdraw Funds:** Users can withdraw money, provided they have sufficient funds.
4. **Deposit Funds (Fast Deposit):** Users can add money to their account balance.
5. **Change PIN:** Users can update their authentication PIN.

### Security Vulnerabilities
To demonstrate real-world coding flaws and test our SAST tool, the following three vulnerabilities were intentionally embedded into the application:

1. **Hardcoded Credentials:**
   * *Description:* The default authentication PIN (e.g., `"1234"`) is stored directly in the source code as a global plaintext character array. Anyone with access to the source code or binary can extract the secret key.
2. **Improper Input Validation (Buffer Overflow):**
   * *Description:* The application uses unsafe C-style string functions like `strcpy()` to handle user input during login. Because these functions do not check buffer boundaries, inputting a string longer than the allocated array size will cause a buffer overflow, corrupting adjacent memory.
3. **Missing Authentication Checks:**
   * *Description:* While most functions verify if the user is authenticated, the "Deposit" function intentionally omits the session check (`if (!logged_in)`). This allows an unauthenticated user to bypass the login screen and manipulate the account balance directly.

### Technology Stack
* **Language:** C++
* **Standard:** C++11 or later
* **Compiler:** GCC (g++)
* **SAST Tool:** Flawfinder
* **Development Environment:** Visual Studio Code

### Secure Application Project Structure
```text
CryptoLabX/
├── secure_application/
│   ├── src/
│   │   └── atm_system.cpp
│   ├── reports/
│   │   └── sast_lab_log.txt
│   ├── outputs/
│   │   └── atm_system.exe
│   └── screenshots/
└── ...
