from config.connect_config import HOST, PORT
from config.logger_config import getLogger
from server import Server

if __name__ == "__main__":
    Server(getLogger(), HOST, PORT).run()
