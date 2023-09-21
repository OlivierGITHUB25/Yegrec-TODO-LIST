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


def login(conn, output):
    try:
        for c in output:
            username = c["username"]
            password = c["password"]
    except KeyError:
        print("FORMAT JSON INVALIDE")
    with open("users.json", "r") as user_DB:
        DB = json.load(user_DB)
        for c in DB:
            if c["username"] == username:
                if get_hash(password, c["password"]):
                    print(f"User {username} is logged in !")
                    return 0
        return -1


def sign_up(conn, output):
    pass


def get_hash(password, hash):                   ##A FIXER
    print(password, hash)
    if bcrypt.checkpw(password, hash):
        return True
    else:
        return False


def thread_socket(conn, ip, port):
    print(f"Client {ip}:{port} is connected !")

    received_message = ""
    old_msg = ""

    while True:
        buffer = conn.recv(1024)
        received_message = buffer.decode('utf-8')

        if received_message != old_msg:
            try:
                output = json.loads(received_message)
                for c in output:
                    action = c["action"]
                    received_message = old_msg
            except KeyError:
                print("FORMAT JSON INVALIDE")
                received_message = old_msg
                continue

            if action == "login":
                login(conn, output)
            elif action == "sign_up":
                sign_up(conn, output)
            else:
                print("FORMAT JSON INVALIDE")


if __name__ == "__main__":
    open_sockets = []

    while True:
        print("Waiting for connection...")
        try:
            (conn, (ip, port)) = secure_sock.accept()
        except ConnectionAbortedError:
            print('Client aborted connection')
            continue

        thread = threading.Thread(target=thread_socket, args=[conn, ip, port])
        thread.start()
        open_sockets.append(thread)

