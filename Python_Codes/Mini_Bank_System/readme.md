# 🏦 XYZ Bank - Mini Banking System (Python)

A beginner-friendly banking application developed in Python to learn programming fundamentals, Object-Oriented Programming (OOP), and GUI development using Tkinter.

The project provides both:

* 💻 Console-Based Banking System
* 🖥️ GUI-Based Banking System

and demonstrates how business logic can be separated from the user interface, a common software engineering practice used in real-world applications.

---

# 🎯 Project Goals

This project was created to learn and practice:

* Python Programming
* Functions and Modular Design
* Classes and Objects
* Object-Oriented Programming (OOP)
* Lists and Data Management
* User Input Validation
* Error Handling
* GUI Development using Tkinter
* Project Structure and Code Organization

---

# ✨ Features

## 💻 Console Version

### Account Management

* Create New Account
* Username & PIN Validation
* PIN Confirmation During Registration
* Login Authentication

### Banking Operations

* Deposit Money
* Withdraw Money
* Check Current Balance
* View Transaction History
* Logout
* Exit Program

### Transaction Tracking

Every operation is recorded:

```text
Login
Deposit: 500
Withdraw: 200
Deposit: 1000
Logout
```

---

## 🖥️ GUI Version

The graphical version provides a simple desktop interface using Tkinter.

### GUI Features

* Create Account
* Login System
* Deposit Money
* Withdraw Money
* Balance Display
* Password Masking
* Popup Notifications
* User-Friendly Interface

---

# 🧠 Concepts Demonstrated

## Python Fundamentals

* Variables
* Data Types
* Strings
* Lists
* Loops
* Conditional Statements
* Functions

## Object-Oriented Programming

* Classes
* Objects
* Constructors (`__init__`)
* Methods
* Instance Variables

Example:

```python
account = BankAccount()
```

The account object stores:

```text
Username
PIN
Balance
Transaction History
```

---

## GUI Programming

Built using Tkinter:

```python
import tkinter as tk
```

Widgets used:

* Labels
* Buttons
* Entry Boxes
* Message Boxes

---

## Software Design Principles

The project separates:

```text
GUI Layer
    ↓
Business Logic Layer
```

### bank.py

Responsible for:

* Account Creation
* Login Validation
* Deposits
* Withdrawals
* Balance Management

### gui.py

Responsible for:

* User Interface
* User Input
* Displaying Information

This separation makes the application easier to maintain and extend.

---

# 🗂️ Project Structure

```text
XYZ_Bank/
│
├── bank.py
│   ├── BankAccount Class
│   ├── Console Application
│   └── Banking Logic
│
├── gui.py
│   ├── Tkinter GUI
│   ├── Buttons
│   ├── Labels
│   └── Event Handlers
│
├── README.md
│
└── screenshot.png (optional)
```

---

# 🖥️ Requirements

## Python Version

```text
Python 3.10+
```

Verify:

```bash
python --version
```

Example:

```text
Python 3.12.4
```

---

## Tkinter

Tkinter is usually included with Python.

Verify installation:

```bash
python -m tkinter
```

A test window should appear.

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/namansinghpatel/Python_Progs.git
```

Move into project directory:

```bash
cd Python_Progs
```

---

# ▶️ Running the Application

## Run Console Version

```bash
python bank.py
```

---

## Run GUI Version

```bash
python gui.py
```

---

# 💻 Console Workflow Example

## Create Account

```text
===== XYZ BANK =====

1. Create Account
2. Login
0. Exit

Choose option: 1

Enter Username: Prashant
Enter PIN: 1234
Confirm PIN: 1234

Account created successfully.
```

---

## Login

```text
Username: Prashant
PIN: 1234

Login successful.
```

---

## Banking Menu

```text
1. Deposit
2. Withdraw
3. Check Balance
4. Transaction History
0. Logout
```

---

## Deposit Example

```text
Deposit Amount: 500

Deposit successful.
Balance = 500
```

---

## Withdrawal Example

```text
Withdraw Amount: 200

Withdrawal successful.
Balance = 300
```

---

# 📸 Screenshot

Place a screenshot in the project folder:

```text
screenshot.png
```

Then add:

```markdown
![XYZ Bank GUI](screenshot.png)
```

GitHub will automatically display the image.

---

# 🔮 Future Enhancements

Planned improvements:

## Banking Features

* Multiple User Accounts
* Account Numbers
* Money Transfer
* Account Statements
* Interest Calculation

## Security Features

* Password Hashing
* PIN Encryption
* Login Attempt Limits
* Account Locking

## Data Storage

* JSON Storage
* CSV Export
* Database Integration (SQLite)

## GUI Improvements

* Modern Theme
* Dashboard
* Transaction Tables
* Charts and Analytics

---

# 🧪 Testing Ideas

Suggested test cases:

### Login

* Correct Username & PIN
* Incorrect Username
* Incorrect PIN

### Deposit

* Positive Amount
* Zero Amount
* Negative Amount

### Withdraw

* Sufficient Balance
* Insufficient Balance
* Negative Amount

---

# 👨‍💻 Author

## Naman Singh Patel

Python Enthusiast | Learning Software Development

GitHub:
https://github.com/namansinghpatel

---

# 📜 License

This project is created for educational and learning purposes.

Feel free to modify, improve, and experiment with the code.

---

⭐ If you found this project helpful, consider giving it a star on GitHub.
