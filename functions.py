from ast import Function
from heap import heap

__author__ = 'Donhilion'

class Alloc(Function):

    def __init__(self):
        Function.__init__(self, (), None)

    def call(self, args, env):
        return heap.alloc()

    def __str__(self):
        return "The predefined alloc function"