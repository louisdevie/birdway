import re
from tokens import *


class BirdwayLexicalError(Exception):
    pass


RE_KEYWORD = re.compile(r"\b(args|else|if|meta|param|println|run|then)\b")
RE_NEWLINE = re.compile(r"\n|\r\n")
RE_IGNORE = re.compile(r"\s+")
RE_DOUBLEQUOTES = re.compile(r'"')
RE_PUNCTUATION = re.compile(r";|:|\{|\}|\[|\]")
RE_OPERATOR = re.compile(r"\?")
RE_IDENTIFIER = re.compile(r"[A-Za-z0-9_]+")
RE_VARIABLE = re.compile(r"\$[A-Za-z0-9_]*")
RE_TYPE = re.compile(r"str")


def parse(text):
    result = list()

    parse_body(text, result, 0, 1)

    return result


def parse_body(source, output, cursor, line):
    while cursor < len(source):
        if m := RE_KEYWORD.match(source, cursor):
            match m.group():
                case "args":
                    output.append(KeywordArgs(line))
                case "else":
                    output.append(KeywordElse(line))
                case "if":
                    output.append(KeywordIf(line))
                case "meta":
                    output.append(KeywordMeta(line))
                case "param":
                    output.append(KeywordParam(line))
                case "println":
                    output.append(KeywordPrintln(line))
                case "run":
                    output.append(KeywordRun(line))
                case "then":
                    output.append(KeywordThen(line))
                case other:
                    raise BirdwayLexicalError(f"unknown keyword {other}")
            cursor = m.end()
            continue

        if m := RE_TYPE.match(source, cursor):
            match m.group():
                case "str":
                    output.append(TypeName(line, type=Type.STRING))
                case other:
                    raise BirdwayLexicalError(f"unknown type {other}")
            cursor = m.end()
            continue

        if m := RE_PUNCTUATION.match(source, cursor):
            match m.group():
                case "{":
                    output.append(BlockBegin(line))
                case "}":
                    output.append(BlockEnd(line))
                case "[":
                    output.append(TableBegin(line))
                case "]":
                    output.append(TableEnd(line))
                case ";":
                    output.append(LineEnd(line))
                case ":":
                    output.append(Association(line))
                case other:
                    raise BirdwayLexicalError(f"unknown puctuation mark ‘{other}’")
            cursor = m.end()
            continue

        if m := RE_DOUBLEQUOTES.match(source, cursor):
            output.append(FormattedStringDelimiter(line))
            cursor = parse_formatted_string(source, output, m.end(), line)
            continue

        if m := RE_OPERATOR.match(source, cursor):
            match m.group():
                case "?":
                    output.append(UnaryOperator(line, operator=Unary.ISDEF))
                case other:
                    raise LexicalError(f"unknown operator ‘{other}’")
            cursor = m.end()
            continue

        if m := RE_IDENTIFIER.match(source, cursor):
            output.append(Identifier(line, name=m.group()))
            cursor = m.end()
            continue

        if m := RE_NEWLINE.match(source, cursor):
            line += 1
            cursor = m.end()
            continue

        if m := RE_IGNORE.match(source, cursor):
            cursor = m.end()
            continue

        raise BirdwayLexicalError(
            f"unexpected character ‘{source[cursor]}’ at position {cursor}"
        )


def parse_formatted_string(source, output, cursor, line):
    buffer = str()

    while cursor < len(source):
        if m := RE_DOUBLEQUOTES.match(source, cursor):
            output.append(StringContent(line, value=buffer))
            buffer = str()
            output.append(FormattedStringDelimiter(line))
            return m.end()

        if m := RE_VARIABLE.match(source, cursor):
            output.append(StringContent(line, value=buffer))
            buffer = str()
            output.append(Variable(line, name=m.group()[1:]))
            cursor = m.end()
            continue

        buffer += source[cursor]
        cursor += 1

    raise BirdwayLexicalError(f"hit EOF while parsing string literal")
