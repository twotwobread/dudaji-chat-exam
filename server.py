import json
import socket
from _thread import start_new_thread

from config.connect_config import BUFFER_SIZE, HOST, PORT
from config.logger_config import getLogger

client_sockets = []
logger = getLogger()


def threaded(client_socket, addr, NAME):
    entering_message = f"{NAME}:{addr}님이 접속하였습니다."
    logger.info(entering_message)

    while True:
        try:
            data = client_socket.recv(1024).decode()  # 1024byte
            if not data:
                logger.info("%s님이 나갔습니다.", NAME)
                break
            logger.info("%s [%s:%s] %s", NAME, addr[0], addr[1], json.loads(data))
            boroadcast = json.dumps(data).encode()
            for client in client_sockets:
                if client != client_socket:
                    client.send(boroadcast)

        except Exception:
            break

    if client_socket in client_sockets:
        client_sockets.remove(client_socket)
        logger.info("Rest Clients : %s", len(client_sockets))
    client_socket.close()


logger.info(">> Server Start")
server_socket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM
)  # AF_INET: IP Version 4, SOCK_STREAM: TCP 패킷 허용. row/"stream"/데이터그램 socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 포트 여러번 바인드하면 발생하는 에러 방지
server_socket.bind((HOST, PORT))
server_socket.listen()  # 클라이언트를 기다림. 인수로는 동시 접속할 최대한의 클라이언트 수. 실제 송수신은 accept을 통해서

try:
    while True:
        logger.info(">> Wait")
        client_socket, addr = server_socket.accept()
        NAME = json.loads(client_socket.recv(BUFFER_SIZE).decode())["name"]
        client_sockets.append(client_socket)
        start_new_thread(threaded, (client_socket, addr, NAME))
        logger.info("참가자 수 : %s", len(client_sockets))
except Exception as e:
    logger.error("에러발생 : %s", e)
finally:
    server_socket.close()
    logger.close()
