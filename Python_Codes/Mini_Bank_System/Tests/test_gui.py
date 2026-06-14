from GUI.login_page import LoginPage
from GUI.create_account_page import CreateAccountPage
from GUI.welcome_page import WelcomePage


def test_login_page_creation(qtbot):
    page = LoginPage(None)
    qtbot.addWidget(page)
    assert page is not None


def test_create_account_page_creation(qtbot):
    page = CreateAccountPage(None)
    qtbot.addWidget(page)
    assert page is not None


def test_welcome_page_creation(qtbot):
    page = WelcomePage(None)
    qtbot.addWidget(page)
    assert page is not None


def test_login_username_field_exists(qtbot):
    page = LoginPage(None)
    qtbot.addWidget(page)
    assert page.username is not None


def test_login_password_field_exists(qtbot):
    page = LoginPage(None)
    qtbot.addWidget(page)
    assert page.password is not None


def test_create_account_username_field_exists(qtbot):
    page = CreateAccountPage(None)
    qtbot.addWidget(page)
    assert page.username is not None


def test_create_account_password_field_exists(qtbot):
    page = CreateAccountPage(None)
    qtbot.addWidget(page)
    assert page.password is not None


def test_create_account_repassword_field_exists(qtbot):
    page = CreateAccountPage(None)
    qtbot.addWidget(page)
    assert page.repassword is not None
