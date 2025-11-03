class LispError(Exception):
    pass


class LispSyntaxError(LispError):
    pass


class LispRuntimeError(LispError):
    pass


class LispValueError(LispError):
    pass


class LispTypeError(LispError):
    pass
