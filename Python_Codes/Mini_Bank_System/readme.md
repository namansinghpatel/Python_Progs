# 🏦 XYZ Bank - Banking System (PyQt6)

A desktop banking application developed in Python using PyQt6.

This project is being built in multiple phases to learn:

* Python Programming
* Object-Oriented Programming (OOP)
* GUI Development with PyQt6
* Authentication Systems
* Database Integration
* Software Architecture
* Virtual Environments
* Git & GitHub Workflows

---

# 🚀 Current Features

### GUI Screens

* Login Page
* Create Account Page
* Welcome Page

### Navigation

* Login → Welcome Page
* Create Account → Login Page
* Logout → Login Page

### Architecture

* Modular Folder Structure
* GUI Layer
* Backend Layer
* Database Layer

---

# 📂 Project Structure

```text
XYZ_Bank/
│
├── main.py
│
├── gui/
│   ├── __init__.py
│   ├── login_page.py
│   ├── create_account_page.py
│   └── welcome_page.py
│
├── backend/
│   └── __init__.py
│
├── database/
│   └── __init__.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🖥️ Prerequisites

* Python 3.10 or newer

Verify installation:

```bash
python --version
```

Example:

```text
Python 3.12.4
```

---

# 🔧 Setup Project

## 1. Clone Repository

```bash
git clone https://github.com/namansinghpatel/Python_Progs.git
```

Move into the project folder:

```bash
cd Python_Progs/Python_Codes/Mini_Bank_System
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
```

### Linux / macOS

```bash
python3 -m venv venv
```

This creates:

```text
venv/
```

which contains an isolated Python environment for the project.

---

## 3. Activate Virtual Environment

### Windows CMD

```bash
venv\Scripts\activate
```

### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
source venv/bin/activate
```

After activation, you should see:

```text
(venv)
```

at the beginning of your terminal prompt.

Example:

```text
(venv) C:\Projects\XYZ_Bank>
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

Current dependencies:

```text
PyQt6>=6.8.0
```

---

## 5. Verify Installation

```bash
pip list
```

Expected output includes:

```text
PyQt6
PyQt6-Qt6
PyQt6-sip
```

---

# ▶️ Run Application

Start the application:

```bash
python main.py
```

---

# 🖼️ Application Flow

```text
Login Page
     │
     ├── Login
     │
     ▼
Welcome Page

Login Page
     │
     ├── Create Account
     │
     ▼
Create Account Page
     │
     ▼
Back To Login Page
```

---

# 🧠 Learning Objectives

This project demonstrates:

## Python

* Classes
* Objects
* Functions
* Modules
* Packages
* Virtual Environments

## PyQt6

* QStackedWidget
* QPushButton
* QLabel
* QLineEdit
* Event Handling

## Software Design

```text
GUI Layer
     ↓
Backend Layer
     ↓
Database Layer
```

Each layer has a specific responsibility.

---

# 🔮 Future Roadmap

## Phase 2

* Input Validation
* Password Validation
* Error Dialogs

## Phase 3

* SQLite Database
* User Registration
* User Authentication

## Phase 4

* Dashboard
* Account Details

## Phase 5

* Deposit Money
* Withdraw Money
* Transfer Money

## Phase 6

* Transaction History

## Phase 7

* Password Hashing

## Phase 8

* Admin Dashboard

---

# 🛠️ Useful Development Commands

## Update Requirements File

After installing new packages:

```bash
pip freeze > requirements.txt
```

---

## Deactivate Virtual Environment

```bash
deactivate
```

---

## Remove Virtual Environment

Delete:

```text
venv/
```

folder.

Then recreate it:

```bash
python -m venv venv
```

---

# 👨‍💻 Author

Naman Singh Patel

GitHub:
https://github.com/namansinghpatel

---

# 📜 License

This project is created for learning and educational purposes.

Feel free to fork, modify, and experiment with the code.

---

⭐ If you found this project useful, consider starring the repository.
