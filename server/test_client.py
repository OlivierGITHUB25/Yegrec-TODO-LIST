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
                "password": "azerty68"
            }
        ])
        conn.send(credentials.encode('utf-8'))

        credentials = json.dumps([
            {
                "client": "create_subtask",
                "content": {
                    "name": "Sous tache",
                    "state": "2",
                    "date": "2023-10-20 00:00:00",
                    "task_id": "1",
                    "users_id": {},
                }
            }
        ])
        # credentials = json.dumps([
        #     {
        #         "client": "create_task",
        #         "content": {
        #             "name": "Acheter du pain",
        #             "state": "1",
        #             "priority": "1",
        #             "date": "2023-10-20 00:00:00",
        #             "description": "Description de test",
        #             "labels_id": {},
        #             "users_id": {},
        #         }
        #     }
        # ])
        conn.send(credentials.encode('utf-8'))

        while True:
            msg = ""
            buffer = conn.recv(1024)
            rc = buffer.decode('utf-8')
            if rc != msg:
                print(rc)
                msg = rc
