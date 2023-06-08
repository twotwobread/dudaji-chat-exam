import datetime
import logging
import logging.handlers
import os

LOG_FORMAT = "[%(asctime)-15s] <thread_id : %(thread)d> (%(filename)s:%(lineno)d) %(name)s:%(levelname)s - %(message)s"
LOG_FILE_PATH = "{}/logs".format(os.path.dirname(os.path.realpath(__file__)) + "/..")

if not os.path.exists(LOG_FILE_PATH):
    os.makedirs(LOG_FILE_PATH)


def getLogger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # console logger 설정
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(formatter)

    # file logger 설정
    file_name = "log-{}".format(datetime.datetime.now().strftime("%Y%m%d"))
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename="{}/{}".format(LOG_FILE_PATH, file_name), when="midnight", interval=1, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger
