import socket
import ssl

hostname = '127.0.0.1'
context = ssl.create_default_context()
context.load_verify_locations("./certs/CA.crt")

with socket.create_connection((hostname, 5000)) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        print(ssock.version())
