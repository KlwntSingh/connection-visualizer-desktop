import threading

## Should be improved for passing event object to method invoked as optional

class ThreadFactory(threading.Thread):
    """
    Factory Class for running method of any class in new thread
    When invoking "start" method on instance of this class, It will call the method given as argument in instantiation
    and method will receive "event" object as argument whose condition will turned from instance of threadFactory to stop the called method
    """

    def __init__(self, cls, start_method, **kargs):
        self.class_instance = cls(**kargs)
        self.start_method = start_method
        self.toStop = threading.Event()
        super(ThreadFactory, self).__init__()

    def run(self):
        getattr(self.class_instance, self.start_method)(self.toStop)

    def stop(self):
        return self.toStop.set()

