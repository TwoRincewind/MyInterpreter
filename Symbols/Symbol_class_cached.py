class Symbol:
    _name: str = ...
    def __init__(self, name):
        self._name = name
    @property
    def name(self):
        return self._name


CACHE = dict()


def symbol(name: str) -> Symbol:
    if name not in CACHE:
        print("caching new", name)
        CACHE[name] = Symbol(name)
    return CACHE[name]

def symname(sym: Symbol) -> str:
    return sym.name

def isSymbol(obj) -> bool:
    return isinstance(obj, Symbol)
