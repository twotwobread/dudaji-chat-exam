import socket
import threading
from collections import deque

from client_socket import ClientSocket
from command.command import Command
from config.connect_config import BUFFER_SIZE
from dto.chat_dto import ChatDTO


class Server:
    def __init__(self, logger, host, port):
        self.logger = logger
        self.host = host
        self.port = port
        self.client_sockets = []
        self.client_commands = deque()

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        self.thread_lock = threading.Lock()

    def close_client_socket(self, client_socket: ClientSocket):
        if client_socket in self.client_sockets:
            self.client_sockets.remove(client_socket)
            self.logger.info("Rest Clients : %s", len(self.client_sockets))
        client_socket.close()

    def add_command(self, command: Command):
        with self.thread_lock:
            self.client_commands.append(command)

    def run(self):
        self.logger.info(">> Wait")
        threading.Thread(target=self.process_command).start()
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
        with self.thread_lock:
            for client_socket in self.client_sockets:
                if client_socket.get_client_socket() != socket:
                    client_socket.send(message)

    def process_command(self):
        while True:
            while self.client_commands:
                with self.thread_lock:
                    command = self.client_commands.popleft()
                command.execute()
