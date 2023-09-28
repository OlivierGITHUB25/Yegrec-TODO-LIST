from colorama import Fore, Style
import mysql.connector
import threading
import socket
import bcrypt
import json
import ssl
import sys
import re


class Client:
    def __init__(self, conn, cursor):
        self.__conn = conn
        self.__cursor = cursor
        self.__auth = False
        self.__user = ""

    def run(self):
        previous_msg = ""
        client_action = ""

        while client_action != "disconnect":
            buffer = self.__conn.recv(1024)
            received_message = buffer.decode('utf-8')
            if received_message != previous_msg:
                try:
                    output = json.loads(received_message)
                    for item in output:
                        client_action = item["client"]
                        previous_msg = received_message
                except KeyError:
                    print("Invalid json format")
                    previous_msg = received_message
                    continue
                except json.decoder.JSONDecodeError:
                    print("Invalid json format")
                    previous_msg = received_message
                    continue

                if client_action == "login":
                    self.login(output)
                elif client_action == "sign_up":
                    self.sign_up(output)
                elif client_action == "get_tasks":
                    self.get_tasks(output)

        print("A socket has been closed")

    def login(self, output):
        username = ""
        password = ""

        try:
            for item in output:
                username = item["username"]
                password = item["password"]
        except KeyError:
            print("Invalid json format")
            try:
                self.__conn.send(self.json_maker("response", "no", "InvalidJSONFormat").encode('utf-8'))
            except ssl.SSLEOFError:
                print('Client aborted connection')
            return -1

        with open("users.json", "r") as user_DB:
            _user_DB = json.load(user_DB)
            for item in _user_DB:
                if item["username"] == username:
                    if bcrypt.checkpw(password.encode('utf8'), item["password"].encode('utf8')):
                        print(f"User {username} is logged in !")
                        try:
                            self.__auth = True
                            self.__user = username
                            self.__conn.send(self.json_maker("response", "yes").encode('utf-8'))
                        except ssl.SSLEOFError:
                            print('Client aborted connection')
                        return 0
                    else:
                        print(f"{username} enter wrong password")
                        try:
                            self.__conn.send(self.json_maker("response", "no").encode('utf-8'))
                        except ssl.SSLEOFError:
                            print('Client aborted connection')
        try:
            self.__conn.send(self.json_maker("response", "no").encode('utf-8'))
        except ssl.SSLEOFError:
            print('Client aborted connection')

    def sign_up(self, output):
        username = ""
        password = ""

        try:
            for item in output:
                username = item["username"]
                password = item["password"]
        except KeyError:
            print("Invalid json format")
            try:
                self.__conn.send(self.json_maker("response", "no", "InvalidJSONFormat").encode('utf-8'))
            except ssl.SSLEOFError:
                print('Client aborted connection')
            return -1

        with open("users.json", "r") as user_DB:
            try:
                _user_DB = json.load(user_DB)
            except json.decoder.JSONDecodeError:
                _user_DB = []

        for item in _user_DB:
            if item["username"] == username:
                print("Someone try to create an account with an existing username")
                try:
                    self.__conn.send(self.json_maker("response", "yes", "AccountAlreadyExist").encode('utf-8'))
                except ssl.SSLEOFError:
                    print('Client aborted connection')
                return -1

        if re.search(r"^[a-zA-Z-0-9]+$", username):
            if 3 < len(username) < 32:
                if 7 < len(password) < 32:
                    with open("users.json", "w") as user_DB:
                        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                        _user_DB.append({
                            "username": username,
                            "password": password_hash.decode('utf-8')
                        })
                        json.dump(_user_DB, user_DB, indent=2)
                    try:
                        self.__conn.send(self.json_maker("response", "yes").encode('utf-8'))
                    except ssl.SSLEOFError:
                        print('Client aborted connection')
                else:
                    print("NOK MDP LONGUEUR")
                    try:
                        self.__conn.send(self.json_maker("response", "yes", "BadPassword").encode('utf-8'))
                    except ssl.SSLEOFError:
                        print('Client aborted connection')
            else:
                print("NOK USERNAME LONGUEUR")
                try:
                    self.__conn.send(self.json_maker("response", "yes", "BadUsername").encode('utf-8'))
                except ssl.SSLEOFError:
                    print('Client aborted connection')
        else:
            print("NOK USERNAME CHARACTERS")
            try:
                self.__conn.send(self.json_maker("response", "yes", "BadUsername").encode('utf-8'))
            except ssl.SSLEOFError:
                print('Client aborted connection')

    def get_tasks(self, output):
        if self.__auth:
            # RETOURNER LA LISTE DES TACHES
            pass
        else:
            print("User is not authentificated")
            try:
                self.__conn.send(self.json_maker("response", "no", "NotAuthorized").encode('utf-8'))
            except ssl.SSLEOFError:
                print('Client aborted connection')
            return -1

    @staticmethod
    def json_maker(server_answer, authorized, error="", content=""):
        if content != "":
            return json.dumps([
                {
                    "server": server_answer,
                    "authorized": authorized,
                    "error": error,
                    "content": content
                }
            ])
        else:
            return json.dumps([
                {
                    "server": server_answer,
                    "authorized": authorized,
                    "error": error,
                }
            ])


if __name__ == "__main__":
    open_sockets = []

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('./certs/srv/YeGrec.pem', './certs/srv/YeGrec.key')

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    server.bind(('127.0.0.1', 5000))
    server.listen(5)
    secure_sock = context.wrap_socket(server, server_side=True)

    print("Trying to reach mysql server... ", end="")

    try:
        database = mysql.connector.connect(
            host="10.128.200.7",
            port="3306",
            user="sae52",
            password="Sae52rt31",
            database="mydb"
        )
        cursor = database.cursor()
    except mysql.connector.errors.DatabaseError:
        print(Fore.RED + "Failed")
        print("Can't reach database server" + Style.RESET_ALL)
        sys.exit(-1)

    print(Fore.GREEN + "OK" + Style.RESET_ALL)
    
    while True:
        print("Waiting for connection...")
        try:
            (conn, (ip, port)) = secure_sock.accept()
        except ConnectionAbortedError:
            print('Client aborted connection')
            continue

        print(f"Client {ip}:{port} is connected !")
        client = Client(conn, cursor)
        thread = threading.Thread(target=client.run())
        thread.start()
        open_sockets.append(thread)
