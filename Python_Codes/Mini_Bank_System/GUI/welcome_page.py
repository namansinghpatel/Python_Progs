from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout


class WelcomePage(QWidget):

    def __init__(self, stack):

        super().__init__()

        self.stack = stack

        layout = QVBoxLayout()

        title = QLabel("Welcome To XYZ Banking System")

        logout_btn = QPushButton("Logout")

        logout_btn.clicked.connect(self.logout_clicked)

        layout.addWidget(title)
        layout.addWidget(logout_btn)

        self.setLayout(layout)

    def logout_clicked(self):

        self.stack.setCurrentIndex(0)
