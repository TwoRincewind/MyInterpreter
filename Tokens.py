from enum import Enum
from Symbols.Symbol_string import symkey


class Env:
    frame: dict = ...
    parent = ...

    def __init__(self, parent):
        self.frame = dict()
        self.parent = parent

    def add(self, k, v) -> None:
        # if k in dict.keys():  # config moment: immutible
        #     raise SyntaxError
        self.frame[symkey(k)] = v

    def set(self, k, v) -> None:
        k = symkey(k)
        e = self
        while e:
            if k in e.frame:
                e.frame[k] = v
                return
            e = e.parent
        raise SyntaxError(f"no such symbol: {k}")

    def get(self, k):
        n = symkey(k)
        e = self
        while e:
            if n in e.frame:
                return e.frame[n]
            e = e.parent
        return k
        # config moment: maybe raise


class Lambda:
    args = ...
    body = ...
    env = ...
    def __init__(self, args, body, env):
        self.args = args
        self.body = body
        self.env = env


class Dambda:
    args = ...
    body = ...
    def __init__(self, args, body):
        self.args = args
        self.body = body


class ourEn(Enum):
    '''to inherit'''


class SF(ourEn): # special form
    QUOTE = 'quote'
    EVAL = 'eval'
    TYPEOF = 'typeof'
    CONS = 'cons'
    CAR = 'car'
    CDR = 'cdr'
    IF = 'if'
    DO = 'do'
    PRINT = 'print'
    READ = 'read'
    SYMBOL = 'symbol'  # stateless calc
    DEF = 'def'
    SET = 'set!'
    LAMBDA = 'lambda'
    DAMBDA = 'dambda'


class BO(ourEn): # binary operation
    ADD = '_+_'
    SUB = '_-_'
    MUL = '_*_'
    DIV = '_/_'
    MOD = '_%_'
    STRCONCAT = '_++_'


class BP(ourEn): # binary predicate
    LT = '_<_'
    GT = '_>_'
    EQ = '_==_'
