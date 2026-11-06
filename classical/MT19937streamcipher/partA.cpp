#include <iostream>
#include <string>
#include <random>
#include <ctime>
#include <cstdio>
using namespace std;

string crypt(const string& data, unsigned int seed) {
    mt19937 gen(seed);
    string out;
    for (char c : data) out += (char)(c ^ (gen() & 0xFF));
    return out;
}

string toHex(const string& s) {
    string h;
    char buf[3];
    for (unsigned char c : s) {
        sprintf(buf, "%02x", c);
        h += buf;
    }
    return h;
}

int main() {
    // Steps 1-2: encrypt and decrypt a test message
    string msg = "Hello MT19937";
    string enc = crypt(msg, 1234);
    string dec = crypt(enc, 1234);
    cout << "Test message : " << msg << "\n";
    cout << "Ciphertext   : " << toHex(enc) << "\n";
    cout << "Decrypted    : " << dec << (dec == msg ? "  (OK)" : "  (FAILED)") << "\n\n";

    // Step 3: random prefix + 14 'A' + random 16-bit seed
    mt19937 rng(random_device{}() ^ (unsigned int)time(0));
    int prefixLen = 5 + rng() % 16;
    string plain;
    for (int i = 0; i < prefixLen; i++) plain += (char)(33 + rng() % 94);
    plain += string(14, 'A');
    unsigned int secretSeed = rng() % 65536;
    string cipher = crypt(plain, secretSeed);

    cout << "Plaintext    : " << plain << "\n";
    cout << "Secret seed  : " << secretSeed << "\n";
    cout << "Ciphertext   : " << toHex(cipher) << "\n\n";

    // Step 4: brute force all 65536 seeds using only the ciphertext
    int tested = 0;
    unsigned int foundSeed = 0;
    int foundPos = -1;
    for (unsigned int s = 0; s < 65536; s++) {
        tested++;
        string ks = crypt(string(cipher.size(), '\0'), s);
        for (size_t pos = 0; pos + 14 <= cipher.size(); pos++) {
            bool ok = true;
            for (int i = 0; i < 14 && ok; i++)
                if (((unsigned char)cipher[pos + i] ^ (unsigned char)ks[pos + i]) != 'A') ok = false;
            if (ok) {
                foundSeed = s;
                foundPos = pos;
            }
        }
    }
    cout << "Seeds tested     : " << tested << "\n";
    if (foundPos < 0) {
        cout << "No seed found\n";
        return 1;
    }
    cout << "Recovered seed   : " << foundSeed << "\n";
    cout << "'A' block starts : position " << foundPos << "\n";

    // Step 5: verify
    string recovered = crypt(cipher, foundSeed);
    cout << "Recovered text   : " << recovered << "\n";
    cout << "Seed matches     : " << (foundSeed == secretSeed ? "YES" : "NO") << "\n";
    cout << "Text matches     : " << (recovered == plain ? "YES" : "NO") << "\n";
    cout << "Contains 14 A's  : " << (recovered.find(string(14, 'A')) != string::npos ? "YES" : "NO") << "\n";
    return 0;
}