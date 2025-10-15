import re
import os
from string import whitespace

from Lists.List_absolute_lambda import car, cdr, cons, isList
from Tokens import ourEn, SF, BO, BP, Symbol


NIL = cons(None, None)


def show(v: tuple) -> str:
    if v is None:
        return ''
    if isList(v):
        s = ''
        first = True
        while v != NIL:
            if first:
                first = False
            else:
                s += ' '
            s += show(car(v))
            v = cdr(v)
        return f'({s})'
    elif isinstance(v, str):
        return f'"{v}"'
    elif isinstance(v, ourEn):
        return v.value
    elif isinstance(v, Symbol):
        return v.name
    elif isinstance(v, bool):
        return 'true' if v else 'false'
    return str(v)


MEANINGFUL = '"();\''
IGNORED = whitespace + ','


def processString(s: str) -> str:
    s = s.lstrip(IGNORED)
    while s and s[0] == ';':  # comments handling
        line_end: int = s.find('\n')
        if line_end < 0:
            return ''
        s = s[line_end:].lstrip(IGNORED)
    return s


def findpref(s: str, breakers: str = IGNORED + MEANINGFUL) -> str:
    pattern = rf'^[^{breakers}]*'
    match = re.match(pattern, s)
    if match:
        return match.group(0)
    return ''


def parse_token(token: str) -> str | ourEn:
    for en in [SF, BO, BP]:
        if token in en:
            return en(token)
    if token == 'true':
        return True
    if token == 'false':
        return False
    try:
        return int(token)
    except ValueError:
        if token == 'inf':
            return Symbol(token)
        try:
            return float(token)
        except ValueError:
            return Symbol(token)


def prs(s: str) -> tuple:  # (ast, remainder of s), ast = None if nothing was parsed
    s = processString(s)
    if not s:
        return (None, s)
    match s[0]:
        case '"':  # string
            matching = s.find('"', 1)
            if matching < 0:
                raise SyntaxError(f'the closing " is missing: {s}')
            return (s[1:matching], s[matching + 1:])
        case '(':  # list
            cache = s  # saving initial view for Error illustration
            s = s[1:]
            arr: list = []
            while s and s[0] != ')':
                elem, s = prs(s)
                arr.append(elem)
                s = processString(s)
            if not s:
                raise SyntaxError(f'the closing ) is missing: {cache}')
            result = NIL
            for elem in reversed(arr):
                result = cons(elem, result)
            return (result, s[1:])
        case ')':
            raise SyntaxError(f'extra closing bracket: {s}')  # TODO debug
        case "'":
            try:
                v, rem = prs(s[1:])
            except Exception as e:
                raise RuntimeError(f'invalid quote: {s}') from e
            if v is None:
                raise SyntaxError(f'quote of nothing: {s}')
            return (cons(SF.QUOTE, cons(v, NIL)), rem)
        case _:  # maybe we can find token
            first = findpref(s)
            return (parse_token(first) if first else None, s[len(first):])


EVAL_NIL = lambda: NIL
repr = lambda v: v if type(v) is str else show(v)


def get_elems(v, n):  # get all elements from list with length n
    ret = []
    while v != NIL and len(ret) < n:
        ret.append(car(v))
        v = cdr(v)
    if v != NIL:
        raise SyntaxError('extra elems')
    if len(ret) < n:
        raise SyntaxError('lack of elems')
    return ret


def binop(op, a, b):  # apply binary operation to 2 args
    match op:
        case BO.ADD:
            return a + b
        case BO.SUB:
            return a - b
        case BO.MUL:
            return a * b
        case BO.DIV:
            if type(a) is type(b) is int:
                return a // b
            return a / b
        case BO.MOD:
            return a % b


def binpred(op, a, b):  # apply binary predicat
    match op:
        case BP.LT:
            return a < b
        case BP.GT:
            return a > b
        case BP.EQ:
            return a == b


def eval_naive(v):
    if isList(v):  # call car with cdr as args
        if v == NIL:
            return EVAL_NIL()
        h = eval_naive(car(v))
        t = cdr(v)
        if isinstance(h, BO):
            if h == BO.STRCONCAT:
                a = car(t)
                if t == NIL:
                    raise SyntaxError
                t = cdr(t)
                b = car(t)
                if t == NIL:
                    return repr(eval_naive(a))
                t = cdr(t)
                if t != NIL:
                    raise SyntaxError
                return repr(eval_naive(a)) + repr(eval_naive(b))
            try:
                a, b = get_elems(t, 2)
                return binop(h, eval_naive(a), eval_naive(b))
            except SyntaxError as e:
                raise SyntaxError(f'wrong args for BO: {show(v)}') from e
        elif isinstance(h, BP):
            try:
                a, b = get_elems(t, 2)
                return binpred(h, eval_naive(a), eval_naive(b))
            except SyntaxError as e:
                raise SyntaxError(f'wrong args for BP: {show(v)}') from e
        elif isinstance(h, SF):
            match h:
                case SF.QUOTE:
                    a = get_elems(t, 1)
                    return a[0]
                case SF.CONS:
                    a, b = get_elems(t, 2)
                    evaluated_b = eval_naive(b)
                    if not isList(evaluated_b):
                        raise SyntaxError
                    return cons(eval_naive(a), evaluated_b)
                case SF.CAR:
                    a = eval_naive(get_elems(t, 1)[0])
                    if not isList(a):
                        return a  # config moment
                    if a == NIL:
                        raise SyntaxError("NIL's head???")  # config moment
                    return car(a)
                case SF.CDR:
                    a = eval_naive(get_elems(t, 1)[0])
                    if not isList(a):
                        return NIL  # config moment
                    if a == NIL:
                        raise SyntaxError("NIL's elems???")  # config moment
                    return cdr(a)
                case _:
                    raise SyntaxError
        else:
            raise SyntaxError('wrong head form')
    return v


def repl():
    pref, suff = '>>> ', 'exiting REPL...'
    strs = [':q :quit :exit exit quit', ':l :load']
    exiters, loaders = map(lambda s: s.split(), strs)
    while True:
        try:
            inp = input(pref).strip()
        except KeyboardInterrupt:
            print(suff)
            break
        except EOFError:  # when started with file input
            print('input exhausted, exiting REPL...')
            break
        if not inp:
            continue
        first = findpref(inp, whitespace)
        if first in exiters:
            print(suff)
            break
        if first in loaders:
            filename = inp[len(first)].strip()
            if not filename:
                print(pref + 'Error: no filename provided.')
                continue
            if not os.path.isfile(filename):
                print(pref + f'Error: no such file "{filename}"')
                continue
            with open(filename, 'r', encoding='utf-8') as f:  # TODO execution
                print(pref + f'Content of {filename}:')
                print(f.read())
                print(pref + f'End of {filename}.')
            continue
        try:
            while inp:  # parse multiple objects on single input line
                res, inp = prs(inp)
                to_print = show(eval_naive(res))
                if to_print:
                    print(to_print)
        except Exception as e:
            while e:  # and e not in seen:
                print(e)
                # print(f"{type(e).__name__}: {e}")
                e = e.__cause__  # if e.__cause__ is not None else e.__context__


repl()
