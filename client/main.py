import ssl
import sys
from PyQt5 import QtWidgets

from objects.C_TCP_Session import TCPSession
from objects.C_Infobox import InfoBox
from objects.C_MainWindow import MainWindow


class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.TCP_Session = None
        self.setWindowTitle("YeGrec's Login Page")
        self.setGeometry(100, 100, 400, 225)
        self.setStyleSheet(self.css_loader('../client/styles/styles.css'))
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)
        self.show_login()
        self.connect()

    def show_login(self):
        username_label = QtWidgets.QLabel("Username")
        password_label = QtWidgets.QLabel("Password")
        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setText("valentin")
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setText("azerty68")
        login_button = QtWidgets.QPushButton("Login")
        sign_up_button = QtWidgets.QPushButton("Sign up")
        quit_button = QtWidgets.QPushButton("Quit")

        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)

        self.grid.addWidget(username_label, 1, 1)
        self.grid.addWidget(self.username_input, 2, 1, 1, 4)
        self.grid.addWidget(password_label, 3, 1)
        self.grid.addWidget(self.password_input, 4, 1, 1, 4)
        self.grid.addWidget(login_button, 5, 1, 1, 2)
        self.grid.addWidget(sign_up_button, 5, 3, 1, 2)
        self.grid.addWidget(quit_button, 6, 1, 1, 4)

        login_button.clicked.connect(self.login_action)
        quit_button.clicked.connect(self.quit_action)
        sign_up_button.clicked.connect(self.show_sign_up)

    def show_sign_up(self):
        self.clear()

        username_label = QtWidgets.QLabel("Username")
        password_label = QtWidgets.QLabel("Password")
        password_label_repeat = QtWidgets.QLabel("Repeat password")
        self.username_input = QtWidgets.QLineEdit()
        self.password_input = QtWidgets.QLineEdit()
        self.password_input_repeat = QtWidgets.QLineEdit()
        login_button = QtWidgets.QPushButton("Login")
        sign_up_button = QtWidgets.QPushButton("Sign up")
        cancel_button = QtWidgets.QPushButton("Cancel")

        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input_repeat.setEchoMode(QtWidgets.QLineEdit.Password)

        self.grid.addWidget(username_label, 1, 1)
        self.grid.addWidget(self.username_input, 2, 1)
        self.grid.addWidget(password_label, 3, 1)
        self.grid.addWidget(self.password_input, 4, 1)
        self.grid.addWidget(password_label_repeat, 5, 1)
        self.grid.addWidget(self.password_input_repeat, 6, 1)
        self.grid.addWidget(sign_up_button, 7, 1)
        self.grid.addWidget(cancel_button, 8, 1)

        cancel_button.clicked.connect(self.cancel_action)
        sign_up_button.clicked.connect(self.sign_up_action)

    def show_main_window(self):
        self.main_window = MainWindow(self.TCP_Session)
        self.main_window.show()

    def login_action(self):
        try:
            self.TCP_Session.send_data({
                        "client": "login",
                        "username": self.username_input.text(),
                        "password": self.password_input.text(),
            })
            response = self.TCP_Session.get_data()
            print(response)
        except ssl.SSLEOFError:
            InfoBox("Connection lost", QtWidgets.QMessageBox.Icon.Critical)
            sys.exit()

        if response["success"] == "no":
            if response["error"] == "BadPasswordOrUsername":
                InfoBox("Login error", QtWidgets.QMessageBox.Icon.Warning)
            elif response["error"] == "InvalidJSONFormat":
                InfoBox("Client send an incorrect request", QtWidgets.QMessageBox.Icon.Critical)
                self.quit_action()
            elif response["error"] == "InternalError":
                InfoBox("Internal error from server", QtWidgets.QMessageBox.Icon.Critical)
                self.quit_action()
        elif response["success"] == "yes":
            self.hide()
            self.show_main_window()

    def sign_up_action(self):
        if self.password_input.text() != self.password_input_repeat.text():
            return InfoBox("Passwords don't match", QtWidgets.QMessageBox.Icon.Warning)

        try:
            self.TCP_Session.send_data({
                        "client": "sign_up",
                        "username": self.username_input.text(),
                        "password": self.password_input.text(),
            })
            response = self.TCP_Session.get_data()
            print(response)
        except ssl.SSLEOFError:
            InfoBox("Connection lost", QtWidgets.QMessageBox.Icon.Critical)
            sys.exit()

        if response["success"] == "no":
            if response["error"] == "BadUsername":
                InfoBox("Wrong username", QtWidgets.QMessageBox.Icon.Warning)
            elif response["error"] == "BadPassword":
                InfoBox("Password not strong", QtWidgets.QMessageBox.Icon.Warning)
            elif response["error"] == "AccountAlreadyExist":
                InfoBox("Account already exist", QtWidgets.QMessageBox.Icon.Warning)
            elif response["error"] == "AccountAlreadyExist":
                InfoBox("Account already exist", QtWidgets.QMessageBox.Icon.Warning)
            elif response["error"] == "InvalidJSONFormat":
                InfoBox("Client send an incorrect request", QtWidgets.QMessageBox.Icon.Critical)
                self.quit_action()
            elif response["error"] == "InternalError":
                InfoBox("Internal error from server", QtWidgets.QMessageBox.Icon.Critical)
                self.quit_action()
        elif response["success"] == "yes":
            InfoBox("Account created", QtWidgets.QMessageBox.Icon.Information)

    def quit_action(self):
        try:
            self.TCP_Session.send_data({
                "client": "DISCONNECT",
            })
            print(self.TCP_Session.get_data())
        except ssl.SSLEOFError:
            InfoBox("Connection lost", QtWidgets.QMessageBox.Icon.Critical)
        finally:
            sys.exit()

    def cancel_action(self):
        self.clear()
        self.show_login()

    def connect(self):
        try:
            self.TCP_Session = TCPSession("127.0.0.1", 5000)
        except ConnectionRefusedError:
            InfoBox("Connection error", QtWidgets.QMessageBox.Icon.Critical)
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

    @staticmethod
    def css_loader(filename):
        with open(filename, 'r') as rd:
            content = rd.read()
            rd.close()
        return content


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
