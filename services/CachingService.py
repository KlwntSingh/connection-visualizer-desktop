from config.config import CONFIG
from services.LoggerService import logger
cache_object = CONFIG["CACHING-FILE"]

if not cache_object:
    cache_object = {}

class CacheService:

    @staticmethod
    def put(key, value):
        cache_object[key] = value

    @staticmethod
    def get(key):
        logger.debug("Application cache used")
        if CacheService.has(key):
            return cache_object[key]
        else:
            return None

    @staticmethod
    def has(key):
        return key in cache_object