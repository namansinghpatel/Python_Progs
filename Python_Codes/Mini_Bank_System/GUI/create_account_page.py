from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout
from PyQt6.QtWidgets import QMessageBox
from Backend.auth_service import create_user


class CreateAccountPage(QWidget):

    def __init__(self, stack):

        super().__init__()

        self.stack = stack

        layout = QVBoxLayout()

        title = QLabel("Create New Account")

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")

        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        self.repassword = QLineEdit()
        self.repassword.setPlaceholderText("Re-enter Password")

        self.repassword.setEchoMode(QLineEdit.EchoMode.Password)

        submit_btn = QPushButton("Submit")

        submit_btn.clicked.connect(self.submit_clicked)

        layout.addWidget(title)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.repassword)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    def submit_clicked(self):

        username = self.username.text()
        password = self.password.text()
        re_password = self.repassword.text()
        success, message = create_user(username, password, re_password)

        if success:
            QMessageBox.information(self, "Success", message)
            self.stack.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "Validation Error", message)
