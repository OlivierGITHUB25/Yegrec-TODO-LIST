import ssl
import sys
import socket
from PyQt5 import QtWidgets

from objects.C_TCP_Session import TCPSession
from objects.C_Widgets import InfoBox
from objects.C_MainWindow import MainWindow


class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.TCP_Session = None
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)
        self.init_connect()

    def init_connect(self):
        try:
            with open("server_address", "r") as file:
                for line in file:
                    address, port = line.split(":")
            self.TCP_Session = TCPSession(address, port)
        except ConnectionRefusedError:
            InfoBox("Connection error", QtWidgets.QMessageBox.Icon.Critical)
            sys.exit()
        except (UnboundLocalError, socket.gaierror):
            InfoBox("Wrong server address", QtWidgets.QMessageBox.Icon.Critical)
            sys.exit()
        else:
            self.show_login()

    def show_login(self):
        self.setWindowTitle("YeGrec's Login Page")
        self.setGeometry(0, 0, 400, 225)
        self.setStyleSheet(self.css_loader('../client/styles/styles.css'))
        self.center_window()

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

        login_button.clicked.connect(self.action_login)
        quit_button.clicked.connect(self.action_quit)
        sign_up_button.clicked.connect(self.show_sign_up)

    def show_sign_up(self):
        self.clear_widget()

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

        cancel_button.clicked.connect(self.action_cancel)
        sign_up_button.clicked.connect(self.action_sign_up)

    def show_main_window(self):
        self.main_window = MainWindow(self.TCP_Session)
        self.main_window.show()

    def action_login(self):
        if self.username_input.text() == "" or self.password_input.text() == "":
            return InfoBox("Username or password is blank", QtWidgets.QMessageBox.Icon.Warning)

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
            elif response["error"] == "InternalError":
                InfoBox("Internal error from server", QtWidgets.QMessageBox.Icon.Critical)
            self.action_quit()
        elif response["success"] == "yes":
            self.hide()
            self.show_main_window()

    def action_sign_up(self):
        if self.username_input.text() == "" or self.password_input.text() == "" or self.password_input_repeat.text() == "":
            return InfoBox("Username or password is blank", QtWidgets.QMessageBox.Icon.Warning)
        elif self.password_input.text() != self.password_input_repeat.text():
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
                self.action_quit()
            elif response["error"] == "InternalError":
                InfoBox("Internal error from server", QtWidgets.QMessageBox.Icon.Critical)
                self.action_quit()
        elif response["success"] == "yes":
            InfoBox("Account created", QtWidgets.QMessageBox.Icon.Information)
            self.action_cancel()

    def action_quit(self):
        try:
            self.TCP_Session.send_data({
                "client": "DISCONNECT",
            })
            print(self.TCP_Session.get_data())
        except ssl.SSLEOFError:
            InfoBox("Connection lost", QtWidgets.QMessageBox.Icon.Critical)
        finally:
            sys.exit()

    def action_cancel(self):
        self.clear_widget()
        self.show_login()

    def clear_widget(self):
        for i in reversed(range(self.layout().count())):
            self.layout().itemAt(i).widget().setParent(None)

    def closeEvent(self, event, **kwargs):
        try:
            self.TCP_Session.send_data({
                "client": "DISCONNECT",
            })
            print(self.TCP_Session.get_data())
        except ssl.SSLEOFError:
            InfoBox("Connection lost", QtWidgets.QMessageBox.Icon.Critical)
        finally:
            event.accept()

    def center_window(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

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
