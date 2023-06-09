import socket
import threading

from client_socket import ClientSocket
from dto.chat_dto import ChatDTO

from config.connect_config import BUFFER_SIZE


class Server:
    def __init__(self, logger, host, port):
        self.logger = logger
        self.host = host
        self.port = port
        self.client_sockets = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

    def close_client_socket(self, client_socket: ClientSocket):
        if client_socket in self.client_sockets:
            self.client_sockets.remove(client_socket)
            self.logger.info("Rest Clients : %s", len(self.client_sockets))
        client_socket.close()

    def run(self):
        self.logger.info(">> Wait")
        try:
            while True:
                client_socket, client_addr = self.server_socket.accept()
                recv_dto = ChatDTO.covertFromByteCode(client_socket.recv(BUFFER_SIZE).decode())
                self.logger.info(f"Connected to client: {client_addr}")

                socket = ClientSocket(self, self.logger, client_socket, client_addr, recv_dto.name)
                threading.Thread(target=socket.communicate).start()
                self.client_sockets.append(socket)
                self.logger.info("참가자 수 : %s", len(self.client_sockets))
        except Exception as e:
            self.logger.error(f"Server Error : {e}")
        finally:
            self.server_socket.close()

    def broadcast(self, socket, message):
        for client_socket in self.client_sockets:
            if client_socket.get_client_socket() != socket:
                client_socket.send(message)
