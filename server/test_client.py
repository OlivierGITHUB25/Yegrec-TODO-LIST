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

        # data = json.dumps({
        #         "client": "create_label",
        #         "name": "label1 val",
        #         "color": "#FFFFFF",
        # })
        # conn.send(data.encode('utf-8'))
        #
        # data = json.dumps({
        #         "client": "create_label",
        #         "name": "label2 val",
        #         "color": "#FFFFFF",
        # })
        # conn.send(data.encode('utf-8'))

        # data = json.dumps({
        #     "client": "create_task",
        #     "name": "tache olivier",
        #     "state": 1,
        #     "priority": 2,
        #     "date": "2023-10-20 00:00:00",
        #     "description": "Description de test",
        #     "labels_id": [],
        #     "users_id": []
        # })
        # conn.send(data.encode('utf-8'))

        # data = json.dumps({
        #         "client": "update_task",
        #         "task_id": 4,
        #         "name": "Switching",
        #         "state": 1,
        #         "priority": 2,
        #         "date": "2023-10-20 00:00:00",
        #         "description": "Description de test",
        #         "labels_id": [],
        #         "users_id": []
        # })
        # conn.send(data.encode('utf-8'))

        # data = json.dumps({
        #         "client": "get_users"
        # })
        # conn.send(data.encode('utf-8'))

        # data = json.dumps({
        #         "client": "get_users"
        # })
        # conn.send(data.encode('utf-8'))

        # data = json.dumps({
        #         "client": "get_subtasks",
        #         "task_id": 6
        # })
        # conn.send(data.encode('utf-8'))

        # data = json.dumps({
        #         "client": "get_labels"
        # })
        # conn.send(data.encode('utf-8'))

        # data = json.dumps({
        #     "client": "create_task",
        #     "name": "val tâche 3",
        #     "state": 1,
        #     "priority": 2,
        #     "date": "2023-10-20 00:00:00",
        #     "description": "Description de test",
        #     "labels_id": [],
        #     "users_id": []
        # })
        # conn.send(data.encode('utf-8'))

        data = json.dumps({
                "client": "create_subtask",
                "name": "Sous-tâche val",
                "state": 2,
                "date": "2023-10-20 00:00:00",
                "task_id": 2,
                "labels_id": [],
        })
        conn.send(data.encode('utf-8'))

        while True:
            msg = ""
            buffer = conn.recv(1024)
            rc = buffer.decode('utf-8')
            if rc != msg:
                print(rc)
                msg = rc
