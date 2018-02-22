import time

KEY_TIMEOUT = 15000

class ExpiringDictionary():
    """
    Wrapper over traditional Dictionary which expires and removes key from dictionary after particular period of timeout time
    """
    current_milli_time = lambda x: int(round(time.time() * 1000))

    def __init__(self, atime=KEY_TIMEOUT):
        self.dictionary = dict()
        self.atime = atime

    def __str__(self):
        ls = []
        for i in self.dictionary:
            ls.append((i, self.dictionary[i],))
        return str(ls)

    def get(self, key):
        current_milli_time = self.current_milli_time

        if key in self.dictionary:
            val = self.dictionary[key]

            current_time = current_milli_time()

            if ((current_time - val.put_time) < self.atime):
                return val
            else:
                self.pop(key)
                return None
        else:
            return None

    def put(self, key, value):
        current_milli_time = self.current_milli_time

        put_time = current_milli_time()

        if key in self.dictionary:
            self.dictionary[key].put_time = put_time
        else:
            value.put_time = put_time
            self.dictionary[key] = value

    def pop(self, key):
        self.dictionary.pop(key)
        return None




