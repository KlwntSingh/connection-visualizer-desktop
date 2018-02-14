import logging
from config.config import CONFIG
import os

__LOG_PATH = CONFIG["LOGS_PATH"]
print(__LOG_PATH)
if not os.path.isdir(__LOG_PATH):
    os.makedirs(__LOG_PATH)

class Logger():

    __logger = None

    @classmethod
    def getLogger(cls):

        if not cls.__logger:
            logger = logging.getLogger(CONFIG.get("APP_NAME"))
            flhdlr = logging.FileHandler(CONFIG["LOGS_PATH"] + CONFIG["LOGS_FILE_NAME"])
            formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
            flhdlr.setFormatter(formatter)
            console_handler = logging.StreamHandler()
            logger.addHandler(console_handler)
            logger.addHandler(flhdlr)
            logger.setLevel(CONFIG.get("LOGGING_LEVEL"))
            cls.__logger = logger

        return cls.__logger
