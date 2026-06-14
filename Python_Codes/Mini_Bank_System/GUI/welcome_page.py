from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt


class WelcomePage(QWidget):

    def __init__(self, stack):

        super().__init__()

        self.stack = stack

        layout = QVBoxLayout()

        title = QLabel("💰 Welcome To XYZ Banking System")
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        title.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #F9A825;
                padding: 15px;
            }
        """)

        logout_btn = QPushButton("Logout")

        logout_btn.clicked.connect(self.logout_clicked)

        layout.addWidget(title)
        layout.addWidget(logout_btn)

        self.setLayout(layout)

    def logout_clicked(self):

        self.stack.setCurrentIndex(0)
