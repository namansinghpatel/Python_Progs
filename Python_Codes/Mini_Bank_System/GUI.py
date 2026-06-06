# gui.py

import tkinter as tk
from tkinter import messagebox
from Mini_Bank_System import BankAccount

account = BankAccount()

root = tk.Tk()
root.title("XYZ Bank")
root.geometry("400x300")


# =========================
# Create Account
# =========================
def create_account():

    username = user_entry.get()
    pin = pin_entry.get()

    if username == "" or pin == "":
        messagebox.showerror("Error", "Enter username and PIN")
        return

    account.create_account(username, pin)

    messagebox.showinfo("Success", "Account Created")


# =========================
# Login
# =========================
def login():

    username = user_entry.get()
    pin = pin_entry.get()

    if account.login(username, pin):

        messagebox.showinfo("Login", "Login Successful")

        balance_label.config(
            text=f"Balance: {account.get_balance()}"
        )

    else:

        messagebox.showerror(
            "Error",
            "Invalid Username or PIN"
        )


# =========================
# Deposit
# =========================
def deposit():

    amount = int(amount_entry.get())

    account.deposit(amount)

    balance_label.config(
        text=f"Balance: {account.get_balance()}"
    )


# =========================
# Withdraw
# =========================
def withdraw():

    amount = int(amount_entry.get())

    if account.withdraw(amount):

        balance_label.config(
            text=f"Balance: {account.get_balance()}"
        )

    else:

        messagebox.showerror(
            "Error",
            "Insufficient Balance"
        )


# =========================
# Widgets
# =========================

tk.Label(root, text="Username").pack()

user_entry = tk.Entry(root)
user_entry.pack()

tk.Label(root, text="PIN").pack()

pin_entry = tk.Entry(root, show="*")
pin_entry.pack()

tk.Button(
    root,
    text="Create Account",
    command=create_account
).pack(pady=5)

tk.Button(
    root,
    text="Login",
    command=login
).pack(pady=5)

tk.Label(root, text="Amount").pack()

amount_entry = tk.Entry(root)
amount_entry.pack()

tk.Button(
    root,
    text="Deposit",
    command=deposit
).pack(pady=5)

tk.Button(
    root,
    text="Withdraw",
    command=withdraw
).pack(pady=5)

balance_label = tk.Label(
    root,
    text="Balance: 0"
)
balance_label.pack(pady=10)

root.mainloop()