from Backend.validators import validate_username, validate_passwords, validate_login
from Database.mongodb import mongodb
from Database.sqlitedb import sqlitedb
from Backend.security import hash_password


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

    valid, message = validate_login(username, password)

    if not valid:
        return (False, message)

    authenticated = sqlitedb.authenticate_user(username, password)

    if not authenticated:
        return (False, "Invalid Username or Password")

    return (True, "Login Successful")
