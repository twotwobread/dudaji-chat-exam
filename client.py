import socket
import sys
import threading

from app.config.connect_config import BLANK, BUFFER_SIZE, HOST, PORT, QUIT, UNKNOWN
from app.dto.chat_dto import ChatDTO


class Client:
    def __init__(self, host, port, name):
        self.host = host
        self.port = port
        self.name = name
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

    def run(self):
        send_dto = ChatDTO(self.name, BLANK)
        self.client_socket.send(send_dto.json_data.encode())
        print(f"{NAME}님이 접속하였습니다.")

        recv_thread = threading.Thread(target=self.recv_data)
        send_thread = threading.Thread(target=self.send_data)
        recv_thread.start()
        send_thread.start()

        recv_thread.join()
        send_thread.join()
        print("Client Closed.")

    def recv_data(self):
        while True:
            try:
                recv_dto = ChatDTO.covertFromByteCode(self.client_socket.recv(BUFFER_SIZE).decode())
                print(recv_dto)
            except ConnectionAbortedError:
                break

    def send_data(self):
        while True:
            message = input("")
            send_dto = ChatDTO(self.name, message)

            self.client_socket.send(send_dto.json_data.encode())
            if message == QUIT:
                break
        self.client_socket.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        NAME = sys.argv[1]
    else:
        NAME = UNKNOWN

    Client(HOST, PORT, NAME).run()
