import re
from string import whitespace
from Lists.List_absolute_lambda import *

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
    return str(v)


MEANINGFUL = '"();'
IGNORED = whitespace + ','


def processString(s: str) -> str:
    s = s.lstrip(IGNORED)
    while s and s[0] == ';': # comments handling
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


def prs(s: str) -> tuple: #(ast, remainder of s), ast = None if nothing was parsed
    s = processString(s)
    if not s:
        return (None, s)

    match s[0]:
        case '"': # string
            matching = s.find('"', 1)
            if matching < 0:
                raise SyntaxError (f'the closing " is missing: {s}')
            return (s[1:matching], s[matching + 1:])

        case '(': # list
            cache = s # saving initial view for Error illustration
            s = s[1:]
            arr: list = []
            while s and s[0] != ')':
                elem, s = prs(s)
                arr.append(elem)
                s = processString(s)
            if not s:
                raise SyntaxError (f'the closing ) is missing: {cache}')
            result = NIL
            for elem in reversed(arr):
                result = cons(elem, result)
            return (result, s[1:])

        case _: # maybe we can find token
            first = findpref(s) # TODO recognize token
            return (first if first else None, s[len(first):])


def repl():
    pref = '>>> '
    exiters, loaders = map(lambda s: s.split(), [':q :quit :exit', ':l :load'])

    while True:
        try:
            inp = input(pref).strip()
            if not inp:
                continue
            first = findpref(inp, whitespace)

            if first in exiters:
                print(pref + 'exitng REPL...')
                break

            if first in loaders:
                filename = s[len(first)].strip()
                if not filename:
                    print(pref + 'Error: no filename provided.')
                    continue
                if not os.path.isfile(filename):
                    print(pref + f'Error: no such file "{filename}"')
                    continue
                with open(filename, 'r', encoding='utf-8') as f: # TODO execution
                    print(pref + f'Content of {filename}:')
                    print(f.read())
                    print(pref + f'End of {filename}.')
                continue

            while inp: # parse multiple objects on single input line
                res, inp = prs(inp)
                print(show(res))

        except KeyboardInterrupt:
            print('exiting REPL...')
            break
        except EOFError: # when started with file input
            print('input exhausted, exiting REPL...')
            break
        except Exception as e:
            print(f'{e.__class__.__name__}: {e}')


repl()

