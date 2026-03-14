import csv
from datetime import datetime


class BankAccount:
    def __init__(self, account_number, balance=0):
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be greater than 0.")
            return False
        else:
            self.balance = self.balance + amount
            print("Deposit successful.")
            return True

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdraw amount must be greater than 0.")
            return False
        elif amount > self.balance:
            print("Not enough money in the account.")
            return False
        else:
            self.balance = self.balance - amount
            print("Withdraw successful.")
            return True

    def check_balance(self):
        print("Current balance is:", self.balance)


def save_transaction(account_number, action, amount, balance):
    file_name = "transactions.csv"

    with open(file_name, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), account_number, action, amount, balance])


accounts = {}

while True:
    print("\n----- Simple Bank Account Simulator -----")
    print("1. Create Account")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Check Balance")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        account_number = input("Enter account number: ")

        if account_number in accounts:
            print("This account already exists.")
        else:
            starting_balance = float(input("Enter starting balance: "))
            new_account = BankAccount(account_number, starting_balance)
            accounts[account_number] = new_account
            print("Account created successfully.")
            save_transaction(account_number, "Account Created", starting_balance, starting_balance)

    elif choice == "2":
        account_number = input("Enter account number: ")

        if account_number in accounts:
            amount = float(input("Enter amount to deposit: "))
            success = accounts[account_number].deposit(amount)

            if success:
                save_transaction(account_number, "Deposit", amount, accounts[account_number].balance)
        else:
            print("Account not found.")

    elif choice == "3":
        account_number = input("Enter account number: ")

        if account_number in accounts:
            amount = float(input("Enter amount to withdraw: "))
            success = accounts[account_number].withdraw(amount)

            if success:
                save_transaction(account_number, "Withdraw", amount, accounts[account_number].balance)
        else:
            print("Account not found.")

    elif choice == "4":
        account_number = input("Enter account number: ")

        if account_number in accounts:
            accounts[account_number].check_balance()
        else:
            print("Account not found.")

    elif choice == "5":
        print("Thank you for using the program.")
        break

    else:
        print("Invalid choice. Please try again.")
