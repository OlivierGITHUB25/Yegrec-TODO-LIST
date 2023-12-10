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
        self.__user = None
        self.__user_id = None

    def run(self):
        client_action = None
        output = None

        self.write_log("Connection initialized", "NEW_SOCKET")

        while client_action != "DISCONNECT":
            buffer = self.__conn.recv(1024)
            received_message = buffer.decode('utf-8')

            try:
                output = json.loads(received_message)
                client_action = output["client"]
                output.pop("client")
            except KeyError:
                self.send_error("InvalidJSONFormat", "Invalid json format")
            except TypeError:
                self.send_error("InvalidJSONFormat", "Invalid json format")
            except json.decoder.JSONDecodeError:
                return self.write_log(f"User {self.__user} disconnected", "CLIENT_DISCONNECTED")

            if client_action == "login":
                if self.login(output) == -1:
                    client_action = "DISCONNECT"
            elif client_action == "sign_up":
                if self.sign_up(output) == -1:
                    client_action = "DISCONNECT"
            elif client_action == "create_task":
                if self.create_task(output) == -1:
                    client_action = "DISCONNECT"
            elif client_action == "create_subtask":
                if self.create_subtask(output) == -1:
                    client_action = "DISCONNECT"
            elif client_action == "create_label":
                if self.create_label(output) == -1:
                    client_action = "DISCONNECT"
            elif client_action == "get_tasks":
                if self.get_tasks() == -1:
                    client_action = "DISCONNECT"
            elif client_action == "get_subtasks":
                if self.get_subtasks(output) == -1:
                    client_action = "DISCONNECT"
            elif client_action == "get_labels":
                if self.get_labels() == -1:
                    client_action = "DISCONNECT"
            elif client_action == "get_users":
                if self.get_users() == -1:
                    client_action = "DISCONNECT"
            elif client_action == "update_task":
                if self.update_task(output) == -1:
                    client_action = "DISCONNECT"
            elif client_action == "update_subtask":
                if self.update_subtask(output) == -1:
                    client_action = "DISCONNECT"
            else:
                self.send_error("InvalidJSONFormat", "Invalid json format")

        self.send_success(server_answer="DISCONNECT")
        self.write_log(f"User {self.__user} disconnected", "CLIENT_DISCONNECTED")

    # Verified
    def login(self, output):
        # Get output arguments
        try:
            username = output.get("username", "")
            password = output.get("password", "")
        except AttributeError as error:
            return self.send_error("InvalidJSONFormat", error)

        # Get users from database
        try:
            self.__cursor.execute("SELECT * FROM User")
        except mysql.connector.Error as error:
            return self.send_error("InternalError", error)

        for item in self.__cursor.fetchall():
            # Check if user exist in database
            if item[1] == username:
                # Hash check
                if bcrypt.checkpw(password.encode('utf8'), item[2].encode('utf8')):
                    self.__auth = True
                    self.__user = item[1]
                    self.__user_id = item[0]
                    self.write_log(f"Has logged with username {username}", "SUCCEED_AUTH")
                    return self.send_success()
                else:
                    return self.send_error("BadPasswordOrUsername", "WRONG_PASSWORD")

        return self.send_error("BadPasswordOrUsername", "WRONG_USERNAME")

    # Verified
    def sign_up(self, output):
        # Get output arguments and check them
        try:
            username = output.get("username", "")
            password = output.get("password", "")
            User(username, password)
            self.__cursor.execute("SELECT * FROM User")
        except AttributeError as error:
            return self.send_error("InvalidJSONFormat", error)
        except mysql.connector.Error as error:
            return self.send_error("InternalError", error)
        except C_Exceptions.PasswordError as error:
            return self.send_error("BadPassword", error)
        except C_Exceptions.UsernameError as error:
            return self.send_error("BadUsername", error)

        for item in self.__cursor.fetchall():
            # Check if user already exist in DB
            if item[1] == username:
                self.write_log("Try to create an account with an existing username", "EXISTING_USERNAME")
                return self.send_error("AccountAlreadyExist", "EXISTING_USERNAME")

        sql = "INSERT INTO User (username, password) VALUES (%s, %s)"

        # Generate hash and commit to database
        try:
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            self.__cursor.execute(sql, (username, password_hash.decode('utf-8')))
            self.__database.commit()
        except mysql.connector.Error as error:
            return self.send_error("InternalError", error)

        self.write_log(f"User {username} has been created", "USER_CREATED")
        return self.send_success()

    # Verified
    def create_task(self, output):
        # Check if user is authenticated
        if self.__auth:
            # Get output arguments and check them
            try:
                name = output.get("name", "")
                state = output.get("state", "")
                priority = output.get("priority", "")
                date = output.get("date", "")
                description = output.get("description", "")
                labels_id = output.get("labels_id", [])
                users_id = output.get("users_id", [])
                Task(name, state, priority, date, description, labels_id=labels_id, users_id=users_id)
            except AttributeError as error:
                return self.send_error("InvalidJSONFormat", error)
            except TypeError:
                return self.send_error("InvalidJSONFormat", "Invalid json format")
            except ValueError:
                return self.send_error("ValueError", "Invalid value")

            sql = ("INSERT INTO Task (name, state, priority, date, description)"
                   "VALUES (%s, %s, %s, %s, %s)")

            # Try to insert task data (without committing to database)
            try:
                self.__cursor.execute(sql, (name, state, priority, date, description))
                task_id = self.__cursor.lastrowid
            except mysql.connector.Error as error:
                return self.send_error("InternalError", error)

            sql = ("INSERT INTO User_has_Task (User_idUser, Task_idTask)"
                   "VALUES (%s, %s)")

            # Try to insert User_has_Task data (without committing to database)
            try:
                for user in users_id:
                    self.__cursor.execute(sql, (user, task_id))
                self.__cursor.execute(sql, (self.__user_id, task_id))
            except mysql.connector.errors.IntegrityError as error:
                return self.send_error("ValueError", error)
            except mysql.connector.errors.DatabaseError as error:
                return self.send_error("InvalidJSONFormat", error)

            sql = ("INSERT INTO Task_has_Label (Task_idTask, Label_idLabel)"
                   "VALUES (%s, %s)")

            # Check labels (committing to database)
            if len(labels_id) == 0:
                self.__database.commit()
                return self.send_success()
            else:
                # Try to insert label data (committing to database)
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

    # TODO: Check func
    def create_subtask(self, output):
        # Check if user is authenticated
        if self.__auth:
            # Get output arguments and check them
            try:
                name = output.get("name", "")
                state = output.get("state", "")
                date = output.get("date", "")
                task_id = output.get("task_id", "")
                labels_id = output.get("labels_id", [])
                SubTask(name, state, date, task_id, labels_id)
            except AttributeError as error:
                return self.send_error("InvalidJSONFormat", error)
            except TypeError as error:
                return self.send_error("InvalidJSONFormat", error)
            except ValueError as error:
                return self.send_error("InvalidJSONFormat", error)

            sql = ("SELECT User_idUser FROM User_has_Task "
                   "WHERE Task_idTask = %s AND User_idUser = %s")

            # Checks if the user owns the task
            try:
                self.__cursor.execute(sql, (task_id, self.__user_id))
                result = self.__cursor.fetchall()
            except mysql.connector.Error as error:
                return self.send_error("InternalError", error)
            if not result:
                return self.send_error("NotAuthorized", "NOT_AUTHORIZED")

            sql = ("INSERT INTO Sub_Task (name, state, date, Task_idTask) "
                   "VALUES (%s, %s, %s, %s)")

            # Try to insert Sub_Task data (without committing to database)
            try:
                self.__cursor.execute(sql, (name, state, date, task_id))
                subtask_id = self.__cursor.lastrowid
            except mysql.connector.Error as error:
                return self.send_error("InternalError", error)

            # Check labels (committing to database)
            if len(labels_id) == 0:
                self.__database.commit()
                return self.send_success()

            sql = ("SELECT User_idUser FROM Label "
                   "WHERE idlabel = %s AND User_idUser = %s")

            # Checks if the user owns the label(s)
            try:
                for label in labels_id:
                    self.__cursor.execute(sql, (label, self.__user_id))
                    if not self.__cursor.fetchall():
                        return self.send_error("NotAuthorized", "NOT_AUTHORIZED")
            except mysql.connector.Error as error:
                return self.send_error("InternalError", error)

            sql = ("INSERT INTO Sub_Task_has_Label (Sub_Task_idSub_Task, Label_idLabel) "
                   "VALUES (%s, %s)")

            # Try to insert label data (committing to database)
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

    # Verified
    def create_label(self, output):
        # Check if user is authenticated
        if self.__auth:
            # Get output arguments and check them
            try:
                name = output.get("name", "")
                color = output.get("color", "")
                Label(name, color)
            except AttributeError as error:
                return self.send_error("InvalidJSONFormat", error)
            except TypeError as error:
                return self.send_error("InvalidJSONFormat", error)
            except ValueError as error:
                return self.send_error("InvalidJSONFormat", error)

            sql = ("INSERT INTO Label (name, color, User_idUser) "
                   "VALUES (%s, %s, %s)")

            # Try to insert Label data (committing to database)
            try:
                self.__cursor.execute(sql, (name, color, self.__user_id))
                self.__database.commit()
            except mysql.connector.Error as error:
                return self.send_error("InternalError", error)

            return self.send_success()

        else:
            return self.send_error("NotAuthorized", "NOT_AUTHORIZED")

    # Verified
    def get_tasks(self):
        # Check if user is authenticated
        if self.__auth:
            sql = ("SELECT * FROM Task "
                   "INNER JOIN User_has_Task ON Task.idTask = User_has_Task.Task_idTask "
                   "INNER JOIN User ON User_has_Task.User_idUser = User.idUser "
                   "WHERE User.username = %s")

            # Try to get user tasks
            try:
                self.__cursor.execute(sql, (self.__user,))
            except mysql.connector.Error as error:
                return self.send_error("InternalError", error)

            to_json_task = list()

            # Add labels and users to the result
            for element in self.__cursor.fetchall():
                sql_labels = ("SELECT idlabel FROM Label "
                              "INNER JOIN Task_has_Label ON Label.idlabel = Task_has_Label.Label_idLabel "
                              "INNER JOIN Task ON Task_has_Label.Task_idTask = Task.idTask "
                              "WHERE Task.idTask = %s")

                sql_users = ("SELECT idUser FROM User "
                             "INNER JOIN User_has_Task ON User.idUser = User_has_Task.User_idUser "
                             "INNER JOIN Task ON User_has_Task.Task_idTask = Task.idTask "
                             "WHERE Task.idTask = %s")

                # Try to get labels and users from all user tasks
                try:
                    self.__cursor.execute(sql_labels, (element[0],))
                    labels_id = [result[0] for result in self.__cursor.fetchall()]
                    self.__cursor.execute(sql_users, (element[0],))
                    users_id = [result[0] for result in self.__cursor.fetchall()]
                except mysql.connector.Error as error:
                    return self.send_error("InternalError", error)

                # Convert date to str format
                date_to_str = element[4].strftime('%Y-%m-%d %H:%M:%S')
                # Task template
                task = {"task_id": element[0], "name": element[1], "state": element[2], "priority": element[3],
                        "date": date_to_str, "description": element[5], "labels_id": labels_id, "users_id": users_id}
                # Grouping tasks in a list
                to_json_task.append(task)

            return self.send_success(to_json_task)

        else:
            return self.send_error("NotAuthorized", "NOT_AUTHORIZED")

    # Verified
    def get_subtasks(self, output):
        # Check if user is authenticated
        if self.__auth:
            # Get output argument and check it
            try:
                task_id = int(output.get("task_id", ""))
            except AttributeError as error:
                return self.send_error("InvalidJSONFormat", error)
            except TypeError as error:
                return self.send_error("InvalidJSONFormat", error)
            except ValueError as error:
                return self.send_error("InvalidJSONFormat", error)

            sql = ("SELECT * FROM User_has_Task "
                   "INNER JOIN Task ON User_has_Task.Task_idTask = Task.idTask "
                   "INNER JOIN Sub_Task ON Task.idTask = Sub_Task.Task_idTask "
                   "WHERE User_has_Task.User_idUser = %s AND Task.idTask = %s")

            # Checks if the user owns the sub_tasks
            try:
                self.__cursor.execute(sql, (self.__user_id, task_id,))
                result = self.__cursor.fetchall()
            except mysql.connector.Error as error:
                return self.send_error("InternalError", error)
            if not result:
                return self.send_error("NotAuthorized", "NOT_AUTHORIZED")

            to_json_subtask = list()

            # Add labels for each subtask (if exist)
            for element in result:
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
                task = {"subtask_id": element[0], "name": element[1], "state": element[2], "date": date_to_str,
                        "description": element[4], "labels_id": labels_id}
                to_json_subtask.append(task)

            return self.send_success(to_json_subtask)

        else:
            return self.send_error("NotAuthorized", "NOT_AUTHORIZED")

    # Verified
    def get_labels(self):
        # Check if user is authenticated
        if self.__auth:
            sql = ("SELECT * FROM Label "
                   "WHERE User_idUser = %s")

            # Try to retrieve all labels owned by a user
            try:
                self.__cursor.execute(sql, (self.__user_id,))
            except mysql.connector.Error as error:
                return self.send_error("InternalError", error)

            return self.send_success([result for result in self.__cursor.fetchall()])

        else:
            return self.send_error("NotAuthorized", "NOT_AUTHORIZED")

    # Verified
    def get_users(self):
        # Check if user is authenticated
        if self.__auth:
            sql = ("SELECT idUser, username "
                   "FROM user")

            # Try to retrieve all users
            try:
                self.__cursor.execute(sql)
            except mysql.connector.Error as error:
                return self.send_error("InternalError", error)

            return self.send_success([result for result in self.__cursor.fetchall()])

        else:
            return self.send_error("NotAuthorized", "NOT_AUTHORIZED")

    # TODO: labels and users
    def update_task(self, output):
        # Check if user is authenticated
        if self.__auth:
            # Get output argument and check it
            try:
                task_id = output.get("task_id", "")
                name = output.get("name", "")
                state = output.get("state", "")
                priority = output.get("priority", "")
                date = output.get("date", "")
                description = output.get("description", "")
                labels_id = output.get("labels_id", [])
                users_id = output.get("users_id", [])
                Task(name, state, priority, date, description, labels_id=labels_id, users_id=users_id)
            except AttributeError as error:
                return self.send_error("InvalidJSONFormat", error)
            except TypeError as error:
                return self.send_error("InvalidJSONFormat", error)
            except ValueError as error:
                return self.send_error("InvalidJSONFormat", error)

            sql = ("SELECT Task_idTask FROM User_has_Task "
                   "WHERE User_idUser = %s AND Task_idTask = %s")

            # Check if user own the task
            try:
                self.__cursor.execute(sql, (self.__user_id, task_id))
                result = self.__cursor.fetchall()
            except mysql.connector.Error as error:
                return self.send_error("InternalError", error)
            if not result:
                return self.send_error("NotAuthorized", "NOT_AUTHORIZED")

            sql = ("UPDATE Task "
                   "SET name = %s, state = %s, priority = %s, date = %s, description = %s "
                   "WHERE idTask = %s")

            # Try to update the task attributes
            try:
                self.__cursor.execute(sql, (name, state, priority, date, description, task_id))
                task_id = self.__cursor.lastrowid
            except mysql.connector.Error as error:
                return self.send_error("InternalError", error)

            return self.send_success()

        else:
            return self.send_error("NotAuthorized", "NOT_AUTHORIZED")

    # TODO
    def update_subtask(self, output):
        # Check if user is authenticated
        if self.__auth:
            # Get output argument and check it
            try:
                name = output.get("name", "")
                state = output.get("state", "")
                date = output.get("date", "")
                task_id = output.get("task_id", "")
                labels_id = output.get("labels_id", [])
                SubTask(name, state, date, task_id, labels_id)
            except AttributeError as error:
                return self.send_error("InvalidJSONFormat", error)
            except TypeError as error:
                return self.send_error("InvalidJSONFormat", error)
            except ValueError as error:
                return self.send_error("InvalidJSONFormat", error)

            sql = ("SELECT * FROM User_has_Task "
                   "INNER JOIN Task ON User_has_Task.Task_idTask = Task.idTask "
                   "INNER JOIN Sub_Task ON Task.idTask = Sub_Task.Task_idTask "
                   "WHERE User_has_Task.User_idUser = %s AND Task.idTask = %s")

            # Checks if the user owns the sub_tasks
            try:
                self.__cursor.execute(sql, (self.__user_id, task_id,))
                result = self.__cursor.fetchall()
            except mysql.connector.Error as error:
                return self.send_error("InternalError", error)
            if not result:
                return self.send_error("NotAuthorized", "NOT_AUTHORIZED")

            print(result)

        else:
            return self.send_error("NotAuthorized", "NOT_AUTHORIZED")

    # Verified
    def write_log(self, message, event):
        with open("log.txt", "a") as log_file:
            date = datetime.datetime.now()
            log_file.write(date.strftime(f"%Y:%m:%d %H:%M:%S {self.__address[0]}:{self.__address[1]} {event} : {message}\n"))

    # Verified
    def send_error(self, event, message, server_answer="response") -> int:
        self.__database.rollback()
        self.write_log(message, event)
        try:
            self.__conn.send(self.json_maker(server_answer, "no", event).encode('utf-8'))
        except ssl.SSLEOFError as error:
            self.write_log("Client aborted connection", "ssl.SSLEOFError")
            return -1
        return 0

    # Verified
    def send_success(self, content=None, server_answer="response") -> int:
        self.__database.rollback()
        try:
            self.__conn.send(self.json_maker(server_answer, "yes", error=None, content=content).encode('utf-8'))
        except ssl.SSLEOFError:
            self.write_log("Client aborted connection", "ssl.SSLEOFError")
            return -1
        return 0

    # Verified
    @staticmethod
    def json_maker(server_answer, success, error=None, content=None):
        if content:
            return json.dumps({
                "server": server_answer,
                "success": success,
                "error": error,
                "content": content
            })
        else:
            return json.dumps({
                "server": server_answer,
                "success": success,
                "error": error,
            })
