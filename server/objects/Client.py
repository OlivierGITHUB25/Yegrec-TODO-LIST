import mysql.connector
import datetime
import bcrypt
import json
import ssl
import re


class Client:
    def __init__(self, conn, ip, port, cursor, database):
        self.__conn = conn
        self.__address = (ip, port)
        self.__cursor = cursor
        self.__database = database
        self.__auth = False
        self.__user = ""

    def run(self):
        previous_msg = ""
        client_action = ""

        self.write_log("Connection initialized", "NEW_SOCKET")

        while client_action != "disconnect":
            buffer = self.__conn.recv(1024)
            received_message = buffer.decode('utf-8')

            if received_message != previous_msg:
                try:
                    output = json.loads(received_message)
                    for item in output:
                        client_action = item["client"]
                except KeyError:
                    self.write_log("Invalid json format", "KeyError")
                    continue
                except json.decoder.JSONDecodeError:
                    self.write_log("Invalid json format", "UNKNOWN_ERROR")
                    continue
                finally:
                    previous_msg = received_message

                if client_action == "login":
                    if self.login(output) == -1:
                        client_action = "disconnect"
                elif client_action == "sign_up":
                    if self.sign_up(output) == -1:
                        client_action = "disconnect"
                elif client_action == "create_task":
                    if self.create_task(output) == -1:
                        client_action = "disconnect"
                elif client_action == "create_subtask":
                    if self.create_subtask(output) == -1:
                        client_action = "disconnect"
                elif client_action == "create_label":
                    if self.create_label(output) == -1:
                        client_action = "disconnect"

        self.write_log("The socket has been closed", "CLOSED_SOCKET")

    def login(self, output):
        username = ""
        password = ""

        try:
            for item in output:
                username = item["username"]
                password = item["password"]
        except KeyError:
            self.write_log("Invalid json format", "KeyError")
            try:
                self.__conn.send(self.json_maker("response", "no", "InvalidJSONFormat").encode('utf-8'))
            except ssl.SSLEOFError:
                self.write_log("Client aborted connection", "ssl.SSLEOFError")
                return -1
            return 0

        try:
            self.__cursor.execute("SELECT * FROM User")
        except mysql.connector.Error:
            self.write_log("Internal error", "mysql.connector.Error")
            try:
                self.__conn.send(self.json_maker("response", "yes", "InternalError").encode('utf-8'))
            except ssl.SSLEOFError:
                self.write_log("Client aborted connection", "ssl.SSLEOFError")
                return -1
            return 0

        for item in self.__cursor:
            if item[1] == username:
                if bcrypt.checkpw(password.encode('utf8'), item[2].encode('utf8')):
                    self.write_log(f"Has logged with username {username}", "SUCCEED_AUTH")
                    try:
                        self.__auth = True
                        self.__user = item[1]
                        self.__conn.send(self.json_maker("response", "yes").encode('utf-8'))
                    except ssl.SSLEOFError:
                        self.write_log("Client aborted connection", "ssl.SSLEOFError")
                        return -1
                    return 0
                else:
                    self.write_log(f"{item[1]} enter wrong password", "WRONG_PASSWORD")
                    try:
                        self.__conn.send(self.json_maker("response", "no").encode('utf-8'))
                    except ssl.SSLEOFError:
                        self.write_log("Client aborted connection", "ssl.SSLEOFError")
                        return -1

        try:
            self.__conn.send(self.json_maker("response", "no").encode('utf-8'))
        except ssl.SSLEOFError:
            self.write_log("Client aborted connection", "ssl.SSLEOFError")
            return -1

    def sign_up(self, output):
        username = ""
        password = ""

        try:
            for item in output:
                username = item["username"]
                password = item["password"]
        except KeyError:
            self.write_log("Invalid json format", "KeyError")
            try:
                self.__conn.send(self.json_maker("response", "no", "InvalidJSONFormat").encode('utf-8'))
            except ssl.SSLEOFError:
                self.write_log("Client aborted connection", "ssl.SSLEOFError")
                return -1
            return 0

        try:
            self.__cursor.execute("SELECT * FROM User")
        except mysql.connector.Error:
            self.write_log("Internal error", "mysql.connector.Error")
            try:
                self.__conn.send(self.json_maker("response", "yes", "InternalError").encode('utf-8'))
            except ssl.SSLEOFError:
                self.write_log("Client aborted connection", "ssl.SSLEOFError")
                return -1
            return 0

        for item in self.__cursor:
            if item[1] == username:
                self.write_log("Try to create an account with an existing username", "EXISTING_USERNAME")
                try:
                    username = item[1]
                    password = item[2]
                    self.__conn.send(self.json_maker("response", "yes", "AccountAlreadyExist").encode('utf-8'))
                except ssl.SSLEOFError:
                    self.write_log("Client aborted connection", "ssl.SSLEOFError")
                    return -1
                return 0

        if re.search(r"^[a-zA-Z-0-9]+$", username):
            if 3 < len(username) < 32:
                if 7 < len(password) < 32:
                    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    sql = "INSERT INTO User (username, password) VALUES (%s, %s)"
                    try:
                        self.__cursor.execute(sql, (username, password_hash.decode('utf-8')))
                        self.__database.commit()
                    except mysql.connector.Error:
                        self.write_log("Internal error", "mysql.connector.Error")
                        try:
                            self.__conn.send(self.json_maker("response", "yes", "InternalError").encode('utf-8'))
                        except ssl.SSLEOFError:
                            self.write_log("Client aborted connection", "ssl.SSLEOFError")
                            return -1
                        return 0

                    self.write_log(f"User {username} has been created", "USER_CREATED")

                    try:
                        self.__conn.send(self.json_maker("response", "yes").encode('utf-8'))
                    except ssl.SSLEOFError:
                        self.write_log("Client aborted connection", "ssl.SSLEOFError")
                        return -1
                else:
                    self.write_log(f"Password length is out of range", "PASSWD_ERROR")
                    try:
                        self.__conn.send(self.json_maker("response", "yes", "BadPassword").encode('utf-8'))
                    except ssl.SSLEOFError:
                        self.write_log("Client aborted connection", "ssl.SSLEOFError")
                        return -1
            else:
                self.write_log(f"Username length is out of range", "USERNAME_ERROR")
                try:
                    self.__conn.send(self.json_maker("response", "yes", "BadUsername").encode('utf-8'))
                except ssl.SSLEOFError:
                    self.write_log("Client aborted connection", "ssl.SSLEOFError")
                    return -1
        else:
            self.write_log(f"Username use wrong characters", "USERNAME_ERROR")
            try:
                self.__conn.send(self.json_maker("response", "yes", "BadUsername").encode('utf-8'))
            except ssl.SSLEOFError:
                self.write_log("Client aborted connection", "ssl.SSLEOFError")
                return -1

    def create_task(self, output):
        if self.__auth:
            try:
                content = []
                for item in output:
                    content = item["content"]

                name = content.get("name")
                state = content.get("state")
                priority = content.get("priority")
                date = content.get("date")
                description = content.get("description")
                labels = content.get("labels_id")
                users = content.get("users_id")
            except KeyError:
                self.write_log("Invalid json format", "KeyError")
                try:
                    self.__conn.send(self.json_maker("response", "no", "InvalidJSONFormat").encode('utf-8'))
                except ssl.SSLEOFError:
                    self.write_log("Client aborted connection", "ssl.SSLEOFError")
                    return -1
                return 0
            except IndexError:
                self.write_log("Invalid json format", "IndexError")
                try:
                    self.__conn.send(self.json_maker("response", "no", "InvalidJSONFormat").encode('utf-8'))
                except ssl.SSLEOFError:
                    self.write_log("Client aborted connection", "ssl.SSLEOFError")
                    return -1
                return 0

            sql = ("INSERT INTO Task (name, state, priority, date, description)"
                   "VALUES (%s, %s, %s, %s, %s)")

            try:
                self.__cursor.execute(sql, (name, state, priority, date, description))
                self.__database.commit()
                task_id = self.__cursor.lastrowid
            except mysql.connector.errors.IntegrityError:
                self.write_log("Task name already exist", "mysql.connector.Error.IntegrityError:")
                try:
                    self.__conn.send(self.json_maker("response", "yes", "TaskNameAlreadyExist").encode('utf-8'))
                except ssl.SSLEOFError:
                    self.write_log("Client aborted connection", "ssl.SSLEOFError")
                    return -1
                return 0
            except mysql.connector.Error:
                self.write_log("Internal error", "mysql.connector.Error")
                try:
                    self.__conn.send(self.json_maker("response", "yes", "InternalError").encode('utf-8'))
                except ssl.SSLEOFError:
                    self.write_log("Client aborted connection", "ssl.SSLEOFError")
                    return -1
                return 0

            sql = ("INSERT INTO User_has_Task (User_idUser, Task_idTask)"
                   "VALUES (%s, %s)")

            if len(users) == 0:
                user = [self.__user]
                self.__cursor.execute(sql, (user, task_id))
                self.__database.commit()
            else:
                try:
                    for user in users:
                        self.__cursor.execute(sql, (user, task_id))
                    self.__database.commit()
                except mysql.connector.errors.IntegrityError:
                    try:
                        self.__conn.send(self.json_maker("response", "no", "ValueError").encode('utf-8'))
                    except ssl.SSLEOFError:
                        self.write_log("Client aborted connection", "ssl.SSLEOFError")
                        return -1
                    return 0
                except mysql.connector.errors.DatabaseError:
                    try:
                        self.__conn.send(self.json_maker("response", "no", "InvalidJSONFormat").encode('utf-8'))
                    except ssl.SSLEOFError:
                        self.write_log("Client aborted connection", "ssl.SSLEOFError")
                        return -1
                    return 0

            sql = ("INSERT INTO Task_has_Label (Task_idTask, Label_idLabel)"
                   "VALUES (%s, %s)")

            if len(labels) == 0:
                return 0
            else:
                try:
                    for label in labels:
                        self.__cursor.execute(sql, (task_id, label))
                    self.__database.commit()
                except mysql.connector.errors.IntegrityError:
                    try:
                        self.__conn.send(self.json_maker("response", "no", "ValueError").encode('utf-8'))
                    except ssl.SSLEOFError:
                        self.write_log("Client aborted connection", "ssl.SSLEOFError")
                        return -1
                    return 0
                except mysql.connector.errors.DatabaseError:
                    try:
                        self.__conn.send(self.json_maker("response", "no", "InvalidJSONFormat").encode('utf-8'))
                    except ssl.SSLEOFError:
                        self.write_log("Client aborted connection", "ssl.SSLEOFError")
                        return -1
                    return 0
        else:
            self.write_log("This connection is not authenticated", "NOT_AUTHORIZED")
            try:
                self.__conn.send(self.json_maker("response", "no", "NotAuthorized").encode('utf-8'))
            except ssl.SSLEOFError:
                self.write_log("Client aborted connection", "ssl.SSLEOFError")
                return -1
            return 0

    def create_subtask(self, output):
        if self.__auth:
            try:
                content = []
                for item in output:
                    content = item["content"]

                name = content.get("name")
                state = content.get("state")
                date = content.get("date")
                task_id = content.get("task_id")
                labels = content.get("labels_id")
            except KeyError:
                self.write_log("Invalid json format", "KeyError")
                try:
                    self.__conn.send(self.json_maker("response", "no", "InvalidJSONFormat").encode('utf-8'))
                except ssl.SSLEOFError:
                    self.write_log("Client aborted connection", "ssl.SSLEOFError")
                    return -1
                return 0
            except IndexError:
                self.write_log("Invalid json format", "IndexError")
                try:
                    self.__conn.send(self.json_maker("response", "no", "InvalidJSONFormat").encode('utf-8'))
                except ssl.SSLEOFError:
                    self.write_log("Client aborted connection", "ssl.SSLEOFError")
                    return -1
                return 0

            sql = ("INSERT INTO Sub_Task (name, state, date, Task_idTask)"
                   "VALUES (%s, %s, %s, %s)")

            try:
                self.__cursor.execute(sql, (name, state, date, task_id))
                self.__database.commit()
                subtask_id = self.__cursor.lastrowid
            except mysql.connector.errors.IntegrityError:
                self.write_log("SubTask name already exist", "mysql.connector.Error.IntegrityError:")
                try:
                    self.__conn.send(self.json_maker("response", "yes", "TaskNameAlreadyExist").encode('utf-8'))
                except ssl.SSLEOFError:
                    self.write_log("Client aborted connection", "ssl.SSLEOFError")
                    return -1
                return 0
            except mysql.connector.Error:
                self.write_log("Internal error", "mysql.connector.Error")
                try:
                    self.__conn.send(self.json_maker("response", "yes", "InternalError").encode('utf-8'))
                except ssl.SSLEOFError:
                    self.write_log("Client aborted connection", "ssl.SSLEOFError")
                    return -1
                return 0

            sql = ("INSERT INTO Sub_Task_has_Label (Sub_Task_idSub_Task, Label_idLabel)"
                   "VALUES (%s, %s)")

            if len(labels) == 0:
                return 0
            else:
                try:
                    for label in labels:
                        self.__cursor.execute(sql, (subtask_id, label))
                    self.__database.commit()
                except mysql.connector.errors.IntegrityError:
                    try:
                        self.__conn.send(self.json_maker("response", "no", "ValueError").encode('utf-8'))
                    except ssl.SSLEOFError:
                        self.write_log("Client aborted connection", "ssl.SSLEOFError")
                        return -1
                    return 0
                except mysql.connector.errors.DatabaseError:
                    try:
                        self.__conn.send(self.json_maker("response", "no", "InvalidJSONFormat").encode('utf-8'))
                    except ssl.SSLEOFError:
                        self.write_log("Client aborted connection", "ssl.SSLEOFError")
                        return -1
                    return 0
        else:
            self.write_log("This connection is not authenticated", "NOT_AUTHORIZED")
            try:
                self.__conn.send(self.json_maker("response", "no", "NotAuthorized").encode('utf-8'))
            except ssl.SSLEOFError:
                self.write_log("Client aborted connection", "ssl.SSLEOFError")
                return -1
            return 0

    def create_label(self, output):
        if self.__auth:
            try:
                content = []
                for item in output:
                    content = item["content"]

                name = content.get("name")
                color = content.get("color")

            except KeyError:
                self.write_log("Invalid json format", "KeyError")
                try:
                    self.__conn.send(self.json_maker("response", "no", "InvalidJSONFormat").encode('utf-8'))
                except ssl.SSLEOFError:
                    self.write_log("Client aborted connection", "ssl.SSLEOFError")
                    return -1
                return 0
            except IndexError:
                self.write_log("Invalid json format", "IndexError")
                try:
                    self.__conn.send(self.json_maker("response", "no", "InvalidJSONFormat").encode('utf-8'))
                except ssl.SSLEOFError:
                    self.write_log("Client aborted connection", "ssl.SSLEOFError")
                    return -1
                return 0

            sql = ("INSERT INTO Label (name, color)"
                   "VALUES (%s, %s)")

            try:
                self.__cursor.execute(sql, (name, color))
                self.__database.commit()
            except mysql.connector.errors.IntegrityError:
                self.write_log("Label name already exist", "mysql.connector.Error.IntegrityError:")
                try:
                    self.__conn.send(self.json_maker("response", "yes", "LabelNameAlreadyExist").encode('utf-8'))
                except ssl.SSLEOFError:
                    self.write_log("Client aborted connection", "ssl.SSLEOFError")
                    return -1
                return 0
            except mysql.connector.Error:
                self.write_log("Internal error", "mysql.connector.Error")
                try:
                    self.__conn.send(self.json_maker("response", "yes", "InternalError").encode('utf-8'))
                except ssl.SSLEOFError:
                    self.write_log("Client aborted connection", "ssl.SSLEOFError")
                    return -1
                return 0
        else:
            self.write_log("This connection is not authenticated", "NOT_AUTHORIZED")
            try:
                self.__conn.send(self.json_maker("response", "no", "NotAuthorized").encode('utf-8'))
            except ssl.SSLEOFError:
                self.write_log("Client aborted connection", "ssl.SSLEOFError")
                return -1
            return 0

    def write_log(self, message, event):
        with open("log.txt", "a") as log_file:
            date = datetime.datetime.now()
            log_file.write(date.strftime(f"%Y:%m:%d %H:%M:%S <{self.__address}> {event} : {message}\n"))

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
