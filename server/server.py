from objects.C_Client import Client
from colorama import Fore, Style
import mysql.connector
import threading
import socket
import ssl
import sys


if __name__ == "__main__":
    try:
        if sys.argv[1] == "-p":
            try:
                nb = int(sys.argv[2])
                port = nb
            except ValueError as error:
                raise ValueError("The value must be an integer")
            if nb < 0 or nb > 65535:
                raise ValueError("The value must be between 0 and 65534")
        else:
            raise ValueError("This argument does not exist")
    except IndexError:
        port = 5000

    open_sockets = []
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('./certs/srv/YeGrec.pem', './certs/srv/YeGrec.key')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    secure_sock = context.wrap_socket(server, server_side=True)

    print("Trying to reach mysql server... ", end="")

    try:
        database = mysql.connector.connect(
            host="127.0.0.1",
            port="3306",
            user="root",
            password="toto",
            database="YeGrec"
        )
        cursor = database.cursor(buffered=True)
    except mysql.connector.errors.DatabaseError:
        print(Fore.RED + "Failed")
        print("Can't reach database server" + Style.RESET_ALL)
        sys.exit(-1)

    print(Fore.GREEN + "OK" + Style.RESET_ALL)

    while True:
        print("Waiting for connections...")
        try:
            (conn, (ip, port)) = secure_sock.accept()
        except ConnectionAbortedError:
            print('Client aborted connection')
            continue
        except ConnectionResetError:
            print('Client aborted connection')
            continue
        except ssl.SSLError:
            print('SSL handshake error')
            continue

        print(f"Client {ip}:{port} is connected !")
        client = Client(conn, ip, port, cursor, database)
        thread = threading.Thread(target=client.run())
        thread.start()
        open_sockets.append(thread)
