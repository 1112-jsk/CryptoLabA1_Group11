#include <iostream>
#include <string>
#include <random>
#include <ctime>
#include <cstdio>
using namespace std;

string makeToken(unsigned int seed) {
    mt19937 gen(seed);
    string token;
    for (int i = 0; i < 16; i++) token += (char)(gen() & 0xFF);
    return token;
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
    // Token generation (simulated: token was issued 120 seconds ago)
    long observed = time(0);
    long T = observed - 120;
    string token = makeToken((unsigned int)T);
    cout << "Token generated at T : " << T << "\n";
    cout << "Token (hex)          : " << toHex(token) << "\n\n";

    // Token prediction: attacker knows only the token and the observation time
    cout << "Attacker observed the token at " << observed << "\n";
    cout << "Search interval      : " << observed - 300 << " to " << observed + 300 << "\n";

    int tested = 0;
    long recovered = -1;
    for (long t = observed - 300; t <= observed + 300; t++) {
        tested++;
        if (makeToken((unsigned int)t) == token) recovered = t;
    }
    cout << "Timestamps tested    : " << tested << "\n";
    if (recovered < 0) {
        cout << "No matching timestamp\n";
        return 1;
    }
    cout << "Matching timestamp   : " << recovered << "\n";

    string again = makeToken((unsigned int)recovered);
    cout << "Regenerated token    : " << toHex(again) << "\n";
    cout << "Token verified       : " << (again == token ? "YES" : "NO") << "\n";
    return 0;
}