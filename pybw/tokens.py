from enum import Enum, auto
from autorepr import AutoRepr
from birdway import Unary, Type, Binary


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


for name in [
    "KeywordMeta",
    "KeywordArgs",
    "KeywordParam",
    "KeywordRun",
    "KeywordIf",
    "KeywordThen",
    "KeywordElse",
    "KeywordPrintln",
    "KeywordOption",
    "BlockBegin",
    "BlockEnd",
    "TableBegin",
    "TableEnd",
    "OpeningParens",
    "ClosingParens",
    "FormattedStringDelimiter",
    "StringDelimiter",
    "LineEnd",
    "Association",
    "Separator",
    "Assignment",
    "Return",
    "FormattingExpressionBegin",
    "KeywordStruct",
    "KeywordEnum",
    "KeywordFunc",
    "KeywordFor",
    "KeywordFrom",
    "KeywordTo",
    "KeywordDo",
    "KeywordTry",
    "KeywordOn",
    "Range",
    "KeywordUse",
    "KeywordIn",
]:
    exec(f"class {name} (Token, AutoRepr): pass")
del name


class StringContent(Token, AutoRepr):
    value = str()


class Identifier(Token, AutoRepr):
    name = str()


class Integer(Token, AutoRepr):
    value = int()


class UnaryOperator(Token, AutoRepr):
    operator = Unary(1)


class BinaryOperator(Token, AutoRepr):
    operator = Binary(1)


class Variable(Token, AutoRepr):
    name = str()


class TypeName(Token, AutoRepr):
    type = Type(1)
