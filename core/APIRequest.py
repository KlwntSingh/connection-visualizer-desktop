import requests
from beans.RequestsException import RequestExceptions

class Request():
    def get(self, url):
        res = None
        try:
            res = requests.get(url)
        except requests.exceptions.ConnectionError as e:
            raise RequestExceptions(e)
        except requests.exceptions.RequestExceptions as e:
            raise RequestExceptions(e, exit=True)

        return res