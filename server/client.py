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
                "client": "login",
                "username": "valentin",
                "password": "totototo"
            }
        ])
        conn.send(credentials.encode('utf-8'))

        credentials = json.dumps([
            {
                "client": "create_task",
                "content": {
                    "name": "Tâche test",
                    "state": "todo",
                    "date": "1000-01-01 00:00:00",
                    "description": "Descriptino de test",
                    "priority": "medium",
                    "labels": {},
                    "users": {}
                }
            }
        ])
        conn.send(credentials.encode('utf-8'))

        msg = ""
        buffer = conn.recv(1024)
        rc = buffer.decode('utf-8')
        if rc != msg:
            print(rc)
            msg = rc

        # conn.send(json.dumps([
        #     {
        #         "client": "disconnect"
        #     }
        # ]).encode('utf-8'))

