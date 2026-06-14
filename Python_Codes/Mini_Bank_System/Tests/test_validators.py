from Backend.validators import validate_username, validate_passwords, validate_login


def test_valid_username():
    valid, _ = validate_username("prashant")
    assert valid


def test_empty_username():
    valid, _ = validate_username("")
    assert not valid


def test_spaces_username():
    valid, _ = validate_username("   ")
    assert not valid


def test_short_username():
    valid, _ = validate_username("ab")
    assert not valid


def test_username_length_3():
    valid, _ = validate_username("abc")
    assert valid


def test_valid_passwords():
    valid, _ = validate_passwords("password123", "password123")
    assert valid


def test_password_mismatch():
    valid, _ = validate_passwords("password123", "password321")
    assert not valid


def test_empty_password():
    valid, _ = validate_passwords("", "")
    assert not valid


def test_short_password():
    valid, _ = validate_passwords("pass", "pass")
    assert not valid


def test_password_exactly_8_chars():
    valid, _ = validate_passwords("12345678", "12345678")
    assert valid


def test_valid_login():
    valid, _ = validate_login("prashant", "password123")
    assert valid


def test_login_short_username():
    valid, _ = validate_login("ab", "password123")
    assert not valid


def test_login_short_password():
    valid, _ = validate_login("prashant", "123")
    assert not valid
