import ssl
import sys
import json
import socket
import threading
import time

from PyQt5 import QtWidgets
import random


class TCPSession:
    def __init__(self, hostname, port):
        self.__hostname = hostname
        self.__port = port
        self.__context = ssl.create_default_context()
        self.__context.load_verify_locations("./certs/CA.crt")
        self.__data = None
        self.__connected = False
        self.__init_connection()

    def init_connection(self):
        connection = threading.Thread(target=self.__init_connection)
        connection.start()

    def __init_connection(self):
        tcp_sock = socket.create_connection((self.__hostname, self.__port))
        self.__conn = self.__context.wrap_socket(tcp_sock, server_hostname=self.__hostname)
        self.__connected = True
        rcv_data = threading.Thread(target=self.__receive_data)
        rcv_data.start()

    def __receive_data(self):
        if self.__connected:
            previous_msg = ""
            while self.__data != "DISCONNECT":
                buffer = self.__conn.recv(1024)
                if previous_msg != self.__data:
                    self.__data = buffer.decode('utf-8')
                    print(self.__data)
                    previous_msg = self.__data

    def send_data(self, data):
        thread = threading.Thread(target=self.__send_data, args=[data])
        thread.start()

    def __send_data(self, data):
        if self.__connected:
            self.__conn.send(data.encode('utf-8'))

    def get_data(self):
        if self.__connected:
            time.sleep(0.3)
            while self.__data is None:
                continue
            data = self.__data
            self.__data = None
            return data


class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.TCP_Session = None
        self.show_gui()

    def show_gui(self):
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

        try:
            self.TCP_Session = TCPSession("127.0.0.1", 5000)
        except ConnectionRefusedError:
            InfoBox("Connection error", QtWidgets.QMessageBox.Icon.Critical)
            sys.exit()

    def login_btn(self):
        try:
            self.TCP_Session.send_data(json.dumps([
                {
                        "client": "login",
                        "username": self.username_input.text(),
                        "password": self.password_input.text(),
                        "temp_id": random.randint(1, 100)
                }
            ]))
            response = self.TCP_Session.get_data()
            #response = json.loads(response)
        except ssl.SSLEOFError:
            InfoBox("Connection lost", QtWidgets.QMessageBox.Icon.Critical)
            sys.exit()

    def cancel_btn(self):
        self.TCP_Session.send_data(json.dumps([
            {
                "client": "DISCONNECT",
            }
        ]))
        sys.exit()


class InfoBox(QtWidgets.QMessageBox):
    def __init__(self, message: str, event_type: QtWidgets.QMessageBox.Icon):
        super().__init__()
        self.setText(message)
        self.setWindowTitle("Information")
        self.setIcon(event_type)
        self.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
