# Importing Libraries
import os, json
import secrets
import string
from datetime import datetime

# Initializing file locations and names
MASTER_LOGIN    =   'master_login.json'
PASSWORD_FILE   =   'app_password.json'
LOG_FILE        =   'log.txt'

# Dummy Data
# {"Username":"Password"}
master_login = {"Jimmy":"robert@123",
                "Angela":"2009_Bonnet"}



#  { "Username":[ {"domain":"", "pwd":"" },
#                 {"domain":"", "pwd":"" },... ] }
app_password = {
    "Jimmy": [
        {"domain": "Facebook", "pwd": "JimmyGordan"},
        {"domain": "Instagram", "pwd": "B0atm@n"}
    ],
    "Angela": [
        {"domain": "Facebook", "pwd": "Angela009"},
        {"domain": "Instagram", "pwd": "Mikcy&Angela"},
    ]
}

def ensure_storage():
    """Ensure storage files exist (master logins, password store, and log file)."""
    if not os.path.exists(MASTER_LOGIN):
        with open(MASTER_LOGIN, 'w+') as file:
            json.dump(master_login, file, indent=4)

    if not os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, 'w+') as file:
            json.dump(app_password, file, indent=4)

    # Ensure log exists
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, 'a+').close()


def read_master_login():
    """Read master login credentials from storage."""
    ensure_storage()
    with open(MASTER_LOGIN, 'r') as file:
        return json.load(file)


def authenticate(uid, password):
    """Authenticate a user against the master login store."""
    master = read_master_login()
    return uid in master and master[uid] == password


def get_user_passwords(uid):
    """Return a list of password entries for a user."""
    app_password = read_passwords()
    return app_password.get(uid, [])


def get_password_entry(uid, index):
    """Return a specific password entry by index (0-based)."""
    entries = get_user_passwords(uid)
    if 0 <= index < len(entries):
        return entries[index]
    return None


def add_password_entry(uid, domain, password=None):
    """Create a new password entry for a user."""
    app_password = read_passwords()
    if uid not in app_password:
        app_password[uid] = []

    if not password:
        password = generate_secure_password()

    new_entry = {"domain": domain, "pwd": password}
    app_password[uid].append(new_entry)
    write_passwords(app_password)
    log_update(f"Added password for {domain} under user {uid}")
    return new_entry


def update_password_entry(uid, index, new_password=None):
    """Update an existing password entry by index."""
    app_password = read_passwords()
    entries = app_password.get(uid, [])
    if index < 0 or index >= len(entries):
        return None

    if not new_password:
        new_password = generate_secure_password()

    entries[index]["pwd"] = new_password
    write_passwords(app_password)
    log_update(f"Updated password for {entries[index]['domain']} under user {uid}")
    return entries[index]


def delete_password_entry(uid, index):
    """Delete a password entry by index."""
    app_password = read_passwords()
    entries = app_password.get(uid, [])
    if index < 0 or index >= len(entries):
        return None

    deleted_entry = entries.pop(index)
    write_passwords(app_password)
    log_update(f"Deleted password for {deleted_entry['domain']} under user {uid}")
    # log the deleted credentials for audit purposes
    log_update(
        f"Deleted credentials - user: {uid}, domain: {deleted_entry['domain']}, password: {deleted_entry['pwd']}"
    )
    return deleted_entry


def getting_equal_length(num):
    # Divide the number by 4 using integer division
    quotient = num // 4
    remainder = num % 4
    # Create a list with the quotient repeated 4 times
    result = [quotient] * 4
    # Distribute the remainder among the first few elements
    for i in range(remainder):
        result[i] += 1
    return result


def generate_secure_password(length=12):
    distribution = getting_equal_length(length)

    password = []

    password += [secrets.choice(string.ascii_lowercase) for _ in range(distribution[0])]
    password += [secrets.choice(string.ascii_uppercase) for _ in range(distribution[1])]
    password += [secrets.choice(string.digits) for _ in range(distribution[2])]
    password += [secrets.choice(string.punctuation) for _ in range(distribution[3])]


    # Shuffling the password
    secrets.SystemRandom().shuffle(password)
    return ''.join(password)


# Function to read the stored passwords from the file
def read_passwords():
    ensure_storage()
    with open(PASSWORD_FILE, 'r') as file:
        return json.load(file)

# Function to write the passwords to the file
def write_passwords(data):
    ensure_storage()
    with open(PASSWORD_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Function to log updates to the password log
def log_update(message):
    ensure_storage()
    with open(LOG_FILE, 'a+') as log_file:
        log_file.write(f"{datetime.now()} - {message}\n")

def add_password(uid):
    # Read the stored passwords from the file
    app_password = read_passwords()

    # Prompt user to enter domain and password
    print("="*40)
    print(f"{'Add Password'.center(40)}")
    print("="*40)

    domain = input("Enter the domain name: ")
    print(f"<======  If you wish to generate a random password, leave the password field as blank. ======>")
    password = input("Enter the password for the domain: ")

    # Generating a random password if the user has not provided the password
    if password == "":
      password = generate_secure_password()

    # Check if the user exists in app_password; if not, initialize an empty list for them
    if uid not in app_password:
        app_password[uid] = []

    # Create a new password entry
    new_entry = { "domain": domain, "pwd": password }

    # Append the new entry to the user's password list
    app_password[uid].append(new_entry)

    # Write the updated password list back to the file
    write_passwords(app_password)

    # Log the action for tracking purposes
    log_update(f"Added password for {domain} under user {uid}")

    # Print success message with a decorative format
    print("*"*40)
    print(f"Password for {domain} has been added successfully.")
    print("*"*40)


def retrieve_password(uid):
    # Read the stored passwords from the file
    app_password = read_passwords()

    # Check if the user exists and has stored passwords
    if uid in app_password and app_password[uid]:
        print("="*40)
        print(f"{'Stored Passwords'.center(40)}")  # Title centered
        print("="*40)

        # Enumerate through the list of stored passwords and display the domains
        for index, entry in enumerate(app_password[uid], 1):
            print(f"{index}. {entry['domain']}")  # List the domain name (website)

        # Allow the user to select an option to view a specific password
        try:
            choice = int(input("\nEnter the option number to display the password: "))

            # Validate the user's choice
            if 0 < choice <= len(app_password[uid]):
                selected_entry = app_password[uid][choice - 1]

                # Display the selected password details with decorative formatting
                print("*"*40)
                print(f"Password for {selected_entry['domain']} ==> {selected_entry['pwd']}")
                print("*"*40)
                # Log the password retrival
                log_update(f"Retrieved password for {selected_entry['domain']} under user {uid}")

            else:
                # Invalid option if the choice is out of range
                print("\n[!] Invalid option selected. Please choose a valid number.\n")

        except ValueError:
            # Error message if the user does not input a valid integer
            print("\n[!] Please enter a valid number.\n")

    else:
        # If no passwords are stored or user is not found
        print("\n[!] No passwords stored or user not found.\n")


def update_password(uid):
    # Read the stored passwords from the file
    app_password = read_passwords()

    # Check if the user exists and has stored passwords
    if uid in app_password and app_password[uid]:
        print("="*40)
        print(f"{'Stored Passwords'.center(40)}")  # Title centered
        print("="*40)

        # Enumerate through the list of stored passwords and display the domains
        for index, entry in enumerate(app_password[uid], 1):
            print(f"{index}. {entry['domain']}")  # Display domain name

        # Allow the user to select an option to update a specific password
        try:
            choice = int(input("\nEnter the option number to update the password: "))

            # Validate if the choice is within the valid range
            if 0 < choice <= len(app_password[uid]):
                selected_entry = app_password[uid][choice - 1]

                # Prompt the user for the new password
                print(f"<======  If you wish to generate a random password, leave the password field as blank. ======>")
                new_password = input(f"Enter the new password for {selected_entry['domain']}: ")

                # Generating a random password if the user has not provided the password and updating it
                if new_password == "":
                  selected_entry["pwd"] = generate_secure_password()

                # Write the updated passwords back to the file
                write_passwords(app_password)

                # Log the password update
                log_update(f"Updated password for {selected_entry['domain']} under user {uid}")

                # Provide success feedback to the user
                print("*"*40)
                print(f"Password for {selected_entry['domain']} updated successfully.")
                print("*"*40)

            else:
                # Handle invalid selection
                print("\n[!] Invalid option selected. Please choose a valid number.\n")

        except ValueError:
            # Handle non-integer input
            print("\n[!] Please enter a valid number.\n")

    else:
        # If no passwords are stored or user is not found
        print("\n[!] No passwords stored or user not found.\n")


def delete_password(uid):
    # Read the stored passwords from the file
    app_password = read_passwords()

    # Check if the user exists and has stored passwords
    if uid in app_password and app_password[uid]:
        print("=" * 40)
        print(f"{'Stored Passwords'.center(40)}")
        print("=" * 40)

        # Enumerate through the list of stored passwords and display the domains
        for index, entry in enumerate(app_password[uid], 1):
            print(f"{index}. {entry['domain']}")

        try:
            choice = int(input("\nEnter the option number to delete the password: "))
            if 0 < choice <= len(app_password[uid]):
                deleted_entry = app_password[uid].pop(choice - 1)  # Delete the entry

                write_passwords(app_password)  # Update the password file

                log_update(f"Deleted password for {deleted_entry['domain']} under user {uid}")
                log_update(f"Deleted credentials - user: {uid}, domain: {deleted_entry['domain']}, password: {deleted_entry['pwd']} ")

                print("*" * 40)
                print(f"Password for {deleted_entry['domain']} deleted successfully.")
                print("*" * 40)

            else:
                print("\n[!] Invalid option selected. Please choose a valid number.\n")

        except ValueError:
            print("\n[!] Please enter a valid number.\n")
    else:
        print("\n[!] No passwords stored or user not found.\n")


def main():


    if os.path.exists("master_login.json"):
        with open("master_login.json", 'r') as file:
            master_login = json.load(file)

    if os.path.exists("app_password.json"):
        with open("app_password.json", 'r') as file:
            PASSWORD_FILE = json.load(file)

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
