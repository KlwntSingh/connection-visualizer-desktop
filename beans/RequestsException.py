from beans.CustomBaseException import CustomBaseException

class RequestExceptions(CustomBaseException):
    """
    Custom Exception class for requests exceptions
    """
    def __init__(self, *args, **kargs):
        super(RequestExceptions, self).__init__(*args, **kargs)

