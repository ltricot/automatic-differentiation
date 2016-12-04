from weakref import WeakValueDictionary
from functools import wraps
import numpy as np


def varize(function):
    @wraps(function)
    def op(self, other):
        if isinstance(other, int):
            other = Variable(str(other), other, True)
        return function(self, other)
    return op


class Variable:

    nametovar = WeakValueDictionary()

    def __init__(self, name, val=None, fixed=False):
        self.__class__.nametovar[name] = self
        self.fixed = fixed
        self.name = name
        self.val = val

    def __call__(self, varvalues):
        for k, v in varvalues.items():
            self.__class__.nametovar[k].val = v
        return self.forward()

    def forward(self):
        return self.val

    def backward(self, name):
        if name == self.name:
            return Variable(name='1', val=1, fixed=True)
        return Variable(name='0', val=0, fixed=True)

    def __str__(self):
        return self.name

    @varize
    def __add__(self, other):
        return Add(self, other, name='({} + {})'.format(self.name, other.name))

    @varize
    def __sub__(self, other):
        return Add(self,
            other * Variable(name='-1', val=-1, fixed=True),
            name='({} - {})'.format(self.name, other.name))

    @varize
    def __mul__(self, other):
        return Mul(self, other, name='({} * {})'.format(self.name, other.name))

    @varize
    def __truediv__(self, other):
        return Div(self, other, name='({} / {})'.format(self.name, other.name))


class Op(Variable):

    def __init__(self, a, b, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.a, self.b = a, b


class Add(Op):

    def forward(self):
        return self.a.forward() + self.b.forward()

    def backward(self, name):
        v = super().backward(name)
        if v.val:
            return v
        return self.a.backward(name) + self.b.backward(name)


class Mul(Op):

    def forward(self):
        return self.a.forward() * self.b.forward()

    def backward(self, name):
        v = super().backward(name)
        if v.val:
            return v
        return self.b * self.a.backward(name) + self.a * self.b.backward(name)


class Div(Op):

    def forward(self):
        return self.a.forward() / self.b.forward()

    def backward(self, name):
        num = self.b * self.a.backward(name) - self.a * self.b.backward(name)
        return num / (self.b * self.b)
