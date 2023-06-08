import json
import socket
import sys
from _thread import start_new_thread

from config.connect_config import BUFFER_SIZE, HOST, PORT, QUIT, UNKONWN

if len(sys.argv) > 1:
    NAME = sys.argv[1]
else:
    NAME = UNKONWN

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


def recv_data(client_socket):
    while True:
        received_data = client_socket.recv(BUFFER_SIZE).decode()
        message = eval(json.loads(received_data))
        name = message["name"]
        body = message["body"]
        print(f"{name} : {body}")


start_new_thread(recv_data, (client_socket,))
client_socket.send(json.dumps({"name": NAME}).encode())
print(f"{NAME}님이 접속하였습니다.")

while True:
    sending_data = {}
    message = input("")
    if message == QUIT:
        break

    sending_data["name"] = NAME
    sending_data["body"] = message
    client_socket.send(json.dumps(sending_data).encode())
client_socket.close()
