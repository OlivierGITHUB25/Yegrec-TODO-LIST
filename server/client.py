import socket
import json
import ssl
import time

hostname = '127.0.0.1'
context = ssl.create_default_context()
context.load_verify_locations("./certs/CA.crt")

with socket.create_connection((hostname, 5000)) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as conn:
        print(f"Connected to {hostname} with TLS !")
        time.sleep(1)
        credentials = json.dumps([
            {
                "action": "login",
                "username": "root",
                "password": "tot5o"
            }
        ])
        conn.send(credentials.encode('utf-8'))
        time.sleep(1)
        done = json.dumps([
            {
                "action": "disconnect"
            }
        ])
        conn.send(done.encode('utf-8'))
