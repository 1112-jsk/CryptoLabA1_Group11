#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <iomanip>
using namespace std;

vector<unsigned char> readFile(const string& path) {
    ifstream in(path, ios::binary);
    return vector<unsigned char>((istreambuf_iterator<char>(in)), istreambuf_iterator<char>());
}

double pFromZ(double z) {
    return erfc(fabs(z) / sqrt(2.0));
}

double serialCorr(const vector<unsigned char>& d, int lag) {
    double n = d.size() - lag, sx = 0, sy = 0, sxy = 0, sxx = 0, syy = 0;
    for (size_t i = 0; i + lag < d.size(); i++) {
        double x = d[i], y = d[i + lag];
        sx += x; sy += y; sxy += x * y; sxx += x * x; syy += y * y;
    }
    return (n * sxy - sx * sy) / sqrt((n * sxx - sx * sx) * (n * syy - sy * sy));
}

double poissonUpper(int k, double lambda) {
    double term = exp(-lambda), cdf = 0;
    for (int i = 0; i < k; i++) {
        cdf += term;
        term *= lambda / (i + 1);
    }
    return max(0.0, 1.0 - cdf);
}

void analyze(const string& path) {
    vector<unsigned char> d = readFile(path);
    if (d.empty()) {
        cout << "Could not read " << path << "\n\n";
        return;
    }
    double n = d.size();
    cout << fixed << setprecision(4);
    cout << "=== " << path << " (" << d.size() << " bytes) ===\n";

    // 1. Byte frequency
    vector<long> count(256, 0);
    for (unsigned char b : d) count[b]++;
    double expected = n / 256, chi = 0, entropy = 0;
    for (int i = 0; i < 256; i++) {
        chi += (count[i] - expected) * (count[i] - expected) / expected;
        double p = count[i] / n;
        if (p > 0) entropy -= p * log2(p);
    }
    double df = 255;
    double z = (cbrt(chi / df) - (1 - 2 / (9 * df))) / sqrt(2 / (9 * df));
    double pChi = pFromZ(z);
    cout << "1. Byte frequency\n";
    cout << "   expected count per value : " << expected << "\n";
    cout << "   min / max count          : " << *min_element(count.begin(), count.end())
         << " / " << *max_element(count.begin(), count.end()) << "\n";
    cout << "   chi-square (255 d.f.)    : " << chi << "  p = " << pChi << "\n";
    cout << "   entropy                  : " << entropy << " bits per byte\n";
    cout << "   counts per group of 16 byte values (expected " << expected * 16 << "):\n   ";
    for (int g = 0; g < 16; g++) {
        long s = 0;
        for (int i = 0; i < 16; i++) s += count[g * 16 + i];
        cout << s << " ";
    }
    cout << "\n";

    // 2. Bit distribution
    double bits = n * 8, ones = 0, runs = 1;
    int prev = -1;
    for (unsigned char b : d) {
        for (int k = 7; k >= 0; k--) {
            int bit = (b >> k) & 1;
            ones += bit;
            if (prev != -1 && bit != prev) runs++;
            prev = bit;
        }
    }
    double pMono = pFromZ((2 * ones - bits) / sqrt(bits));
    double pi = ones / bits;
    double expRuns = 2 * bits * pi * (1 - pi);
    double pRuns = erfc(fabs(runs - expRuns) / (2 * sqrt(2 * bits) * pi * (1 - pi)));
    cout << "2. Bit distribution\n";
    cout << "   ones / zeros             : " << (long)ones << " / " << (long)(bits - ones)
         << "  (ones = " << pi * 100 << "%)\n";
    cout << "   monobit test p           : " << pMono << "\n";
    cout << "   runs observed / expected : " << (long)runs << " / " << (long)expRuns
         << "  p = " << pRuns << "\n";

    // 3. Repeated 4-byte patterns
    size_t m = d.size() / 4;
    vector<uint32_t> blocks(m);
    for (size_t i = 0; i < m; i++)
        blocks[i] = d[4 * i] | (d[4 * i + 1] << 8) | (d[4 * i + 2] << 16) | ((uint32_t)d[4 * i + 3] << 24);
    sort(blocks.begin(), blocks.end());
    int repeats = 0;
    for (size_t i = 1; i < m; i++)
        if (blocks[i] == blocks[i - 1]) repeats++;
    double lambda = (double)m * (m - 1) / 2 / 4294967296.0;
    double pRep = poissonUpper(repeats, lambda);
    cout << "3. Repeated patterns (4-byte blocks)\n";
    cout << "   repeats observed / expected : " << repeats << " / " << lambda << "  p = " << pRep << "\n";

    // 4. Serial correlation
    cout << "4. Serial correlation\n   ";
    for (int lag = 1; lag <= 5; lag++) cout << "lag " << lag << ": " << serialCorr(d, lag) << "   ";
    double r1 = serialCorr(d, 1);
    double pSer = pFromZ(r1 * sqrt(n - 1));
    cout << "\n   lag-1 p = " << pSer << "\n";

    bool pass = pChi >= 0.01 && pMono >= 0.01 && pRuns >= 0.01 && pRep >= 0.01 && pSer >= 0.01;
    cout << "Result: " << (pass ? "PASS (all p-values >= 0.01)" : "CHECK (some p-value < 0.01)") << "\n\n";
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cout << "Usage: analyze file1.bin file2.bin ...\n";
        return 1;
    }
    for (int i = 1; i < argc; i++) analyze(argv[i]);
    return 0;
}