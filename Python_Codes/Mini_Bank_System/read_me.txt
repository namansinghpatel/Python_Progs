# 🏦 XYZ Bank - Mini Banking System

A simple Python Banking System built for learning programming concepts such as:

* Variables
* Loops
* Functions
* Classes
* Object-Oriented Programming (OOP)
* Input Validation
* GUI Development with Tkinter
* Project Structure

---

## Features

### Console Version

* Create Account
* Login
* Deposit Money
* Withdraw Money
* Check Balance
* Transaction History
* Logout
* Exit Program

### GUI Version

* Create Account
* Login
* Deposit Money
* Withdraw Money
* Check Balance
* Password Masking
* Popup Messages

---

## Project Structure

```text
BankProject/
│
├── bank.py       # Banking logic + Console version
├── gui.py        # Tkinter GUI
├── README.md
```

---

## Requirements

* Python 3.10 or later
* Tkinter (usually included with Python)

Verify installation:

```bash
python -m tkinter
```

A small window should open if Tkinter is installed correctly.

---

## Running the Console Version

Open terminal in the project directory:

```bash
python bank.py
```

Example:

```text
===== XYZ BANK =====

1. Create Account
2. Login
0. Exit
```

---

## Running the GUI Version

Open terminal in the project directory:

```bash
python gui.py
```

This will launch the graphical banking application.

---

## Banking Workflow

### Create Account

1. Select Create Account
2. Enter Username
3. Enter PIN
4. Confirm PIN

### Login

1. Enter Username
2. Enter PIN
3. Access banking menu

### Deposit

1. Enter amount
2. Balance increases

### Withdraw

1. Enter amount
2. Balance decreases if sufficient funds exist

### Transaction History

Displays all recorded actions:

```text
Login
Deposit: 500
Withdraw: 200
Logout
```

---

## Learning Objectives

This project demonstrates:

### Python Fundamentals

* Variables
* Data Types
* Loops
* Conditional Statements
* Functions

### Object-Oriented Programming

* Classes
* Objects
* Methods
* Constructors (`__init__`)
* Instance Variables

### GUI Programming

Using Tkinter:

* Labels
* Buttons
* Entry Widgets
* Message Boxes
* Event Handling

### Software Design

Separating:

```text
GUI
  ↓
Business Logic
```

The GUI interacts with the BankAccount class instead of implementing banking logic directly.

---

## Future Improvements

Possible enhancements:

* Multiple User Accounts
* Account Numbers
* Transaction IDs
* Transfer Between Accounts
* JSON Data Storage
* CSV Export
* Login Attempt Limits
* Password Hashing
* Interest Calculation
* Admin Dashboard
* Modern GUI Design

---

## Author

Created as a Python learning project for practicing programming, debugging, object-oriented programming, and GUI development.

Happy Coding! 🚀
