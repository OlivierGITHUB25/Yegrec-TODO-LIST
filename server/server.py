import threading
import socket
import bcrypt
import json
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('./certs/srv/YeGrec.pem', './certs/srv/YeGrec.key')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
server.bind(('127.0.0.1', 5000))
server.listen(5)
secure_sock = context.wrap_socket(server, server_side=True)


class Client:
    def __init__(self, conn):
        self.__conn = conn

    def run(self):
        received_msg = ""
        previous_msg = ""
        action = ""

        while action != "disconnect":
            buffer = self.__conn.recv(1024)
            received_message = buffer.decode('utf-8')
            if received_message != previous_msg:
                try:
                    output = json.loads(received_message)
                    for item in output:
                        action = item["action"]
                        received_message = previous_msg
                except KeyError:
                    print("Invalid json format")
                    received_message = previous_msg
                    continue
                except json.decoder.JSONDecodeError:
                    print("Invalid json format")
                    received_message = previous_msg
                    continue

                if action == "login":
                    self.login(output)
                elif action == "sign_up":
                    self.sign_up(output)

    def login(self, output):
        password = ""
        username = ""

        try:
            for item in output:
                username = item["username"]
                password = item["password"]
        except KeyError:
            print("Invalid json format")
            return -1
        with open("users.json", "r") as user_DB:
            _user_DB = json.load(user_DB)
            for item in _user_DB:
                if item["username"] == username:
                    if bcrypt.checkpw(password.encode('utf8'), item["password"].encode('utf8')):
                        print(f"User {username} is logged in !")
                        self.__conn.send(self.json_maker("authorized").encode('utf-8'))
                        return 0
                    else:
                        print(f"{username} enter wrong password")

        self.__conn.send(self.json_maker("unauthorized").encode('utf-8'))

    def sign_up(self, output):
        pass

    @staticmethod
    def json_maker(from_server):
        return json.dumps([
            {
                "FromServer": from_server
            }
        ])


if __name__ == "__main__":
    open_sockets = []

    while True:
        print("Waiting for connection...")
        try:
            (conn, (ip, port)) = secure_sock.accept()
        except ConnectionAbortedError:
            print('Client aborted connection')
            continue

        print(f"Client {ip}:{port} is connected !")
        client = Client(conn)
        thread = threading.Thread(target=client.run())
        thread.start()
        open_sockets.append(thread)
