from Backend.auth_service import create_user, login_user
from unittest.mock import patch


@patch("Backend.auth_service.sqlitedb")
def test_create_new_user(mock_db):
    mock_db.user_exists.return_value = False
    success, message = create_user("new_user_1", "password123", "password123")
    assert success
    assert message == "Account Created Successfully"
    mock_db.user_exists.assert_called_once_with("new_user_1")
    mock_db.create_user.assert_called_once()


@patch("Backend.auth_service.sqlitedb")
def test_create_duplicate_user(mock_db):
    mock_db.user_exists.return_value = True
    success, message = create_user("duplicate_user", "password123", "password123")
    assert not success
    assert message == "Username already exists"
    mock_db.user_exists.assert_called_once_with("duplicate_user")
    mock_db.create_user.assert_not_called()


@patch("Backend.auth_service.sqlitedb")
def test_create_user_password_mismatch(mock_db):
    success, message = create_user("userx", "password123", "password321")
    assert not success
    mock_db.user_exists.assert_not_called()
    mock_db.create_user.assert_not_called()


@patch("Backend.auth_service.sqlitedb")
def test_create_user_short_username(mock_db):
    success, message = create_user("ab", "password123", "password123")
    assert not success
    mock_db.user_exists.assert_not_called()
    mock_db.create_user.assert_not_called()


@patch("Backend.auth_service.sqlitedb")
def test_create_user_short_password(mock_db):
    success, message = create_user("prashant", "123", "123")
    assert not success
    mock_db.user_exists.assert_not_called()
    mock_db.create_user.assert_not_called()


@patch("Backend.auth_service.sqlitedb")
def test_create_user_success(mock_db):
    mock_db.user_exists.return_value = False
    success, message = create_user("new_user", "password123", "password123")
    assert success
    assert message == "Account Created Successfully"
    mock_db.user_exists.assert_called_once_with("new_user")
    mock_db.create_user.assert_called_once()
    username, hashed_password = mock_db.create_user.call_args.args
    assert username == "new_user"
    assert hashed_password != "password123"
    assert hashed_password.startswith("$2b$")


@patch("Backend.auth_service.sqlitedb")
def test_create_user_database_failure(mock_db):
    mock_db.user_exists.return_value = False
    mock_db.create_user.side_effect = Exception("Database Down")
    try:
        create_user("new_user", "password123", "password123")
        assert False
    except Exception as e:
        assert str(e) == "Database Down"


@patch("Backend.auth_service.sqlitedb")
def test_login_success(mock_db):
    mock_db.authenticate_user.return_value = True
    success, message = login_user("login_user", "password123")
    assert success
    assert message == "Login Successful"
    mock_db.authenticate_user.assert_called_once_with("login_user", "password123")


@patch("Backend.auth_service.sqlitedb")
def test_login_wrong_password(mock_db):
    mock_db.authenticate_user.return_value = False
    success, message = login_user("login_user2", "wrongpassword")
    assert not success
    assert message == "Invalid Username or Password"


@patch("Backend.auth_service.sqlitedb")
def test_login_unknown_user(mock_db):
    mock_db.authenticate_user.return_value = False
    success, message = login_user("unknown_user", "password123")
    assert not success
    assert message == "Invalid Username or Password"


@patch("Backend.auth_service.sqlitedb")
def test_login_empty_username(mock_db):
    success, message = login_user("", "password123")
    assert not success
    mock_db.authenticate_user.assert_not_called()


@patch("Backend.auth_service.sqlitedb")
def test_login_empty_password(mock_db):
    success, message = login_user("prashant", "")
    assert not success
    mock_db.authenticate_user.assert_not_called()


@patch("Backend.auth_service.sqlitedb")
def test_login_database_success(mock_db):
    mock_db.authenticate_user.return_value = True
    success, _ = login_user("prashant", "password123")
    assert success


@patch("Backend.auth_service.sqlitedb")
def test_login_database_failure(mock_db):
    mock_db.authenticate_user.side_effect = Exception("Database Down")
    try:
        login_user("prashant", "password123")
        assert False
    except Exception as e:
        assert str(e) == "Database Down"
