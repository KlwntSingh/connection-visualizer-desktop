import requests
from beans.RequestsException import RequestExceptions

class Request():
    """
    Wrapper over requests module
    Reason: change will be in this class only when replacing request module to any other async.io module like grequests
    """
    def get(self, url):
        res = None
        try:
            res = requests.get(url)
        except requests.exceptions.ConnectionError as e:
            raise RequestExceptions(e)
        except requests.exceptions.RequestExceptions as e:
            raise RequestExceptions(e, exit=True)

        return res