def validate_username(username):

    if not username.strip():
        return (False, "Username cannot be empty")

    if len(username) < 3:
        return (False, "Username must be at least 3 characters")

    return (True, "Username Valid")


def validate_passwords(password, re_password):

    if not password:
        return (False, "Password cannot be empty")

    if password != re_password:
        return (False, "Password and Re-Password do not match")

    if len(password) < 8:
        return (False, "Password must contain at least 8 characters")

    return (True, "Password Valid")
