import threading

class ThreadFactory(threading.Thread):
    def __init__(self, cls, start_method, **kargs):
        self.class_instance = cls(**kargs)
        self.start_method = start_method
        self.toStop = threading.Event()
        super(ThreadFactory, self).__init__()

    def run(self):
        getattr(self.class_instance, self.start_method)(self.toStop)

    def stop(self):
        return self.toStop.set()

