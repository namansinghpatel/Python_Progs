from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QMessageBox
from PyQt6.QtCore import Qt
from Backend.auth_service import login_user


class LoginPage(QWidget):

    def __init__(self, stack):

        super().__init__()

        self.stack = stack

        layout = QVBoxLayout()

        title = QLabel("🏦 XYZ Banking System")
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        title.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #1565C0;
                padding: 15px;
            }
        """)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")

        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        login_btn = QPushButton("Login")

        create_btn = QPushButton("Create New Account")

        login_btn.clicked.connect(self.login_clicked)

        create_btn.clicked.connect(self.create_account_clicked)

        layout.addWidget(title)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(login_btn)
        layout.addWidget(create_btn)

        self.setLayout(layout)

    def login_clicked(self):

        username = self.username.text()

        password = self.password.text()

        success, message = login_user(username, password)

        if success:

            QMessageBox.information(self, "Success", message)

            self.stack.setCurrentIndex(2)

        else:

            QMessageBox.warning(self, "Login Failed", message)

    def create_account_clicked(self):

        self.stack.setCurrentIndex(1)
