__author__ = 'Donhilion'

class Env(object):

    def __init__(self, parent=None):
        if parent is None:
            parent = {}
        self.parent = parent
        self.dict = {}

    def __contains__(self, item):
        return item in self.dict or item in self.parent

    def directly_defined(self, item):
        return item in self.dict

    def __getitem__(self, item):
        if item not in self:
            raise Exception("%s is not defined" % item)
        return self.dict[item] if item in self.dict else self.parent[item]

    def __setitem__(self, key, value):
        if key in self.dict:
            self.dict[key] = value
        elif key in self.parent:
            self.parent[key] = value
        else:
            raise Exception("%s is not defined" % key)

    def declare(self, key, value):
        self.dict[key] = value
