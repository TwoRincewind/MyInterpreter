# первый
def cons(x, y):
    return lambda f: f(x, y)

# хвост
def car(l):
    return l(lambda x, _: x)

# конструктор нового элемента
def cdr(l):
    return l(lambda _, y: y)

def isList(val):
    from typing import Callable
    return isinstance(val, Callable)
