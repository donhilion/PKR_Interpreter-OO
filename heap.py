__author__ = 'Donhilion'

class Heap(object):

    def __init__(self):
        self.memory = []
        self.free = []

    def alloc(self):
        if len(self.free) > 0:
            return self.free.pop()
        self.memory.append(None)
        addr = len(self.memory)-1
        return addr

    def free(self, addr):
        self.memory[addr] = None
        self.free.append(addr)

    def __getitem__(self, item):
        return self.memory[item]

    def __setitem__(self, key, value):
        self.memory[key] = value

heap = Heap()
