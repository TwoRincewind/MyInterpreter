import re, os, sys
from string import whitespace

from Lists.List_absolute_lambda import car, cdr, cons, isList
from Symbols.Symbol_string import symbol, symname, isSymbol
from Tokens import ourEn, SF, BO, BP, Env, Lambda, Dambda, Macro


NIL = cons(None, None)
ENV = Env(None)


def show(obj) -> str:
    '''
    return showable string representation of obj
    how it could be passed to our parser
    '''
    if obj is None:
        obj = NIL
        # return ''
    if isList(obj):
        s = ''
        first = True
        while obj != NIL:
            if first:
                first = False
            else:
                s += ' '
            s += show(car(obj))
            obj = cdr(obj)
        return f'({s})'
    elif isSymbol(obj):
        return symname(obj)
    elif isinstance(obj, str):
        return f'"{obj}"'
    elif isinstance(obj, ourEn):
        return obj.value
    elif isinstance(obj, bool):
        return 'true' if obj else 'false'
    elif isinstance(obj, Lambda):
        return f'({show(SF.LAMBDA)} {show(obj.args)} {show(obj.body)})'
    elif isinstance(obj, Dambda):
        return f'({show(SF.DAMBDA)} {show(obj.args)} {show(obj.body)})'
    elif isinstance(obj, Macro):
        return f'({show(SF.MACRO)} {show(obj.args)} {show(obj.body)})'
    return str(obj)


MEANINGFUL = '"();\''
IGNORED = whitespace + ','


def processString(s: str) -> str:
    '''
    remove all the blank characters, comments
    '''
    s = s.lstrip(IGNORED)
    while s and s[0] == ';':  # comments handling
        line_end: int = s.find('\n')
        if line_end < 0:
            return ''
        s = s[line_end:].lstrip(IGNORED)
    return s


def findpref(s: str, separators: str = IGNORED + MEANINGFUL) -> str:
    '''
    find meaningful prefix
    '''
    pattern = rf'^[^{separators}]*'
    match = re.match(pattern, s)
    if match:
        return match.group(0)
    return ''


def parse_token(token: str):
    '''
    tryes to recognize given token
    '''
    for en in [SF, BO, BP]:
        if token in en:
            return en(token)
    if token in ['true', 'false']:
        return token == 'true'
    try:
        return int(token)
    except ValueError:
        if token == 'inf':
            return symbol(token)
        try:
            return float(token)
        except ValueError:
            return symbol(token)

# string -> ast, remainder of string
def prs(s: str) -> tuple:
    '''
    parses one token
    '''
    s = processString(s)
    if not s:
        return (NIL, s)
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
            return (parse_token(first) if first else NIL, s[len(first):])


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
        case BO.STRCONCAT:
            return repr(a) + repr(b)


def binpred(op, a, b):  # apply binary predicat
    match op:
        case BP.LT:
            return a < b
        case BP.GT:
            return a > b
        case BP.EQ:
            return a == b


def eval_naive(v, e):
    if isSymbol(v):
        return e.get(v)
    elif isList(v):  # call car with cdr as args
        if v == NIL:
            return EVAL_NIL()
        h = eval_naive(car(v), e)
        t = cdr(v)
        if isinstance(h, BO):
            try:
                a, b = get_elems(t, 2)
                return binop(h, eval_naive(a, e), eval_naive(b, e))
            except SyntaxError as e:
                raise SyntaxError(f'wrong args for BO: {show(v)}') from e
        elif isinstance(h, BP):
            try:
                a, b = get_elems(t, 2)
                return binpred(h, eval_naive(a, e), eval_naive(b, e))
            except SyntaxError as e:
                raise SyntaxError(f'wrong args for BP: {show(v)}') from e
        elif isinstance(h, SF):
            match h:
                case SF.QUOTE:
                    return get_elems(t, 1)[0]
                case SF.EVAL:
                    return eval_naive(eval_naive(get_elems(t, 1)[0], e), e)
                case SF.TYPEOF:
                    a = eval_naive(get_elems(t, 1)[0], e)
                    return 'List' if isList(a) else str(a.__class__.__name__)
                case SF.CONS:
                    a, b = get_elems(t, 2)
                    evaluated_b = eval_naive(b, e)
                    if not isList(evaluated_b):
                        raise SyntaxError
                    return cons(eval_naive(a, e), evaluated_b)
                case SF.CAR:
                    a = eval_naive(get_elems(t, 1)[0], e)
                    if not isList(a):
                        return a  # config moment
                    if a == NIL:
                        raise SyntaxError("NIL's head???")  # config moment
                    return car(a)
                case SF.CDR:
                    a = eval_naive(get_elems(t, 1)[0], e)
                    if not isList(a):
                        return NIL  # config moment
                    if a == NIL:
                        raise SyntaxError("NIL's elems???")  # config moment
                    return cdr(a)
                case SF.IF:
                    a, b, c = get_elems(t, 3)  # a ? b : c
                    evaled_a = eval_naive(a, e)
                    if type(evaled_a) is bool:
                        return eval_naive(b, e) if evaled_a else eval_naive(c, e)
                    raise SyntaxError(f'not boolean {a} in {show(v)}')  # TODO
                case SF.DO:
                    ev = NIL
                    while not t == NIL:
                        ev = eval_naive(car(t), e)
                        t = cdr(t)
                    return ev
                case SF.PRINT:
                    a = eval_naive(get_elems(t, 1)[0], e)
                    print(repr(a), end='')
                    return NIL
                case SF.READ:
                    get_elems(t, 0)
                    s = input('\nreading: ')
                    return prs(s)[0]
                case SF.SYMBOL:
                    a = eval_naive(get_elems(t, 1)[0], e)
                    if not isinstance(a, str):
                        raise SyntaxError('symbol not from string')
                    return symbol(a)
                case SF.DEF:
                    a, b = get_elems(t, 2)
                    if isSymbol(a):
                        e.add(a, eval_naive(b, e))
                        return NIL
                    raise SyntaxError('cannot define non-symbol')
                case SF.SET:
                    a, b = get_elems(t, 2)
                    if isSymbol(a):
                        e.set(a, eval_naive(b, e))
                        return NIL
                    raise SyntaxError('cannot set non-Symbol')
                case SF.LAMBDA:
                    a, b = get_elems(t, 2)
                    if isList(a):
                        return Lambda(a, b, e)
                    raise SyntaxError(f'wrong args form for lambda: {show(a)}')
                case SF.DAMBDA:
                    a, b = get_elems(t, 2)
                    if isList(a):
                        return Dambda(a, b)
                    raise SyntaxError(f'wrong args form for dambda: {show(a)}')
                case SF.MACRO:
                    a, b = get_elems(t, 2)
                    if isList(a):
                        return Macro(a, b)
                    raise SyntaxError(f'wrong args form for macro: {show(a)}')
                case _:
                    raise SyntaxError
        elif isinstance(h, Lambda):
            lambda_e = Env(h.env)
            a = h.args
            if a == NIL and t != NIL:
                raise SyntaxError("more than zero args for lambda")
            while a != NIL and t != NIL:
                arg = t if cdr(a) == NIL and cdr(t) != NIL else eval_naive(car(t), e)
                lambda_e.add(car(a), arg)
                a = cdr(a)
                t = cdr(t)
            if a != NIL:
                return Lambda(a, h.body, lambda_e)
            return eval_naive(h.body, lambda_e)
        elif isinstance(h, Dambda):
            dambda_e = Env(e)
            a = h.args
            if a == NIL and t != NIL:
                raise SyntaxError("more than zero args for dambda")
            while a != NIL and t != NIL:
                arg = t if cdr(a) == NIL and cdr(t) != NIL else eval_naive(car(t), e)
                dambda_e.add(car(a), arg)
                a = cdr(a)
                t = cdr(t)
            if a != NIL:
                return Lambda(a, h.body, dambda_e)
            return eval_naive(h.body, dambda_e)
        elif isinstance(h, Macro):
            d = dict()
            a = h.args
            if a == NIL and t != NIL:
                raise SyntaxError("more than zero args for macro")
            while a != NIL and t != NIL:
                d[car(a)] = car(t)
                a = cdr(a)
                t = cdr(t)
            expanded = macro_expand(h.body, d)
            print(show(expanded), file=sys.stderr)
            return eval_naive(expanded, e)
        else:
            raise SyntaxError(f'wrong head form: {show(h)}')
    return v


def macro_expand(body, d):
    if isSymbol(body):
        if body in d:
            return d[body]  # autoquote
        return body
    if isList(body):
        if body == NIL:
            return NIL
        return cons(macro_expand(car(body), d), macro_expand(cdr(body), d))
    return body


def repl():
    def eval_local(s, load=False):
        try:
            res = ''
            while s:  # parse every object
                res, s = prs(s)
                res = eval_naive(res, ENV)
                # to_print = show(eval_naive(res, ENV))
                # if not load:  # and to_print:
                #     print(to_print)
            return res
        except SyntaxError as e:
            while e:
                print(e)
                e = e.__cause__
                # \ if e.__cause__ is not None else e.__context__

    pref, suff = '>>> ', 'exiting REPL...'
    strs = [':q :quit :exit exit quit', ':l :load']
    exiters, loaders = map(lambda s: s.split(), strs)
    prev, inp = '', ''
    if not sys.stdin.isatty():
        eval_local(sys.stdin.read(), load=True)
        # print(show())
        print('\ninput exhausted,', suff)
        return
    while True:
        prev = inp
        try:
            inp = input(pref).strip()
        except KeyboardInterrupt:
            print(suff)
            break
        if not inp:
            continue
        first = findpref(inp, whitespace)
        if first == ':':
            inp = prev
            first = findpref(inp, whitespace)
        if first in exiters:
            print(suff)
            break
        if first in loaders:
            filename = inp[len(first):].strip()
            if not filename:
                print(pref + 'Error: no filename provided.')
                continue
            if not os.path.isfile(filename):
                print(pref + f'Error: no such file "{filename}"')
                continue
            with open(filename, 'r', encoding='utf-8') as f:
                eval_local(f.read(), load=True)
                print()
            continue
        print(show(eval_local(inp)))


repl()
