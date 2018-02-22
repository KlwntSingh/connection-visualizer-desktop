from config.config import CONFIG
from services.LoggerService import logger
cache_object = CONFIG["CACHING-FILE"]

if not cache_object:
    cache_object = {}

class CacheService:
    """
    This class provides caching service
    Caching can either be in-memory or sqlite db based depending on user configuration
    For Now, It supports in-memory caching
    """
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