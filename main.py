from List_lambda import *

NIL = cons(None, None)


def show(v):
    if isList(v):
        s = ""
        first = True
        while v != NIL:
            if first:
                first = False
            else:
                s += ' '
            s += show(car(v))
            v = cdr(v)
        return f"({s})"
    elif isinstance(v, str):
        return f'"{v}"'
    return str(v)


a = cons(1, cons("123", cons(3, NIL)))
b = cons(-1, cons(1, cons("", NIL)))
c = cons(a, cons(b, NIL))
d = cons(NIL, cons(NIL, NIL))
print(show(a))
print(show(b))
print(show(c))
print(show(d))

