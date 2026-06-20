from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout

from PyQt6.QtCore import Qt


class WelcomePage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.setWindowTitle("XYZ Banking System")
        self.setMinimumSize(700, 500)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        # ------------------------
        # Title
        # ------------------------
        title = QLabel("🏦 Welcome To XYZ Banking System")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #1565C0;
            margin: 20px;
            """)
        # ------------------------
        # Button Grid
        # ------------------------
        grid = QGridLayout()
        self.check_balance_btn = QPushButton("💰 Check Balance")
        self.deposit_btn = QPushButton("➕ Deposit")
        self.withdraw_btn = QPushButton("💸 Withdraw")
        self.transfer_btn = QPushButton("🔄 Transfer")
        buttons = [
            self.check_balance_btn,
            self.deposit_btn,
            self.withdraw_btn,
            self.transfer_btn,
        ]
        for button in buttons:
            button.setMinimumHeight(80)
            button.setStyleSheet("""
                QPushButton
                {
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 10px;
                    background-color: #1565C0;
                    color: white;
                }
                QPushButton:hover
                {
                    background-color: #1976D2;
                }
                """)

        grid.addWidget(self.check_balance_btn, 0, 0)
        grid.addWidget(self.deposit_btn, 0, 1)
        grid.addWidget(self.withdraw_btn, 1, 0)
        grid.addWidget(self.transfer_btn, 1, 1)
        main_layout.addStretch()
        main_layout.addWidget(title)
        main_layout.addLayout(grid)
        main_layout.addStretch()
        self.setLayout(main_layout)
