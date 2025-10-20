class Symbol:
    _name: str = ...
    def __init__(self, name):
        self._name = name
    @property
    def name(self):
        return self._name


def symbol(name: str) -> Symbol:
    return Symbol(name)

def symname(sym: Symbol) -> str:
    return sym.name

def isSymbol(obj) -> bool:
    return isinstance(obj, Symbol)
