# 🏦 Mini Bank System

A desktop banking application built with **Python**, **PyQt6**, **SQLite**, **bcrypt**, and **pytest**.

This project was created as a learning journey to understand how real-world applications are structured using:

* GUI Development
* Backend Services
* Database Management
* Authentication & Security
* Unit Testing
* Software Architecture

---

# 🚀 Features

## 🔐 User Authentication

* Create New Account
* Login with Username & Password
* Username Validation
* Password Validation
* Duplicate Username Detection
* Secure Password Storage using bcrypt

---

## 🛡️ Password Security

Passwords are **never stored in plain text**.

Example:

Instead of:

```text
password123
```

The database stores:

```text
$2b$12$Pc4Qd5YJ....
```

using bcrypt hashing.

### Benefits

* Passwords cannot be decrypted
* Salted hashing protects against rainbow-table attacks
* Industry-standard authentication approach

---

## 🖥️ GUI Features

### Login Page

* Username field
* Password field
* Show / Hide Password 👁
* Login Button
* Create New Account Button
* Exit Button

### Create Account Page

* Username field
* Password field
* Re-enter Password field
* Submit Button
* Back Button

### Welcome Page

Displays:

```text
🏦 Welcome to XYZ Banking System
```

after successful login.

---

# 📂 Project Structure

```text
Mini_Bank_System/

│
├── main.py
│
├── GUI/
│   ├── __init__.py
│   ├── login_page.py
│   ├── create_account_page.py
│   └── welcome_page.py
│
├── Backend/
│   ├── __init__.py
│   ├── auth_service.py
│   ├── validators.py
│   └── security.py
│
├── Database/
│   ├── __init__.py
│   ├── sqlite_db.py
│   └── xyz_bank.db
│
├── Tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth_service.py
│   ├── test_validators.py
│   ├── test_sqlite_db.py
│   └── test_gui.py
│
├── requirements.txt
│
├── .gitignore
│
└── README.md
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/namansinghpatel/Python_Progs/tree/main/Python_Codes/Mini_Bank_System
```

---

## Navigate To Project

```bash
cd Mini_Bank_System
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

---

### Linux / macOS

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

---

# 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Application

```bash
python main.py
```

---

# 🗄️ Database

This project uses SQLite.

Database file:

```text
Database/xyz_bank.db
```

SQLite automatically creates:

```text
users
```

table during application startup.

---

# 👤 User Registration Flow

```text
Create Account
      ↓
Validate Username
      ↓
Validate Password
      ↓
Check Duplicate User
      ↓
Hash Password (bcrypt)
      ↓
Store In Database
      ↓
Success Message
```

---

# 🔑 Login Flow

```text
Login
   ↓
Validate Input
   ↓
Fetch User Hash
   ↓
Verify Password (bcrypt)
   ↓
Success / Failure
```

---

# 🧪 Testing

The project includes automated testing using:

* pytest
* pytest-qt
* unittest.mock

---

## Run All Tests

```bash
pytest
```

---

## Run Tests Verbosely

```bash
pytest -v
```

---

## Run Specific Test File

```bash
pytest Tests/test_auth_service.py
```

---

# ✅ Test Coverage

### Validators

Tests:

* Valid Username
* Empty Username
* Username Length Validation
* Password Match Validation
* Password Length Validation
* Login Validation

---

### Authentication Service

Tests:

* Create User Success
* Duplicate User
* Password Mismatch
* Short Username
* Short Password
* Login Success
* Login Failure
* Unknown User
* Empty Username
* Empty Password
* Database Success
* Database Failure

---

### Database Layer

Tests:

* Insert User
* User Exists
* User Count
* Multiple Users
* Search Existing User
* Search Non-Existing User

---

### GUI

Tests:

* Login Page Creation
* Create Account Page Creation
* Welcome Page Creation
* Username Field Exists
* Password Field Exists
* Re-password Field Exists

---

# 🎭 Mocking Strategy

Authentication tests use a mocked database instead of the real database.

```text
Test
 ↓
Mock Database
 ↓
No Real SQLite Access
```

Benefits:

* Faster Tests
* Isolated Tests
* No Database Cleanup Required
* Reliable Results

---

# 🔒 Security

Implemented:

✅ bcrypt Password Hashing

Not Yet Implemented:

⬜ Password Complexity Rules

⬜ Account Lockout After Failed Attempts

⬜ Session Management

⬜ Role-Based Access Control

⬜ Encryption Of Sensitive Banking Data

---

# 📚 Concepts Learned

This project demonstrates:

* Object-Oriented Programming
* GUI Development with PyQt6
* SQLite Database Operations
* Authentication Systems
* Password Hashing
* Software Layering
* Dependency Isolation
* Mocking
* Unit Testing
* Integration Testing
* Virtual Environments
* Git Project Structure

---

# 🛠️ Future Enhancements

## Banking Features

* Deposit
* Withdraw
* Transfer Money
* Transaction History
* Account Balance

---

## Security Features

* Password Complexity Rules
* Forgot Password
* OTP Verification
* Account Lockout
* Encryption of Sensitive Data

---

## Database Features

* Transaction Table
* Account Table
* Foreign Key Relationships
* Audit Logs

---

## Testing Improvements

* 80%+ Test Coverage
* GUI Navigation Tests
* End-to-End Tests
* Performance Tests

---

# 👨‍💻 Author

Naman Singh Patel

Built as a learning project to understand how real-world banking systems are designed using Python.

---

⭐ If you found this project useful, consider starring the repository and following the project's future enhancements.
