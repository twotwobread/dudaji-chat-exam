from command.send_broadcast_command import SendBroadcastCommand
from config.connect_config import BUFFER_SIZE, QUIT
from dto.chat_dto import ChatDTO


class ClientSocket:
    def __init__(self, server, logger, client_socket, client_addr, name):
        self.server = server
        self.logger = logger
        self.client_socket = client_socket
        self.client_addr = client_addr
        self.name = name

    def __eq__(self, other):
        return self.client_socket == other.get_client_socket()

    def close(self):
        self.client_socket.close()

    def get_client_socket(self):
        return self.client_socket

    def send(self, message):
        self.client_socket.send(message)

    def communicate(self):
        self.logger.info(f"{self.name}:{self.client_addr}님이 접속하였습니다.")

        while True:
            try:
                recv_dto = ChatDTO.covertFromByteCode(self.client_socket.recv(BUFFER_SIZE).decode())
                self.logger.info("%s [%s:%s] %s", self.name, self.client_addr[0], self.client_addr[1], recv_dto)
                if recv_dto.body == QUIT:
                    self.logger.info("%s님이 나갔습니다.", self.name)
                    break
                self.server.add_command(
                    SendBroadcastCommand(self.server, self.client_socket, recv_dto.json_data.encode())
                )
            except Exception:
                break
        self.server.close_client_socket(self)
