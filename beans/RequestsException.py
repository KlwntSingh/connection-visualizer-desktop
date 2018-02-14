from beans.CustomBaseException import CustomBaseException

class RequestExceptions(CustomBaseException):
    def __init__(self, *args, **kargs):
        super(RequestExceptions, self).__init__(*args, **kargs)

