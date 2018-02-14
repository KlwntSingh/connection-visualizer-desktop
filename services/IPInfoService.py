from config.config import CONFIG
from core.APIRequest import Request
import re
from beans.RequestsException import RequestExceptions
import AppUtils as au
from services.LoggerService import logger
import concurrent.futures
import time
import socket

request = Request()
REGEX_PATTERN = 'https?:\/\/(www.)?([a-zA-Z\d\-\.]*\.[a-zA-Z]{2,3})|(localhost)'

IP_API = CONFIG["IP_API"]

class IPInfo():

    def __init__(self, **kwargs):
        shared_data = kwargs
        self.shared_data = shared_data.get("expiring_map")
        self.ignored_ip_set = shared_data.get("ignored_ip_set")
        self.getIPForAPI()
        self.executor = shared_data.get("executors")

    def getIPForAPI(self):
        p = re.search(REGEX_PATTERN, IP_API).groups()
        DOMAIN_NAME = p[len(p) - 1]
        DOMAIN_URL = DOMAIN_NAME
        try:
            res = socket.gethostbyname(DOMAIN_URL)
            self.api_ip = res
            self.ignored_ip_set.add(self.api_ip)
        except RequestExceptions as e:
            logger.error(e, exc_info=True)
            if e.exit:
                au.exitFromApp()

    def getDomainNamesForIP(self, ip, cb):
        if ip not in self.ignored_ip_set:
            futureObj = self.executor.submit(request.get, IP_API + ip)
            futureObj.add_done_callback(cb)
        else:
            cb(None)