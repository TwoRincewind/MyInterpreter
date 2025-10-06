# первый
def car(lst):
    return lst[0]

# хвост
def cdr(lst):
    return lst[1]

# конструктор нового элемента
def cons(val, lst):
    return (val, lst)

def isList(val):
    return isinstance(val, tuple)
