from Lists.List_absolute_lambda import *

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


while True:
    lst = NIL
    for elem in reversed(input("enter list values: ").split()):
        if elem == ":q":
            exit(0)
        try:
            elem_ = eval(elem)
            if isinstance(elem_, str) or isinstance(elem_, int):
                elem = elem_
        except Exception as _:
            pass
        lst = cons(elem, lst)
    print(show(lst))

