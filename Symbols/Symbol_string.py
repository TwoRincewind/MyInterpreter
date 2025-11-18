pref = '\0'

def symbol(name: str) -> str:
    return pref + name

def symname(sym: str) -> str:
    return sym[1:]

def symkey(sym: str) -> str:
    return sym

def isSymbol(obj) -> bool:
    return isinstance(obj, str) and obj != '' and obj[0] == pref
