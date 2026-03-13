import json
from config import MASTER_LOGIN_PATH, PASSWORD_FILE_PATH
from password_manager import add_password, delete_password, log_update, retrieve_password, update_password


def main():
    if MASTER_LOGIN_PATH.exists():
        with MASTER_LOGIN_PATH.open('r', encoding='utf-8') as file:
            master_login = json.load(file)

    if PASSWORD_FILE_PATH.exists():
        with PASSWORD_FILE_PATH.open('r', encoding='utf-8') as file:
            app_password = json.load(file)

    while True:
        # Create a more visually appealing header
        print("="*40)
        print(f"{'Welcome to the Password Manager'.center(40)}")
        print("="*40)

        # User login
        uid = input("Enter your UID: ")
        if uid not in master_login:
            print("\n[!] User not found.\n")
            continue

        pss = input("Enter your password: ")
        if master_login[uid] != pss:
            print("\n[!] Password mismatch.\n")
            continue

        # updating the log for an user login
        log_update(f"User {uid} has logged-in")

        # Success message with stylized heading
        print("*"*40)
        print(f"{f'Login successful - Welcome {uid}'.center(40)}")
        print("*"*40)

        # Menu for actions
        while True:
            print("\nSelect an option:")
            print("+"*40)
            print("1. Add Password")
            print("2. Retrieve Password")
            print("3. Update Password")
            print("4. Delete Password")
            print("9. Exit")
            print("+"*40)

            choice = input("Choose an option: ")

            if choice == "1":
                add_password(uid)
            elif choice == "2":
                retrieve_password(uid)
            elif choice == "3":
                update_password(uid)
            elif choice == "4":
                delete_password(uid)
            elif choice == "9":
                print(f"\n[!] Exiting the Password Manager. Stay safe! - {uid}")
                break
            else:
                print("\n[!] Invalid option. Please try again.\n")

        # End message
        print("="*40)
        print(f"{'Thank you for using the Password Manager!'.center(40)}")
        print("="*40)
        break  # Break the while loop to exit after finishing tasks.

if __name__ == "__main__":
    main()
