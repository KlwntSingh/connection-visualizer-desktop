import re
import socket
from config.config import CONFIG
from core.APIRequest import Request
from beans.RequestsException import RequestExceptions
import AppUtils as au
from services.LoggerService import logger
from services.CachingService import CacheService

request = Request()
REGEX_PATTERN = 'https?:\/\/(www.)?([a-zA-Z\d\-\.]*\.[a-zA-Z]{2,3})|(localhost)'

IP_API = CONFIG["IP_API"]

class IPInfo():

    def __init__(self, **kwargs):
        shared_data = kwargs
        self.shared_data = shared_data.get("expiring_map")
        self.ignored_ip_set = shared_data.get("ignored_ip_set")
        self.ignored_ip_set.add('127.0.0.1')
        self.ignored_ip_set.add('127.0.1.1')
        self.getIPForAPI()
        self.executor = shared_data.get("executors")

    def getIPForAPI(self):
        p = re.search(REGEX_PATTERN, IP_API).groups()
        DOMAIN_NAME = p[len(p) - 2]
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
        def temp_cb(fut):
            if fut:
                rs = fut.result().json()
                CacheService.put(ip, rs)
                cb(rs)
            else:
                cb(None)

        if ip not in self.ignored_ip_set:
            try:
                if not CacheService.has(ip):
                    futureObj = self.executor.submit(request.get, IP_API + ip)
                    futureObj.add_done_callback(temp_cb)
                else:
                    cb(CacheService.get(ip))
            except RuntimeError as e:
                logger.warn(e)
        else:
            cb(None)