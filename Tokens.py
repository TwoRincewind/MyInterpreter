from enum import Enum


class Symbol:
    _name: str = ...
    def __init__(self, name):
        self._name = name
    @property
    def name(self):
        return self._name


class ourEn(Enum):
    '''to inherit'''


class SF(ourEn): # special form
    QUOTE = 'quote'
    CONS = 'cons'
    CAR = 'car'
    CDR = 'cdr'
    DEF = 'def'
    IF = 'if'


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

