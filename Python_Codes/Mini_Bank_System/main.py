import sys

from PyQt6.QtWidgets import QApplication, QStackedWidget

from GUI.login_page import LoginPage
from GUI.create_account_page import CreateAccountPage
from GUI.welcome_page import WelcomePage

app = QApplication(sys.argv)

stack = QStackedWidget()

login_page = LoginPage(stack)


create_account_page = CreateAccountPage(stack)

welcome_page = WelcomePage(stack)

stack.addWidget(login_page)
stack.addWidget(create_account_page)
stack.addWidget(welcome_page)

stack.setWindowTitle("XYZ Banking System")

stack.resize(500, 300)

stack.show()

sys.exit(app.exec())

if __name__ == "__main__":
    main()
