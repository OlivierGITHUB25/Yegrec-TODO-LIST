import ssl
import sys
import json
import random
from PyQt5 import QtWidgets

from objects.C_TCP_Session import TCPSession
from objects.C_Infobox import InfoBox


class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.TCP_Session = None
        self.setWindowTitle("Login Page")
        self.setGeometry(100, 100, 300, 150)

        self.username_label = QtWidgets.QLabel("Username:")
        self.password_label = QtWidgets.QLabel("Password:")
        self.username_input = QtWidgets.QLineEdit()
        self.password_input = QtWidgets.QLineEdit()
        self.login_button = QtWidgets.QPushButton("Login")
        self.sign_in = QtWidgets.QPushButton("Sign Up")
        self.cancel = QtWidgets.QPushButton("Cancel")

        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)

        grid = QtWidgets.QGridLayout()
        grid.addWidget(self.username_label, 1, 1)
        grid.addWidget(self.username_input, 2, 1, 1, 4)
        grid.addWidget(self.password_label, 3, 1)
        grid.addWidget(self.password_input, 4, 1, 1, 4)
        grid.addWidget(self.login_button, 5, 1, 1, 2)
        grid.addWidget(self.sign_in, 5, 3, 1, 2)
        grid.addWidget(self.cancel, 6, 1, 1, 4)

        self.login_button.clicked.connect(self.login_btn)
        self.cancel.clicked.connect(self.cancel_btn)

        self.setLayout(grid)
        self.connect()

    def connect(self):
        try:
            self.TCP_Session = TCPSession("127.0.0.1", 5000)
        except ConnectionRefusedError:
            InfoBox("Connection error", QtWidgets.QMessageBox.Icon.Critical)
            sys.exit()

    def login_btn(self):
        try:
            self.TCP_Session.send_data({
                        "client": "login",
                        "username": self.username_input.text(),
                        "password": self.password_input.text(),
                        "temp_id": random.randint(1, 100)
            })
            print(self.TCP_Session.get_data())
        except ssl.SSLEOFError:
            InfoBox("Connection lost", QtWidgets.QMessageBox.Icon.Critical)
            sys.exit()

    def cancel_btn(self):
        self.TCP_Session.send_data({
            "client": "DISCONNECT",
        })
        print(self.TCP_Session.get_data())
        sys.exit()

    def closeEvent(self, event):
        self.TCP_Session.send_data({
            "client": "DISCONNECT",
        })
        print(self.TCP_Session.get_data())
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
