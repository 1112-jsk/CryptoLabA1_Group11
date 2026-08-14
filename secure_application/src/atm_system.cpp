#include <iostream>
#include <cstring>
#include <string>

using namespace std;

// VULNERABILITY 1: Hardcoded Credentials
char current_pin[20] = "1234";
double account_balance = 5000.0;
bool logged_in = false;

void login() {
    char input_pin[5];
    string user_input;

    cout << "\n--- ATM Login ---\n";
    cout << "Enter your 4-digit PIN: ";
    cin >> user_input;

    // VULNERABILITY 2: Improper Input Validation
    strcpy(input_pin, user_input.c_str());

    if (strcmp(input_pin, current_pin) == 0) {
        logged_in = true;
        cout << "Login successful! Welcome.\n";
    } else {
        cout << "Authentication failed. Incorrect PIN.\n";
    }
}

void balanceInquiry() {
    if (!logged_in) {
        cout << "Access Denied: Please login first.\n";
        return;
    }
    cout << "Current Balance: $" << account_balance << "\n";
}

void withdrawal() {
    if (!logged_in) {
        cout << "Access Denied: Please login first.\n";
        return;
    }
    
    double amount;
    cout << "Enter amount to withdraw: $";
    cin >> amount;
    
    if (amount > account_balance) {
        cout << "Transaction Failed: Insufficient funds.\n";
    } else if (amount <= 0) {
        cout << "Invalid amount.\n";
    } else {
        account_balance -= amount;
        cout << "Please collect your cash. New Balance: $" << account_balance << "\n";
    }
}

void deposit() {
    // VULNERABILITY 3: Missing Authentication Checks
    double amount;
    cout << "Enter amount to deposit: $";
    cin >> amount;
    
    if (amount > 0) {
        account_balance += amount;
        cout << "Deposit successful. New Balance: $" << account_balance << "\n";
    } else {
        cout << "Invalid deposit amount.\n";
    }
}

void changePin() {
    if (!logged_in) {
        cout << "Access Denied: Please login first.\n";
        return;
    }
    
    string new_pin;
    cout << "Enter new 4-digit PIN: ";
    cin >> new_pin;

    strcpy(current_pin, new_pin.c_str());
    cout << "PIN successfully changed!\n";
}

int main() {
    int choice;

    while (true) {
        cout << "\n========================\n";
        cout << "       ATM SYSTEM       \n";
        cout << "========================\n";
        cout << "1. Login\n";
        cout << "2. Balance Inquiry\n";
        cout << "3. Withdraw Funds\n";
        cout << "4. Deposit Funds (Fast Deposit)\n";
        cout << "5. Change PIN\n";
        cout << "6. Exit\n";
        cout << "Select an option: ";

        cin >> choice;

        switch (choice) {
            case 1: login(); break;
            case 2: balanceInquiry(); break;
            case 3: withdrawal(); break;
            case 4: deposit(); break; 
            case 5: changePin(); break;
            case 6:
                cout << "Thank you for using the ATM. Goodbye!\n";
                return 0;
            default:
                cout << "Invalid choice. Please try again.\n";
        }
    }
    return 0;
}