import threading
import socket
import json
import ssl


class TCPSession:
    def __init__(self, hostname, port):
        self.__address = (hostname, port)
        self.__context = ssl.create_default_context()
        self.__context.load_verify_locations("./cert/CA.crt")
        self.__data = None
        self.__connected = False
        self.__error = None
        self.__init_connection()

    def init_connection(self):
        connection = threading.Thread(target=self.__init_connection)
        connection.start()

    def __init_connection(self):
        tcp_sock = socket.create_connection((self.__address[0], self.__address[1]))
        self.__conn = self.__context.wrap_socket(tcp_sock, server_hostname=self.__address[0])
        self.__connected = True
        rcv_data = threading.Thread(target=self.__receive_data)
        rcv_data.start()

    def __receive_data(self):
        if self.__connected:
            previous_msg = ""
            server_answer = ""

            while server_answer != "DISCONNECT":
                buffer = self.__conn.recv(1024)
                received_message = buffer.decode('utf-8')

                if received_message != previous_msg:
                    self.__data = json.loads(received_message)
                    server_answer = self.__data.get("server")

    def send_data(self, data):
        data = json.dumps(data)
        thread = threading.Thread(target=self.__send_data, args=[data])
        thread.start()

    def __send_data(self, data):
        if self.__connected:
            self.__conn.send(data.encode('utf-8'))

    def get_data(self):
        if self.__connected:
            while self.__data is None:
                continue
            data = self.__data
            self.__data = None
            return data
