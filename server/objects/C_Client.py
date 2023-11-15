import mysql.connector
import datetime
import bcrypt
import json
import ssl

from .C_Task import Task
from .C_SubTask import SubTask
from .C_Label import Label
from .C_User import User
from . import C_Exceptions


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

        while client_action != "DISCONNECT":
            buffer = self.__conn.recv(1024)
            received_message = buffer.decode('utf-8')
            if received_message != previous_msg:
                try:
                    output = json.loads(received_message)
                    client_action = output["client"]
                    output.pop("client")
                except KeyError:
                    self.send_error("InvalidJSONFormat", "Invalid json format")
                except TypeError:
                    self.send_error("InvalidJSONFormat", "Invalid json format")
                except json.decoder.JSONDecodeError:
                    return self.write_log("Invalid json format", "UNKNOWN_ERROR")
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
                elif client_action == "get_tasks":
                    if self.get_tasks() == -1:
                        client_action = "disconnect"
                elif client_action == "get_subtasks":
                    if self.get_subtasks(output) == -1:
                        client_action = "disconnect"
                else:
                    self.send_error("InvalidJSONFormat", "WRONG_ACTION")

        self.__conn.send("DISCONNECT".encode('utf-8'))
        self.write_log("The socket has been closed", "CLOSED_SOCKET")

    def login(self, output):
        try:
            username = output.get("username", "")
            password = output.get("password", "")
        except AttributeError as error:
            return self.send_error("InvalidJSONFormat", error)

        try:
            self.__cursor.execute("SELECT * FROM User")
        except mysql.connector.Error as error:
            return self.send_error("InternalError", error)

        for item in self.__cursor:
            if item[1] == username:
                if bcrypt.checkpw(password.encode('utf8'), item[2].encode('utf8')):
                    self.__auth = True
                    self.__user = item[1]
                    self.write_log(f"Has logged with username {username}", "SUCCEED_AUTH")
                    return self.send_success()
                else:
                    return self.send_error("BadPasswordOrUsername", "WRONG_PASSWORD")

        return self.send_error("BadPasswordOrUsername", "WRONG_USERNAME")

    def sign_up(self, output):
        try:
            username = output.get("username", "")
            password = output.get("password", "")
            self.__cursor.execute("SELECT * FROM User")
        except AttributeError as error:
            return self.send_error("InvalidJSONFormat", error)
        except mysql.connector.Error as error:
            return self.send_error("InternalError", error)

        for item in self.__cursor:
            if item[1] == username:
                self.write_log("Try to create an account with an existing username", "EXISTING_USERNAME")
                return self.send_error("AccountAlreadyExist", "EXISTING_USERNAME")

        try:
            User(username, password)
        except C_Exceptions.PasswordError as error:
            return self.send_error("BadPassword", error)
        except C_Exceptions.UsernameError as error:
            return self.send_error("BadUsername", error)

        sql = "INSERT INTO User (username, password) VALUES (%s, %s)"

        try:
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            self.__cursor.execute(sql, (username, password_hash.decode('utf-8')))
            self.__database.commit()
        except mysql.connector.Error as error:
            self.send_error("InternalError", error)

        self.write_log(f"User {username} has been created", "USER_CREATED")
        self.send_success()

    def create_task(self, output):
        if self.__auth:
            try:
                name = output.get("name", "")
                state = output.get("state", "")
                priority = output.get("priority", "")
                date = output.get("date", "")
                description = output.get("description", "")
                labels_id = output.get("labels_id", [])
                users_id = output.get("users_id", [])
                task = Task(name, state, priority, date, description, labels_id=labels_id, users_id=users_id)
            except AttributeError as error:
                return self.send_error("InvalidJSONFormat", error)
            except TypeError:
                return self.send_error("InvalidJSONFormat", "Invalid json format")
            except ValueError:
                return self.send_error("ValueError", "Invalid value")

            name = task.get_name()
            state = task.get_state()
            priority = task.get_priority()
            date = task.get_date()
            description = task.get_description()
            users_id = task.get_users_id()
            labels_id = task.get_labels_id()

            sql = ("INSERT INTO Task (name, state, priority, date, description)"
                   "VALUES (%s, %s, %s, %s, %s)")

            try:
                self.__cursor.execute(sql, (name, state, priority, date, description))
                task_id = self.__cursor.lastrowid
            except mysql.connector.errors.IntegrityError as error:
                return self.send_error("TaskNameAlreadyExist", error)
            except mysql.connector.Error as error:
                return self.send_error("InternalError", error)

            sql = "SELECT idUser FROM User WHERE username = %s"

            try:
                self.__cursor.execute(sql, (self.__user, ))
                personal_id = self.__cursor.fetchone()
                personal_id = personal_id[0]
            except mysql.connector.Error as error:
                return self.send_error("InternalError", error)

            sql = ("INSERT INTO User_has_Task (User_idUser, Task_idTask)"
                   "VALUES (%s, %s)")

            try:
                for user in users_id:
                    self.__cursor.execute(sql, (user, task_id))
                self.__cursor.execute(sql, (personal_id, task_id))
                self.__database.commit()
            except mysql.connector.errors.IntegrityError as error:
                return self.send_error("ValueError", error)
            except mysql.connector.errors.DatabaseError as error:
                return self.send_error("InvalidJSONFormat", error)

            sql = ("INSERT INTO Task_has_Label (Task_idTask, Label_idLabel)"
                   "VALUES (%s, %s)")

            if len(labels_id) == 0:
                self.__conn.send(self.json_maker("response", "yes").encode('utf-8'))
            else:
                try:
                    for label in labels_id:
                        self.__cursor.execute(sql, (task_id, label))
                    self.__database.commit()
                except mysql.connector.errors.IntegrityError as error:
                    return self.send_error("ValueError", error)
                except mysql.connector.errors.DatabaseError as error:
                    return self.send_error("InvalidJSONFormat", error)

            return self.send_success()

        else:
            return self.send_error("NotAuthorized", "NOT_AUTHORIZED")

    def create_subtask(self, output):
        if self.__auth:
            try:
                name = output.get("name", "")
                state = output.get("state", "")
                date = output.get("date", "")
                task_id = output.get("task_id", "")
                labels_id = output.get("labels_id", [])
                sub_task = SubTask(name, state, date, task_id, labels_id)
            except AttributeError as error:
                return self.send_error("InvalidJSONFormat", error)
            except TypeError as error:
                return self.send_error("InvalidJSONFormat", error)
            except ValueError as error:
                return self.send_error("InvalidJSONFormat", error)

            name = sub_task.get_name()
            state = sub_task.get_state()
            date = sub_task.get_date()
            task_id = sub_task.get_task_id()
            labels_id = sub_task.get_labels()

            sql = ("INSERT INTO Sub_Task (name, state, date, Task_idTask)"
                   "VALUES (%s, %s, %s, %s)")

            try:
                self.__cursor.execute(sql, (name, state, date, task_id))
                self.__database.commit()
                subtask_id = self.__cursor.lastrowid
            except mysql.connector.errors.IntegrityError as error:
                return self.send_error("SubTaskNameAlreadyExist", error)
            except mysql.connector.Error as error:
                return self.send_error("InternalError", error)

            sql = ("INSERT INTO Sub_Task_has_Label (Sub_Task_idSub_Task, Label_idLabel)"
                   "VALUES (%s, %s)")

            if len(labels_id) == 0:
                self.__conn.send(self.json_maker("response", "yes").encode('utf-8'))
            else:
                try:
                    for label in labels_id:
                        self.__cursor.execute(sql, (subtask_id, label))
                    self.__database.commit()
                except mysql.connector.errors.IntegrityError as error:
                    self.send_error("ValueError", error)
                except mysql.connector.errors.DatabaseError as error:
                    self.send_error("InvalidJSONFormat", error)

            return self.send_success()

        else:
            return self.send_error("NotAuthorized", "NOT_AUTHORIZED")

    def create_label(self, output):
        if self.__auth:
            try:
                name = output.get("name", "")
                color = output.get("color", "")
                label = Label(name, color)
            except AttributeError as error:
                return self.send_error("InvalidJSONFormat", error)
            except TypeError as error:
                return self.send_error("InvalidJSONFormat", error)
            except ValueError as error:
                return self.send_error("InvalidJSONFormat", error)

            sql = ("INSERT INTO Label (name, color)"
                   "VALUES (%s, %s)")

            try:
                self.__cursor.execute(sql, (name, color))
                self.__database.commit()
            except mysql.connector.errors.IntegrityError as error:
                self.send_error("LabelNameAlreadyExist", error)
            except mysql.connector.Error as error:
                self.send_error("InternalError", error)

            return self.send_success()

        else:
            return self.send_error("NotAuthorized", "NOT_AUTHORIZED")

    def get_tasks(self):
        if self.__auth:
            sql = ("SELECT Task.* "
                   "FROM Task "
                   "INNER JOIN User_has_Task ON Task.idTask = User_has_Task.Task_idTask "
                   "INNER JOIN User ON User_has_Task.User_idUser = User.idUser "
                   "WHERE User.username = %s")

            try:
                self.__cursor.execute(sql, (self.__user,))
            except mysql.connector.Error as error:
                return self.send_error("InternalError", error)

            to_json_task = list()

            for element in self.__cursor.fetchall():
                sql_labels = ("SELECT Label.idlabel "
                              "FROM Label "
                              "INNER JOIN Task_has_Label ON Label.idlabel = Task_has_Label.Label_idLabel "
                              "INNER JOIN Task ON Task_has_Label.Task_idTask = Task.idTask "
                              "WHERE Task.idTask = %s")

                sql_users = ("SELECT User.idUser "
                             "FROM User "
                             "INNER JOIN User_has_Task ON User.idUser = User_has_Task.User_idUser "
                             "INNER JOIN Task ON User_has_Task.Task_idTask = Task.idTask "
                             "WHERE Task.idTask = %s")

                try:
                    self.__cursor.execute(sql_labels, (element[0],))
                    labels_id = [result[0] for result in self.__cursor.fetchall()]
                    self.__cursor.execute(sql_users, (element[0],))
                    users_id = [result[0] for result in self.__cursor.fetchall()]
                except mysql.connector.Error as error:
                    return self.send_error("InternalError", error)

                date_to_str = element[4].strftime('%Y-%m-%d %H:%M:%S')
                task = {"task_id": element[0], "name": element[1], "state": element[2], "priority": element[3], "date": date_to_str, "description": element[5], "labels_id": labels_id, "users_id": users_id}
                to_json_task.append(task)

            return self.send_success(to_json_task)

        else:
            return self.send_error("NotAuthorized", "NOT_AUTHORIZED")

    def get_subtasks(self, output):
        if self.__auth:
            sql = ("SELECT Sub_Task.* "
                   "FROM Sub_Task "
                   "WHERE Task_idTask = %s")

            try:
                task_id = output.get("task_id", "")
                int(task_id)
                self.__cursor.execute(sql, (task_id,))
            except AttributeError as error:
                return self.send_error("InvalidJSONFormat", error)
            except mysql.connector.Error as error:
                return self.send_error("InternalError", error)

            to_json_task = list()

            for element in self.__cursor.fetchall():
                sql = ("SELECT Label.idlabel "
                       "FROM Label "
                       "INNER JOIN Sub_Task_has_Label ON Label.idlabel = Sub_Task_has_Label.Label_idLabel "
                       "INNER JOIN Sub_Task ON Sub_Task_has_Label.Sub_Task_idSub_Task = Sub_Task.idSub_Task "
                       "WHERE Sub_Task.idSub_Task = %s")

                try:
                    self.__cursor.execute(sql, (element[0],))
                    labels_id = [result[0] for result in self.__cursor.fetchall()]
                except mysql.connector.Error as error:
                    return self.send_error("InternalError", error)

                date_to_str = element[3].strftime('%Y-%m-%d %H:%M:%S')
                task = {"subtask_id": element[0], "name": element[1], "state": element[2], "date": date_to_str, "description": element[4], "labels_id": labels_id}
                to_json_task.append(task)

            return self.send_success(to_json_task)

        else:
            return self.send_error("NotAuthorized", "NOT_AUTHORIZED")

    def write_log(self, message, event):
        with open("log.txt", "a") as log_file:
            date = datetime.datetime.now()
            log_file.write(date.strftime(f"%Y:%m:%d %H:%M:%S <{self.__address}> {event} : {message}\n"))

    def send_error(self, event, message) -> int:
        self.write_log(message, event)
        try:
            self.__conn.send(self.json_maker("response", "no", event).encode('utf-8'))
        except ssl.SSLEOFError as error:
            self.write_log("Client aborted connection", "ssl.SSLEOFError")
            return -1
        return 0

    def send_success(self, content=None) -> int:
        try:
            self.__conn.send(self.json_maker("response", "yes", error=None, content=content).encode('utf-8'))
        except ssl.SSLEOFError:
            self.write_log("Client aborted connection", "ssl.SSLEOFError")
            return -1
        return 0

    @staticmethod
    def json_maker(server_answer, success, error=None, content=None):
        if content:
            return json.dumps([{
                    "server": server_answer,
                    "success": success,
                    "error": error,
                    "content": content
            }])
        else:
            return json.dumps([{
                    "server": server_answer,
                    "success": success,
                    "error": error,
            }])
