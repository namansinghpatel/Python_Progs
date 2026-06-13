from Backend.validators import validate_username, validate_passwords
from Database.mongodb import mongodb
from Database.sqlitedb import sqlitedb


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

    sqlitedb.create_user(username, password)
    return (True, "Account Created Successfully")
