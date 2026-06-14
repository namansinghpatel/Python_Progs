from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt
from Backend.auth_service import create_user


class CreateAccountPage(QWidget):

    def __init__(self, stack):

        super().__init__()

        self.stack = stack

        layout = QVBoxLayout()

        title = QLabel("➕ CREATE NEW ACCOUNT")
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        title.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #C62828;
                padding: 15px;
            }
        """)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        self.show_password_btn = QPushButton("👁")
        self.show_password_btn.clicked.connect(self.toggle_password)

        self.repassword = QLineEdit()
        self.repassword.setPlaceholderText("Re-enter Password")
        self.repassword.setEchoMode(QLineEdit.EchoMode.Password)

        submit_btn = QPushButton("Submit")
        submit_btn.clicked.connect(self.submit_clicked)

        back_btn = QPushButton("⬅️ Back")

        back_btn.clicked.connect(self.back_clicked)

        layout.addWidget(title)
        layout.addWidget(self.username)
        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password)
        password_layout.addWidget(self.show_password_btn)
        layout.addLayout(password_layout)
        layout.addWidget(self.repassword)
        layout.addWidget(submit_btn)
        layout.addWidget(back_btn)
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

    def back_clicked(self):
        self.stack.setCurrentIndex(0)

    def toggle_password(self):
        if self.password.echoMode() == QLineEdit.EchoMode.Password:
            self.password.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_password_btn.setText("🙈")

        else:
            self.password.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_password_btn.setText("👁")
