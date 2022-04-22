from functools import partial

class Q:
    def __init__(self):
        self.funcs = []

    def put(self, priority, func, *args):
        if len(args) == 0:
            self.funcs.insert(priority, func)
        else:
            self.funcs.insert(priority, partial(func, *args))

    def get(self):
        while not self.funcs:
            continue
        return self.funcs.pop()
