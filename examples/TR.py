from typing import Callable

class TR:
    def __init__(self, f, *args, **kwargs):
        self.f = f
        self.args = args
        self.kwargs = kwargs
    def __call__(self):
        return self.f(*self.args, **self.kwargs)

def evalTR(value):
    while isinstance(value, TR):
        value = value()
    return value

def suman(n, acc):
    return acc if n <= 0 else TR(suman, n - 1, acc + n)

def isOdd(n):
    return False if n == 0 else TR(isEven, n - 1)

def isEven(n):
    return True if n == 0 else TR(isOdd, n - 1)

while n := int(input()):
    print(evalTR(suman(n, 0)))
    # print(evalTR(isEven(n)), evalTR(isOdd(n)))