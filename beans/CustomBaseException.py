class CustomBaseException(Exception):
    def __init__(self, *arg, **kargs):
        self.exit = kargs.get("exit", False)
        super(CustomBaseException, self).__init__(*arg)


    def __str__(self):
        return super(CustomBaseException, self).__str__()
