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
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)
        self.show_login()

    def show_login(self):
        self.username_label = QtWidgets.QLabel("Username:")
        self.password_label = QtWidgets.QLabel("Password:")
        self.username_input = QtWidgets.QLineEdit()
        self.password_input = QtWidgets.QLineEdit()
        self.login_button = QtWidgets.QPushButton("Login")
        self.sign_up = QtWidgets.QPushButton("Sign up")
        self.cancel = QtWidgets.QPushButton("Cancel")

        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)

        self.grid.addWidget(self.username_label, 1, 1)
        self.grid.addWidget(self.username_input, 2, 1, 1, 4)
        self.grid.addWidget(self.password_label, 3, 1)
        self.grid.addWidget(self.password_input, 4, 1, 1, 4)
        self.grid.addWidget(self.login_button, 5, 1, 1, 2)
        self.grid.addWidget(self.sign_up, 5, 3, 1, 2)
        self.grid.addWidget(self.cancel, 6, 1, 1, 4)

        self.login_button.clicked.connect(self.login_btn)
        self.cancel.clicked.connect(self.cancel_btn)
        self.sign_up.clicked.connect(self.show_sign_up)

        self.connect()

    def show_sign_up(self):
        self.clear()

        self.username_label = QtWidgets.QLabel("Username:")
        self.password_label_repeat = QtWidgets.QLabel("Repeat password:")

        self.username_input = QtWidgets.QLineEdit()
        self.password_input = QtWidgets.QLineEdit()
        self.password_input_repeat = QtWidgets.QLineEdit()

        self.login_button = QtWidgets.QPushButton("Login")
        self.sign_up = QtWidgets.QPushButton("Sign up")
        self.cancel = QtWidgets.QPushButton("Cancel")

        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)

        self.grid.addWidget(self.username_label, 1, 1)
        self.grid.addWidget(self.username_input, 2, 1)
        self.grid.addWidget(self.password_label, 3, 1)
        self.grid.addWidget(self.password_input, 4, 1)
        self.grid.addWidget(self.password_label_repeat, 5, 1)
        self.grid.addWidget(self.password_input_repeat, 6, 1)
        self.grid.addWidget(self.sign_up, 7, 1)
        self.grid.addWidget(self.cancel, 8, 1)

        self.cancel.clicked.connect(self.cancel_btn)
        self.sign_up.clicked.connect(self.sign_up_btn)

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

    def sign_up_btn(self):
        try:
            self.TCP_Session.send_data({
                        "client": "sign_up",
                        "username": self.username_input.text(),
                        "password": self.password_input.text(),
                        "temp_id": random.randint(1, 100)
            })
            print(self.TCP_Session.get_data())
        except ssl.SSLEOFError:
            InfoBox("Connection lost", QtWidgets.QMessageBox.Icon.Critical)
            sys.exit()

    def cancel_btn(self):
        try:
            self.TCP_Session.send_data({
                "client": "DISCONNECT",
            })
            print(self.TCP_Session.get_data())
        except ssl.SSLEOFError:
            InfoBox("Connection lost", QtWidgets.QMessageBox.Icon.Critical)
        finally:
            sys.exit()

    def clear(self):
        for i in reversed(range(self.layout().count())):
            self.layout().itemAt(i).widget().setParent(None)

    def closeEvent(self, event):
        try:
            self.TCP_Session.send_data({
                "client": "DISCONNECT",
            })
            print(self.TCP_Session.get_data())
        except ssl.SSLEOFError:
            InfoBox("Connection lost", QtWidgets.QMessageBox.Icon.Critical)
        finally:
            event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
