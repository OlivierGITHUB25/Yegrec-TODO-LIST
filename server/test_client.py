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
        data = json.dumps({
                "client": "login",
                "username": "valentin",
                "password": "azerty68"
        })
        conn.send(data.encode('utf-8'))

        data = json.dumps({
                "client": "get_users"
        })
        conn.send(data.encode('utf-8'))

        # data = json.dumps({
        #         "client": "get_tasks"
        # })
        # conn.send(data.encode('utf-8'))

        # data = json.dumps({
        #         "client": "get_subtasks",
        #         "task_id": 46
        # })
        # conn.send(data.encode('utf-8'))

        # data = json.dumps({
        #         "client": "create_label",
        #         "name": "Security",
        #         "color": "#FFFFFF",
        # })
        # conn.send(data.encode('utf-8'))

        # data = json.dumps({
        #     "client": "create_task",
        #     "name": "Switching",
        #     "state": 1,
        #     "priority": 2,
        #     "date": "2023-10-20 00:00:00",
        #     "description": "Description de test",
        #     "labels_id": [7],
        #     "users_id": [4, 5]
        # })
        # conn.send(data.encode('utf-8'))

        # data = json.dumps({
        #         "client": "create_subtask",
        #         "name": "port sfp autre",
        #         "state": 2,
        #         "date": "2023-10-20 00:00:00",
        #         "task_id": 45,
        #         "labels_id": [6, 8],
        # })
        # conn.send(data.encode('utf-8'))

        while True:
            msg = ""
            buffer = conn.recv(1024)
            rc = buffer.decode('utf-8')
            if rc != msg:
                print(rc)
                msg = rc
