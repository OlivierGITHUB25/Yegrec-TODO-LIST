import socket
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('./certs/srv/YeGrec.pem', './certs/srv/YeGrec.key')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind(('127.0.0.1', 5000))
    sock.listen(5)
    print("Waiting for connection...")
    with context.wrap_socket(sock, server_side=True) as ssock:
        conn, address = ssock.accept()
