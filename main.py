# Bank Account Simulator
# Uses a dictionary (hash map) to store all accounts.
# Each account maps to another dictionary holding its balance and transaction history.
#
# Data structure layout:
#   accounts = {
#       "ACC001": {
#           "balance": 500.0,
#           "transactions": [
#               {"type": "Deposit", "amount": 500.0, "balance_after": 500.0},
#               ...
#           ]
#       },
#       ...
#   }

import datetime  # used only to timestamp transactions


# --- Helper Functions ---

def create_account(accounts, account_number, starting_balance):
    """Create a new account and add it to the accounts dictionary."""

    # Check if account already exists
    if account_number in accounts:
        print("Error: Account already exists.")
        return

    # Validate starting balance
    if starting_balance < 0:
        print("Error: Starting balance cannot be negative.")
        return

    # Build the account entry as a dictionary
    accounts[account_number] = {
        "balance": starting_balance,
        "transactions": []  # empty list; we'll append to this over time
    }

    # Record the opening transaction
    record_transaction(accounts, account_number, "Account Opened", starting_balance)
    print("Account created! Account number:", account_number)


def deposit(accounts, account_number, amount):
    """Add money to an existing account."""

    # Make sure the account exists before doing anything
    if account_number not in accounts:
        print("Error: Account not found.")
        return

    # Amount must be positive
    if amount <= 0:
        print("Error: Deposit amount must be greater than 0.")
        return

    # Add the amount to the balance
    accounts[account_number]["balance"] = accounts[account_number]["balance"] + amount

    record_transaction(accounts, account_number, "Deposit", amount)
    print("Deposited $%.2f. New balance: $%.2f" % (amount, accounts[account_number]["balance"]))


def withdraw(accounts, account_number, amount):
    """Remove money from an existing account if funds are sufficient."""

    # Make sure the account exists
    if account_number not in accounts:
        print("Error: Account not found.")
        return

    # Amount must be positive
    if amount <= 0:
        print("Error: Withdrawal amount must be greater than 0.")
        return

    # Check that the account has enough money
    if amount > accounts[account_number]["balance"]:
        print("Error: Insufficient funds. Balance is $%.2f" % accounts[account_number]["balance"])
        return

    # Subtract the amount from the balance
    accounts[account_number]["balance"] = accounts[account_number]["balance"] - amount

    record_transaction(accounts, account_number, "Withdrawal", amount)
    print("Withdrew $%.2f. New balance: $%.2f" % (amount, accounts[account_number]["balance"]))


def check_balance(accounts, account_number):
    """Print the current balance of an account."""

    if account_number not in accounts:
        print("Error: Account not found.")
        return

    balance = accounts[account_number]["balance"]
    print("Account %s balance: $%.2f" % (account_number, balance))


def view_transactions(accounts, account_number):
    """Loop through and print the transaction history for an account."""

    if account_number not in accounts:
        print("Error: Account not found.")
        return

    # Get the list of transaction dictionaries for this account
    history = accounts[account_number]["transactions"]

    if len(history) == 0:
        print("No transactions found.")
        return

    print("\n--- Transaction History for Account %s ---" % account_number)

    # Loop through each transaction dictionary in the list
    for i in range(len(history)):
        t = history[i]  # t is one transaction dictionary
        print("%d. [%s] %s  $%.2f  (Balance after: $%.2f)"
              % (i + 1, t["date"], t["type"], t["amount"], t["balance_after"]))

    print("--- End of History ---\n")


def record_transaction(accounts, account_number, transaction_type, amount):
    """Append a transaction record (dictionary) to the account's transactions list."""

    # Get today's date and time as a string
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Build a dictionary for this single transaction
    transaction = {
        "date": timestamp,
        "type": transaction_type,
        "amount": amount,
        "balance_after": accounts[account_number]["balance"]
    }

    # Append it to the account's transactions list
    accounts[account_number]["transactions"].append(transaction)

    # Also save to a plain text log file so data persists between runs
    save_to_file(account_number, transaction)


def save_to_file(account_number, transaction):
    """Write a single transaction line to transactions.txt."""

    # Open file in append mode ("a") so we don't erase previous entries
    file = open("transactions.txt", "a")
    line = "%s | %s | %s | $%.2f | Balance: $%.2f\n" % (
        transaction["date"],
        account_number,
        transaction["type"],
        transaction["amount"],
        transaction["balance_after"]
    )
    file.write(line)
    file.close()


# --- Main Program ---

def run_simulator():
    """Main loop that shows a menu and handles user input."""

    # This dictionary holds all accounts for the current session
    accounts = {}

    while True:
        # Print the menu options
        print("\n===== Bank Account Simulator =====")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. View Transaction History")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            account_number = input("Enter new account number: ")
            starting_balance = float(input("Enter starting balance: $"))
            create_account(accounts, account_number, starting_balance)

        elif choice == "2":
            account_number = input("Enter account number: ")
            amount = float(input("Enter amount to deposit: $"))
            deposit(accounts, account_number, amount)

        elif choice == "3":
            account_number = input("Enter account number: ")
            amount = float(input("Enter amount to withdraw: $"))
            withdraw(accounts, account_number, amount)

        elif choice == "4":
            account_number = input("Enter account number: ")
            check_balance(accounts, account_number)

        elif choice == "5":
            account_number = input("Enter account number: ")
            view_transactions(accounts, account_number)

        elif choice == "6":
            print("Goodbye!")
            break  # exit the while loop

        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


# --- Test Case ---
# This block only runs when you execute this file directly (not when imported).
# It tests each function automatically without needing manual input.

def run_tests():
    print("===== Running Tests =====\n")

    # Use a fresh dictionary for tests so it doesn't affect real data
    test_accounts = {}

    # Test 1: Create an account
    print("Test 1 - Create account:")
    create_account(test_accounts, "T001", 200.0)
    assert "T001" in test_accounts, "FAIL: Account not created"
    assert test_accounts["T001"]["balance"] == 200.0, "FAIL: Wrong starting balance"
    print("PASS\n")

    # Test 2: Deposit money
    print("Test 2 - Deposit $50:")
    deposit(test_accounts, "T001", 50.0)
    assert test_accounts["T001"]["balance"] == 250.0, "FAIL: Deposit not applied"
    print("PASS\n")

    # Test 3: Withdraw money
    print("Test 3 - Withdraw $100:")
    withdraw(test_accounts, "T001", 100.0)
    assert test_accounts["T001"]["balance"] == 150.0, "FAIL: Withdrawal not applied"
    print("PASS\n")

    # Test 4: Overdraft should be blocked
    print("Test 4 - Overdraft attempt:")
    balance_before = test_accounts["T001"]["balance"]
    withdraw(test_accounts, "T001", 9999.0)  # should print error and not change balance
    assert test_accounts["T001"]["balance"] == balance_before, "FAIL: Overdraft was allowed"
    print("PASS\n")

    # Test 5: Transaction history should have 3 entries (open, deposit, withdraw)
    print("Test 5 - Transaction history length:")
    history = test_accounts["T001"]["transactions"]
    assert len(history) == 3, "FAIL: Expected 3 transactions, got %d" % len(history)
    print("PASS\n")

    # Test 6: Duplicate account creation should be blocked
    print("Test 6 - Duplicate account:")
    create_account(test_accounts, "T001", 500.0)  # should print error
    assert test_accounts["T001"]["balance"] == 150.0, "FAIL: Duplicate account overwrote data"
    print("PASS\n")

    print("===== All Tests Passed =====\n")


# Entry point: ask the user whether to run tests or the real simulator
if __name__ == "__main__":
    mode = input("Run (T)ests or (S)imulator? [T/S]: ").strip().upper()
    if mode == "T":
        run_tests()
    else:
        run_simulator()
