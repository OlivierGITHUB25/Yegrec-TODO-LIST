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
    def __init__(self, conn, cursor, database):
        self.__conn = conn
        self.__cursor = cursor
        self.__database = database
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
                except KeyError:
                    print("Invalid json format")
                    continue
                except json.decoder.JSONDecodeError:
                    print("Invalid json format - UNKNOWN ERROR")
                    continue
                finally:
                    previous_msg = received_message

                if client_action == "login":
                    self.login(output)
                elif client_action == "sign_up":
                    self.sign_up(output)
                elif client_action == "create_task":
                    self.create_task(output)

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

        try:
            self.__cursor.execute("SELECT * FROM user")
        except mysql.connector.Error:
            print("Internal error : Can't create entry")
            try:
                self.__conn.send(self.json_maker("response", "yes", error="InternalError").encode('utf-8'))
            except ssl.SSLEOFError:
                print('Client aborted connection')
            finally:
                return -1

        for item in self.__cursor:
            if item[1] == username:
                if bcrypt.checkpw(password.encode('utf8'), item[2].encode('utf8')):
                    print(f"User {username} is logged in !")
                    try:
                        self.__auth = True
                        self.__user = item[1]
                        self.__conn.send(self.json_maker("response", "yes").encode('utf-8'))
                    except ssl.SSLEOFError:
                        print('Client aborted connection')
                    return 0
                else:
                    print(f"{item[1]} enter wrong password")
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

        try:
            self.__cursor.execute("SELECT * FROM user")
        except mysql.connector.Error:
            print("Internal error : Can't create entry")
            try:
                self.__conn.send(self.json_maker("response", "yes", error="InternalError").encode('utf-8'))
            except ssl.SSLEOFError:
                print('Client aborted connection')
            finally:
                return -1

        for item in self.__cursor:
            if item[1] == username:
                print("Someone try to create an account with an existing username")
                try:
                    username = item[1]
                    password = item[2]
                    self.__conn.send(self.json_maker("response", "yes", "AccountAlreadyExist").encode('utf-8'))
                except ssl.SSLEOFError:
                    print('Client aborted connection')
                return -1

        if re.search(r"^[a-zA-Z-0-9]+$", username):
            if 3 < len(username) < 32:
                if 7 < len(password) < 32:
                    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    sql = "INSERT INTO user (username, password) VALUES (%s, %s)"
                    try:
                        self.__cursor.execute(sql, (username, password_hash.decode('utf-8')))
                        self.__database.commit()
                    except mysql.connector.Error:
                        print("Internal error : Can't create entry")
                        try:
                            self.__conn.send(self.json_maker("response", "yes", error="InternalError").encode('utf-8'))
                        except ssl.SSLEOFError:
                            print('Client aborted connection')
                        finally:
                            return -1

                    print(f"User {username} has been created")

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

    def create_task(self, output):
        name = ""
        state = ""
        date = ""
        priority = ""
        labels = []
        users = []

        if self.__auth:
            try:
                content = []
                for item in output:
                    content = item["content"]

                name = content.get("name")
                state = content.get("state")
                date = content.get("date")
                description = content.get("description")
                priority = content.get("priority")
                labels = content.get("labels")
                if content.get("users") == {}:
                    users = self.__user
                else:
                    users = content.get("users")

                print(type(labels))
                print(name, "\n", state, "\n", date, "\n", description, "\n", priority, "\n", labels, "\n", users)

            except KeyError:
                print("Invalid json format - KeyError")
                try:
                    self.__conn.send(self.json_maker("response", "no", "InvalidJSONFormat").encode('utf-8'))
                except ssl.SSLEOFError:
                    print('Client aborted connection')
                return -1
            except IndexError:
                print("Invalid json format - IndexError")
                try:
                    self.__conn.send(self.json_maker("response", "no", "InvalidJSONFormat").encode('utf-8'))
                except ssl.SSLEOFError:
                    print('Client aborted connection')
                return -1

            sql = "INSERT INTO task (name, state, date, description, priority, labels, users) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            try:
                self.__cursor.execute(sql, (name, state, date, description, priority, labels, users))
                self.__database.commit()
            except mysql.connector.Error:
                print("Internal error : Can't create entry")
                try:
                    self.__conn.send(self.json_maker("response", "yes", error="InternalError").encode('utf-8'))
                except ssl.SSLEOFError:
                    print('Client aborted connection')
                finally:
                    return -1

        else:
            print("User is not authenticated")
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
            host="10.129.10.153",
            port="3306",
            user="sae52",
            password="Sae52rt31",
            database="yegrec"
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
        client = Client(conn, cursor, database)
        thread = threading.Thread(target=client.run())
        thread.start()
        open_sockets.append(thread)
