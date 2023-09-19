import threading
import socket
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('./certs/srv/YeGrec.pem', './certs/srv/YeGrec.key')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
server.bind(('127.0.0.1', 5000))
server.listen(5)
secure_sock = context.wrap_socket(server, server_side=True)


def thread_socket(conn, ip, port):
    print(f"Client {ip}:{port} is connected !")


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

