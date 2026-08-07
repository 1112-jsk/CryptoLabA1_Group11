import sys
from utils.logger import log_execution

def display_menu():
    print("==========================================")
    print("      CryptoLabX Framework - v1.0         ")
    print("==========================================")
    print("  1. Encrypt")
    print("  2. Decrypt")
    print("  3. Attack")
    print("  4. Analyze")
    print("  5. Exit")
    print("==========================================")

def main():
    while True:
        display_menu()
        choice = input("Select an option (1-5): ").strip()
        
        log_execution(choice)

        if choice == "1":
            print("\n[+] Encrypt Module: Coming Soon!\n")
        elif choice == "2":
            print("\n[+] Decrypt Module: Coming Soon!\n")
        elif choice == "3":
            print("\n[+] Attack Module: Coming Soon!\n")
        elif choice == "4":
            print("\n[+] Analyze Module: Coming Soon!\n")
        elif choice == "5":
            print("\nExiting CryptoLabX Toolkit. Goodbye!")
            sys.exit(0)
        else:
            print(f"\n[!] Invalid entry '{choice}'. Please select a number from 1 to 5.\n")

if __name__ == "__main__":
    main()
