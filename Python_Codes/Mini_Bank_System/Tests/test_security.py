from Backend.security import hash_password, verify_password


def test_hash_password():
    hashed = hash_password("password123")
    assert hashed != "password123"


def test_verify_password_success():
    hashed = hash_password("password123")
    assert verify_password("password123", hashed)


def test_verify_password_failure():
    hashed = hash_password("password123")
    assert not verify_password("wrongpassword", hashed)
