import re
from dataclasses import dataclass

from error import BirdwayLexicalError

RE_KEYWORD = re.compile(
    r"\b(const|do|else|enum|flag|for|from|func|if|in|let|limit|meta|option|param|print|println|read|readln|return|struct|then|to|until|while)\b"
)
RE_SPACE = re.compile(r"\s+")
RE_IDENTIFIER = re.compile(r"\b\w+\b")
RE_STRINGDELIMITER = re.compile(r'"')
RE_SYMBOL = re.compile(r"{|;|}|\(|,|\)|\[|\.|]|::|:|->")
RE_OPERATOR = re.compile(r"=")
RE_PRIMITIVE = re.compile(r"\b(Bool|Byte|File|Float|Int|RegEx|Str|Void)\b")


@dataclass
class EndOfFile:
    def __str__(self):
        return "EOF"


@dataclass
class Keyword:
    keyword: str

    def __str__(self):
        return f"keyword ‘{self.keyword}’"


@dataclass
class Identifier:
    name: str

    def __str__(self):
        return f"identifier ‘{self.name}’"


@dataclass
class Symbol:
    symbol: str

    def __str__(self):
        return f"‘{self.symbol}’"


@dataclass
class Operator:
    operator: str

    def __str__(self):
        return f"operator ‘{self.operator}’"


@dataclass
class StringDelitmiter:
    def __str__(self):
        return "double-quotes"


@dataclass
class Text:
    text: str

    def __str__(self):
        return f"text ‘{self.text}’"


@dataclass
class Primitive:
    name: str

    def __str__(self):
        return f"type ‘{self.name}’"


__all__ = [
    "EndOfFile",
    "Keyword",
    "Identifier",
    "Symbol",
    "Operator",
    "StringDelitmiter",
    "Text",
    "Primitive",
]


def tokenise(source):
    context = "main"
    cursor = 0
    buffer = ""

    while cursor < len(source):
        match context:
            case "main":
                if m := RE_SPACE.match(source, cursor):
                    cursor = m.end()
                    continue

                if m := RE_SYMBOL.match(source, cursor):
                    yield Symbol(m.group())
                    cursor = m.end()
                    continue

                if m := RE_OPERATOR.match(source, cursor):
                    yield Operator(m.group())
                    cursor = m.end()
                    continue

                if m := RE_KEYWORD.match(source, cursor):
                    yield Keyword(m.group())
                    cursor = m.end()
                    continue

                if m := RE_PRIMITIVE.match(source, cursor):
                    yield Primitive(m.group())
                    cursor = m.end()
                    continue

                if m := RE_IDENTIFIER.match(source, cursor):
                    yield Identifier(m.group())
                    cursor = m.end()
                    continue

                if m := RE_STRINGDELIMITER.match(source, cursor):
                    yield StringDelitmiter()
                    cursor = m.end()
                    context = "string"
                    continue

                raise BirdwayLexicalError(f"invalid character ‘{source[cursor]}’")

            case "string":
                if m := RE_STRINGDELIMITER.match(source, cursor):
                    yield Text(buffer)
                    buffer = ""
                    yield StringDelitmiter()
                    cursor = m.end()
                    context = "main"
                    continue

                buffer += source[cursor]
                cursor += 1

            case invalid:
                raise ValueError(f"entered invalid context {invalid}")

    yield EndOfFile()
