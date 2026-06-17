from Backend.validators import validate_username, validate_passwords, validate_login
from Database.mongodb import mongodb
from Database.sqlitedb import sqlitedb
from Backend.security import hash_password, verify_password
from datetime import datetime, timedelta


def create_user(username, password, re_password):

    # -------------------
    # Username Validation
    # -------------------

    valid, message = validate_username(username)

    if not valid:
        return (False, message)

    # -------------------
    # Password Validation
    # -------------------

    valid, message = validate_passwords(password, re_password)

    if not valid:
        return (False, message)

    # -------------------
    # Username Exists?
    # -------------------

    if sqlitedb.user_exists(username):
        return (False, "Username already exists")

    # -------------------
    # Create User
    # -------------------

    password_hash = hash_password(password)
    sqlitedb.create_user(username, password_hash)
    return (True, "Account Created Successfully")


def login_user(username, password):

    # -------------------------
    # Validate Input
    # -------------------------
    valid, message = validate_login(username, password)
    if not valid:
        return (False, message)
    # -------------------------
    # Check Lock Status
    # -------------------------
    locked_until = sqlitedb.get_locked_until(username)
    if locked_until:
        locked_until = datetime.fromisoformat(locked_until)
        current_time = datetime.now()
        if current_time < locked_until:
            remaining_seconds = int((locked_until - current_time).total_seconds())
            return (False, f"Account locked. Try again in {remaining_seconds} seconds.")
    # -------------------------
    # Get Stored Hash
    # -------------------------
    stored_hash = sqlitedb.get_user_password_hash(username)
    if stored_hash is None:
        return (False, "Invalid Username or Password")
    # -------------------------
    # Verify Password
    # -------------------------
    if not verify_password(password, stored_hash):
        attempts = sqlitedb.get_failed_attempts(username)
        attempts += 1
        sqlitedb.update_failed_attempts(username, attempts)
        # -------------------------
        # Lock Account After 3 Attempts
        # -------------------------
        if attempts >= 3:
            lock_until = datetime.now() + timedelta(minutes=1)
            sqlitedb.lock_user(username, lock_until.isoformat())
            return (
                False,
                "Account locked for 1 minute due to multiple failed login attempts.",
            )
        return (
            False,
            f"Invalid Username or Password. Attempts remaining: {3 - attempts}",
        )
    # -------------------------
    # Successful Login
    # -------------------------
    sqlitedb.reset_login_attempts(username)
    return (True, "Login Successful")
