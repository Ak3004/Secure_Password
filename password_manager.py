import json
from datetime import datetime

from Week_2.password import getting_equal_length, generate_secure_password

from config import (
    ensure_data_dir_exists,
    LOG_FILE_PATH,
    PASSWORD_FILE_PATH,
)

# Ensure the data directory / file paths are available.
ensure_data_dir_exists()

# Function to read the stored passwords from the file
def read_passwords():
    if PASSWORD_FILE_PATH.exists():
        with PASSWORD_FILE_PATH.open("r", encoding="utf-8") as file:
            return json.load(file)
    return {}

# Function to write the passwords to the file
def write_passwords(data):
    with PASSWORD_FILE_PATH.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

# Function to log updates to the password log
def log_update(message):
    with LOG_FILE_PATH.open("a+", encoding="utf-8") as log_file:
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