#include <iostream>
#include <vector>
#include <fstream>
#include <algorithm>
#include <iomanip>
#include <map>
#include <string>
#include <cctype>

using namespace std;

string encrypt(const string& plaintext, const string& key) {
    string ciphertext = "";
    for (char c : plaintext) {
        if (isalpha(c)) {
            bool is_upper = isupper(c);
            char mapped_char = key[toupper(c) - 'A'];
            ciphertext += is_upper ? mapped_char : tolower(mapped_char);
        } else {
            ciphertext += c;
        }
    }
    return ciphertext;
}

// 1. frequency_analysis()
void frequency_analysis(const string& ciphertext) {
    vector<pair<char, int>> freq(26);
    for (int i = 0; i < 26; i++) {
        freq[i] = {'A' + i, 0};
    }

    int total_letters = 0;
    for (char c : ciphertext) {
        if (isalpha(c)) {
            freq[toupper(c) - 'A'].second++;
            total_letters++;
        }
    }

    sort(freq.begin(), freq.end(), [](const pair<char, int>& a, const pair<char, int>& b) {
        return a.second > b.second;
    });

    cout << "\n--- LETTER FREQUENCY ANALYSIS ---\n";
    for (int i = 0; i < 26; i++) {
        if (freq[i].second > 0) {
            double percentage = (freq[i].second * 100.0) / total_letters;
            cout << freq[i].first << " : " << setw(4) << freq[i].second 
                 << "  (" << fixed << setprecision(2) << percentage << "%)\n";
        }
    }

    cout << "\nTop 5 Most Frequent Letters:\n";
    for (int i = 0; i < 5 && freq[i].second > 0; i++) {
        cout << freq[i].first << " -> " << freq[i].second << " occurrences\n";
    }
}

// 2. word_frequency_analysis()
void word_frequency_analysis(const string& ciphertext) {
    map<string, int> word_counts;
    string current_word = "";

    for (char c : ciphertext) {
        if (isalpha(c)) {
            current_word += toupper(c);
        } else if (!current_word.empty()) {
            word_counts[current_word]++;
            current_word = "";
        }
    }
    if (!current_word.empty()) word_counts[current_word]++;

    cout << "\n--- WORD FREQUENCY ANALYSIS ---\n";

    for (int len = 1; len <= 3; len++) {
        cout << "\n" << len << "-letter words:\n";
        for (const auto& pair : word_counts) {
            if (pair.first.length() == len) {
                cout << pair.first << " -> " << pair.second << "\n";
            }
        }
    }

    cout << "\nRepeated words (length > 3):\n";
    for (const auto& pair : word_counts) {
        if (pair.first.length() > 3 && pair.second > 1) {
            cout << pair.first << " -> " << pair.second << "\n";
        }
    }
}

// Helper for pattern_analysis()
string get_pattern(const string& word) {
    map<char, char> char_map;
    char current_id = '0';
    string pattern = "";

    for (char c : word) {
        if (char_map.find(c) == char_map.end()) {
            char_map[c] = current_id++;
        }
        pattern += char_map[c];
    }
    return pattern;
}

// 3. pattern_analysis()
void pattern_analysis(const string& ciphertext) {
    map<string, vector<string>> pattern_groups;
    string current_word = "";

    for (char c : ciphertext) {
        if (isalpha(c)) {
            current_word += toupper(c);
        } else if (!current_word.empty()) {
            if (current_word.length() > 2) { 
                string pat = get_pattern(current_word);
                if (find(pattern_groups[pat].begin(), pattern_groups[pat].end(), current_word) == pattern_groups[pat].end()) {
                    pattern_groups[pat].push_back(current_word);
                }
            }
            current_word = "";
        }
    }

    cout << "\n--- PATTERN ANALYSIS ---\n";
    for (const auto& pair : pattern_groups) {
        if (pair.second.size() > 1) { 
            cout << "Pattern " << pair.first << " : ";
            for (size_t i = 0; i < pair.second.size(); i++) {
                cout << pair.second[i] << (i + 1 < pair.second.size() ? ", " : "");
            }
            cout << "\n";
        }
    }
}

// 4. apply_substitution()
string apply_substitution(const string& ciphertext, const string& current_key) {
    string partial = "";
    for (char c : ciphertext) {
        if (isalpha(c)) {
            int index = toupper(c) - 'A';
            char sub = current_key[index];
            
            if (sub != '?') {
                partial += isupper(c) ? toupper(sub) : tolower(sub);
            } else {
                partial += '_';
            }
        } else {
            partial += c;
        }
    }
    return partial;
}

// 5. display_partial_plaintext()
void display_partial_plaintext(const string& ciphertext, const string& current_key) {
    cout << "\n--- CURRENT PARTIAL PLAINTEXT ---\n";
    cout << apply_substitution(ciphertext, current_key) << "\n";
    cout << "---------------------------------\n";
}

// 6. verify_solution()
bool verify_solution(const string& original_plaintext, const string& recovered_ciphertext, const string& current_key) {
    string attempt = apply_substitution(recovered_ciphertext, current_key);
    
    string norm_plain = "", norm_attempt = "";
    for(char c : original_plaintext) if(isalpha(c)) norm_plain += toupper(c);
    for(char c : attempt) if(isalpha(c)) norm_attempt += toupper(c);

    if (norm_plain == norm_attempt && norm_attempt.find('_') == string::npos) {
        cout << "\n[SUCCESS] The recovered key is completely accurate!\n";
        return true;
    }
    cout << "\n[FAILED] The plaintext does not match perfectly or is incomplete.\n";
    return false;
}

int main() {
    // Secret encryption key
    const string SECRET_KEY = "QWERTYUIOPASDFGHJKLZXCVBNM";
    
    ifstream file("../input/plaintext.txt");
    if (!file) {
        cout << "Error: Unable to open plaintext.txt\n";
        cout << "Please ensure the file exists in the same directory as the executable.\n";
        return 1;
    }

    string plaintext = "", line;
    while (getline(file, line)) {
        plaintext += line + "\n";
    }
    file.close();

    string ciphertext = encrypt(plaintext, SECRET_KEY);
    string user_recovered_key = string(26, '?');

    cout << "\n      CRYPTANALYSIS INITIALIZED        ";
    
    cout << "\n--- CIPHERTEXT ---\n";
    cout << ciphertext << "\n";
    cout << "------------------\n";

    frequency_analysis(ciphertext);
    word_frequency_analysis(ciphertext);
    pattern_analysis(ciphertext);

    while (true) {
        cout << "\nOptions:\n";
        cout << " - Map a letter:   C P  (Cipher 'C' becomes Plain 'P')\n";
        cout << " - Unmap a letter: C ?  (Remove mapping for Cipher 'C')\n";
        cout << " - Type 'exit' to verify and quit.\n";
        cout << "Input: ";

        string input;
        getline(cin, input);

        if (input == "exit") break;

        if (input.length() >= 3) {
            char cipher_char = toupper(input[0]);
            char plain_char = toupper(input[2]);

            if (!isalpha(cipher_char)) {
                cout << "Invalid ciphertext character.\n";
                continue;
            }

            int index = cipher_char - 'A';

            if (plain_char == '?') {
                user_recovered_key[index] = '?';
                cout << "[Unmapped] " << cipher_char << " is now unknown.\n";
                display_partial_plaintext(ciphertext, user_recovered_key);
            } 
            else if (isalpha(plain_char)) {
                bool conflict = false;
                for (int i = 0; i < 26; i++) {
                    if (user_recovered_key[i] == plain_char && i != index) {
                        cout << "[Error] Plaintext letter '" << plain_char << "' is already mapped to Ciphertext letter '" << char('A' + i) << "'.\n";
                        conflict = true;
                        break;
                    }
                }
                
                if (!conflict) {
                    user_recovered_key[index] = plain_char;
                    cout << "[Mapped] " << cipher_char << " -> " << plain_char << "\n";
                    display_partial_plaintext(ciphertext, user_recovered_key);
                }
            } else {
                cout << "Invalid plaintext character.\n";
            }
        }
    }

    cout << "\n--- RECOVERED KEY MAPPING ---\n";
    cout << "CIPHER : ABCDEFGHIJKLMNOPQRSTUVWXYZ\n";
    cout << "PLAIN  : " << user_recovered_key << "\n";

    verify_solution(plaintext, ciphertext, user_recovered_key);

    return 0;
}