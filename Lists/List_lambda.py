# первый
def car(lst):
    return lst(True)

# хвост
def cdr(lst):
    return lst(False)

# конструктор нового элемента
def cons(val, lst):
    return (lambda a: val if a else lst)

def isList(val):
    from typing import Callable
    return isinstance(val, Callable)
