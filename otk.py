import random
import string

class emailKey:
    def __init__(self):
        pass

    def getKey(self, size=7, chars=string.digits):
        self.key = "".join(random.choice(chars) for _ in range(size))
        print(self.key)
        return self.key


    def check(self, entry, key):
        if str(entry) != str(key):
            return 2
        if str(entry) == str(key):
            return 1
