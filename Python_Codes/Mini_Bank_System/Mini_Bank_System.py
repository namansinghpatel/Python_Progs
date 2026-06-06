# bank.py


class BankAccount:

    def __init__(self):
        self.username = None
        self.pin = None
        self.balance = 0

    # =========================
    # Account Creation
    # =========================
    def create_account(self, username, pin):
        self.username = username
        self.pin = pin
        self.balance = 0

    # =========================
    # Login
    # =========================
    def login(self, username, pin):

        return (
            self.username == username and
            self.pin == pin
        )

    # =========================
    # Deposit
    # =========================
    def deposit(self, amount):

        if amount <= 0:
            return False

        self.balance += amount
        return True

    # =========================
    # Withdraw
    # =========================
    def withdraw(self, amount):

        if amount <= 0:
            return False

        if amount > self.balance:
            return False

        self.balance -= amount
        return True

    # =========================
    # Balance
    # =========================
    def get_balance(self):
        return self.balance


# ==================================================
# Console Mode
# ==================================================

def run_console():

    account = BankAccount()

    while True:

        print("\n" + "=" * 40)
        print("        XYZ BANK")
        print("=" * 40)

        print("1. Create Account")
        print("2. Login")
        print("0. Exit")

        choice = input("\nChoose option: ")

        # ----------------------------------
        # Create Account
        # ----------------------------------
        if choice == "1":

            print("\n===== Create Account =====")

            username = input("Enter Username: ")

            pin = input("Enter PIN: ")

            while True:

                confirm_pin = input("Confirm PIN: ")

                if pin == confirm_pin:
                    break

                print("PIN mismatch. Try again.")

            account.create_account(
                username,
                pin
            )

            print("\nAccount created successfully.")

        # ----------------------------------
        # Login
        # ----------------------------------
        elif choice == "2":

            print("\n===== Login =====")

            username = input("Username: ")
            pin = input("PIN: ")

            if account.login(username, pin):

                print("\nLogin successful.")

                # =====================
                # Banking Menu
                # =====================
                while True:

                    print("\n" + "-" * 40)
                    print("1. Deposit")
                    print("2. Withdraw")
                    print("3. Check Balance")
                    print("0. Logout")
                    print("-" * 40)

                    option = input("Choose option: ")

                    # Deposit
                    if option == "1":

                        amount = float(
                            input("Deposit Amount: ")
                        )

                        if account.deposit(amount):

                            print(
                                f"Deposit successful."
                            )

                            print(
                                f"Balance = {account.get_balance()}"
                            )

                        else:

                            print(
                                "Invalid deposit amount."
                            )

                    # Withdraw
                    elif option == "2":

                        amount = float(
                            input("Withdraw Amount: ")
                        )

                        if account.withdraw(amount):

                            print(
                                "Withdrawal successful."
                            )

                            print(
                                f"Balance = {account.get_balance()}"
                            )

                        else:

                            print(
                                "Insufficient balance or invalid amount."
                            )

                    # Balance
                    elif option == "3":

                        print(
                            f"Current Balance = {account.get_balance()}"
                        )

                    # Logout
                    elif option == "0":

                        print(
                            "Logged out successfully."
                        )

                        break

                    else:

                        print(
                            "Invalid option."
                        )

            else:

                print(
                    "\nInvalid username or PIN."
                )

        # ----------------------------------
        # Exit
        # ----------------------------------
        elif choice == "0":

            print("\nThank you for using XYZ Bank.")
            break

        else:

            print("\nInvalid choice.")


# ==================================================
# Entry Point
# ==================================================

if __name__ == "__main__":
    run_console()