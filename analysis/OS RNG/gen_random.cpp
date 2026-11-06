#include <fstream>
#include <vector>
#include <cstdlib>
#include <iostream>
#include <windows.h>
#include <bcrypt.h>

const size_t N = 1024 * 1024;

void save(const char* name, const std::vector<unsigned char>& buf) {
    std::ofstream out(name, std::ios::binary);
    if (!out) {
        std::cout << "Could not write " << name << "\n";
        return;
    }
    out.write((const char*)buf.data(), buf.size());
    std::cout << "Wrote " << name << " (" << buf.size() << " bytes)\n";
}

int main() {
    std::system("if not exist data mkdir data");

    std::vector<unsigned char> buf(N);
    if (BCryptGenRandom(NULL, buf.data(), (ULONG)N, BCRYPT_USE_SYSTEM_PREFERRED_RNG) < 0) {
        std::cout << "BCryptGenRandom failed\n";
        return 1;
    }
    save("data/windows_cng.bin", buf);
    std::system("openssl rand -out data/openssl_rand.bin 1048576");
    return 0;
}