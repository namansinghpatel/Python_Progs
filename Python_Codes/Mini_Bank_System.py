print("Welcome to XYZ Bank!!")
print("Please select an option:")
print("1. Create new account")
print("2. Login to an existing account")

choice = int(input("Choose an option: "))

if choice == 1:
    print("Thank you for creating an account with us")

    username = input("Please enter your username: ")
    pin = int(input("Please enter your PIN: "))

    while True:
        con_pin = int(input("Please confirm your PIN: "))
        if pin == con_pin:
            print("Account created successfully")
            break
        else:
            print("Wrong PIN confirmation. Try again.")

    balance = 0

    print("Now login to continue")

    login_user = input("Enter username: ")
    login_pin = int(input("Enter PIN: "))

    if login_user == username and login_pin == pin:
        print("Login successful")

        print("choose any option")

        print("1. Deposit")
        print("2. Withdraw")

        option = int(input("Choose an option: "))

        if option == 1:
            amount = int(input("Enter amount to deposit: "))
            balance += amount
            print("Deposit successful")
            print("Current balance:", balance)

        elif option == 2:
            amount = int(input("Enter amount to withdraw: "))

            if amount <= balance:
                balance -= amount
                print("Withdrawal successful")
                print("Current balance:", balance)
            else:
                print("Insufficient balance")

        else:
            print("Invalid option")

    else:
        print("Invalid username or PIN")

elif choice == 2:
    print("No account exists yet. Please create an account first.")

else:
    print("Invalid choice")