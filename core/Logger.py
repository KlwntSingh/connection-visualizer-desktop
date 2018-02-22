import logging
from config.config import CONFIG
import os

__LOG_PATH = CONFIG["LOGS_PATH"]

if not os.path.isdir(__LOG_PATH):
    os.makedirs(__LOG_PATH)

## Note:- Currently logger is working in both file and console mode

class Logger():
    """
    This class is wrapper over logging module in python to make it singleton
    This class is for logging different levels of execeptions.
    getLogger method returns instance of logger
    """
    __logger = None

    @classmethod
    def getLogger(cls):

        if not cls.__logger:
            logger = logging.getLogger(CONFIG.get("APP_NAME"))

            flhdlr = logging.FileHandler(CONFIG["LOGS_PATH"] + CONFIG["LOGS_FILE_NAME"])
            console_handler = logging.StreamHandler()

            formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
            flhdlr.setFormatter(formatter)

            logger.addHandler(console_handler)
            logger.addHandler(flhdlr)

            logger.setLevel(CONFIG.get("LOGGING_LEVEL"))

            cls.__logger = logger

        return cls.__logger
