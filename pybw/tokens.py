from enum import Enum, auto
from autorepr import AutoRepr
from birdway import Unary, Type


class Token:
    def __init__(self, line=None, **attributes):
        self._line = line
        for attr in dir(self):
            if not attr.startswith("_"):
                if attr in attributes:
                    setattr(self, attr, attributes[attr])
                else:
                    raise TypeError(f"no value specified for {attr}")

    def __eq__(self, other):
        if type(self) is type(other):
            for attr in dir(self):
                if not attr.startswith("_"):
                    if getattr(self, attr) != getattr(other, attr):
                        return False
            return True
        else:
            return False


class KeywordMeta(Token, AutoRepr):
    pass


class KeywordArgs(Token, AutoRepr):
    pass


class KeywordParam(Token, AutoRepr):
    pass


class KeywordRun(Token, AutoRepr):
    pass


class KeywordIf(Token, AutoRepr):
    pass


class KeywordThen(Token, AutoRepr):
    pass


class KeywordElse(Token, AutoRepr):
    pass


class KeywordPrintln(Token, AutoRepr):
    pass


class BlockBegin(Token, AutoRepr):
    pass


class BlockEnd(Token, AutoRepr):
    pass


class TableBegin(Token, AutoRepr):
    pass


class TableEnd(Token, AutoRepr):
    pass


class FormattedStringDelimiter(Token, AutoRepr):
    pass


class StringContent(Token, AutoRepr):
    value = str()


class LineEnd(Token, AutoRepr):
    pass


class Association(Token, AutoRepr):
    pass


class Identifier(Token, AutoRepr):
    name = str()


class UnaryOperator(Token, AutoRepr):
    operator = Unary(1)


class Variable(Token, AutoRepr):
    name = str()


class TypeName(Token, AutoRepr):
    type = Type
