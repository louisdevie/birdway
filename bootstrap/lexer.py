import re
from dataclasses import dataclass, field

from error import BirdwayLexicalError

RE_KEYWORD = re.compile(
    r"\b(break|const|do|else|enum|finally|flag|for|from|func|if|in|let|limit|meta|option|on|param|print|println|read|readln|return|struct|then|throw|to|try|until|use|while)\b"
)
RE_SPACE = re.compile(r"\s+")
RE_LINE_COMMENT = re.compile(r"--.*\n")
RE_IDENTIFIER = re.compile(r"\b\w+\b")
RE_STRINGDELIMITER = re.compile(r'"')
RE_PUNCTUATION = re.compile(r"{|;|}|\(|,|\)|\[|\.|]|::|:|->|\$")
RE_OPERATOR = re.compile(
    r"~|#|\?|!|\bnot\b|-|&&|&|\||\^|\+|==|=|%|\*\*|\*|<=|<<|<|>=|>>|>|//|/|!=|\band\b|\bor\b|\bxor\b|<=|<"
)
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
class Punctuation:
    symbol: str

    def __str__(self):
        return f"‘{self.symbol}’"


ARITY = {"==": "binary", "=": "binary", "?": "unary", "#": "unary"}


@dataclass
class Operator:
    operator: str
    arity: str = field(init=False)

    def __post_init__(self):
        self.arity = ARITY[self.operator]

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
    "tokenise",
    "EndOfFile",
    "Keyword",
    "Identifier",
    "Punctuation",
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

                if m := RE_LINE_COMMENT.match(source, cursor):
                    cursor = m.end()
                    continue

                if m := RE_PUNCTUATION.match(source, cursor):
                    yield Punctuation(m.group())
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
