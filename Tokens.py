from enum import Enum


class Symbol:
    _name: str = ...
    def __init__(self, name):
        self._name = name
    @property
    def name(self):
        return self._name


class Env:
    frame: dict = ...

    def __init__(self):
        self.frame = dict()

    def add(self, k: Symbol, v) -> None:
        # if k in dict.keys():  # config moment: immutible
        #     raise SyntaxError
        self.frame[k.name] = v
    
    def set(self, k: Symbol, v) -> None:
        self.frame[k.name] = v

    def get(self, k: Symbol):
        # config moment: what if not k?
        return self.frame[k.name] if k.name in self.frame.keys() else k


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
