import re
from tokens import *
from exceptions import BirdwayLexicalError


RE_KEYWORD = re.compile(r"\b(args|do|else|enum|for|from|func|if|meta|on|option|param|println|run|struct|then|to|try)\b")
RE_NEWLINE = re.compile(r"\n|\r\n")
RE_IGNORE = re.compile(r"\s+")
RE_DOUBLEQUOTES = re.compile(r'"')
RE_SINGLEQUOTE = re.compile(r"'")
RE_PUNCTUATION = re.compile(r";|:|\{|\}|\[|\]|,|\(|\)")
RE_OPERATOR = re.compile(r"\?|!|\*|##|#|-|\+")
RE_IDENTIFIER = re.compile(r"[A-Za-z0-9_]+")
RE_VARIABLE = re.compile(r"(\$)([A-Za-z0-9_]*)")
RE_FORMATEXPRESSION = re.compile(r"\$\(")
RE_TYPE = re.compile(r"\bstr\b")
RE_ASSIGNMENT = re.compile(r"=")
RE_RETURN = re.compile(r"->")
RE_LINECOMMENT = re.compile(r"/:.*(\n|\r\n)")


class Counter:
    def __init__(self, initial_value=0):
        self._val = initial_value

    def inc(self):
        self._val += 1

    def __str__(self):
        return self._val.__str__()

    def __repr__(self):
        return self._val.__repr__()

    def __int__(self):
        return self._val

def parse(text):
    result = list()

    parse_body(text, result, 0, Counter(1))

    return result


def parse_body(source, output, cursor, line):
    while cursor < len(source):
        if m := RE_LINECOMMENT.match(source, cursor):
            cursor = m.end()
            continue

        if m := RE_KEYWORD.match(source, cursor):
            match m.group():
                case "args":
                    output.append(KeywordArgs(int(line)))
                case "else":
                    output.append(KeywordElse(int(line)))
                case "if":
                    output.append(KeywordIf(int(line)))
                case "meta":
                    output.append(KeywordMeta(int(line)))
                case "option":
                    output.append(KeywordOption(int(line)))
                case "param":
                    output.append(KeywordParam(int(line)))
                case "println":
                    output.append(KeywordPrintln(int(line)))
                case "run":
                    output.append(KeywordRun(int(line)))
                case "then":
                    output.append(KeywordThen(int(line)))
                case "struct":
                    output.append(KeywordStruct(int(line)))
                case "enum":
                    output.append(KeywordEnum(int(line)))
                case "func":
                    output.append(KeywordFunc(int(line)))
                case "for":
                    output.append(KeywordFor(int(line)))
                case "from":
                    output.append(KeywordFrom(int(line)))
                case "to":
                    output.append(KeywordTo(int(line)))
                case "do":
                    output.append(KeywordDo(int(line)))
                case "try":
                    output.append(KeywordTry(int(line)))
                case "on":
                    output.append(KeywordOn(int(line)))
                case other:
                    raise BirdwayLexicalError(f"unknown keyword {other}")
            cursor = m.end()
            continue

        if m := RE_TYPE.match(source, cursor):
            match m.group():
                case "str":
                    output.append(TypeName(int(line), type=Type.STRING))
                case other:
                    raise BirdwayLexicalError(f"unknown type {other}")
            cursor = m.end()
            continue

        if m := RE_PUNCTUATION.match(source, cursor):
            match m.group():
                case "{":
                    output.append(BlockBegin(int(line)))
                case "}":
                    output.append(BlockEnd(int(line)))
                case "[":
                    output.append(TableBegin(int(line)))
                case "]":
                    output.append(TableEnd(int(line)))
                case ";":
                    output.append(LineEnd(int(line)))
                case ":":
                    output.append(Association(int(line)))
                case ",":
                    output.append(Separator(int(line)))
                case "(":
                    output.append(OpeningParens(int(line)))
                    cursor = parse_body(source, output, m.end(), line)
                    continue
                case ")":
                    output.append(ClosingParens(int(line)))
                    return m.end()
                case other:
                    raise BirdwayLexicalError(f"unknown puctuation mark ‘{other}’")
            cursor = m.end()
            continue

        if m := RE_DOUBLEQUOTES.match(source, cursor):
            output.append(FormattedStringDelimiter(int(line)))
            cursor = parse_formatted_string(source, output, m.end(), int(line))
            continue

        if m := RE_SINGLEQUOTE.match(source, cursor):
            output.append(StringDelimiter(int(line)))
            cursor = parse_string(source, output, m.end(), int(line))
            continue

        if m := RE_RETURN.match(source, cursor):
            output.append(Return(int(line)))
            cursor = m.end()
            continue

        if m := RE_OPERATOR.match(source, cursor):
            match m.group():
                case "?":
                    output.append(UnaryOperator(int(line), operator=Unary.ISDEF))
                case "!":
                    output.append(UnaryOperator(int(line), operator=Unary.ISNTDEF))
                case "#":
                    output.append(UnaryOperator(int(line), operator=Unary.LAST))
                case "##":
                    output.append(UnaryOperator(int(line), operator=Unary.SIZE))
                case "*":
                    output.append(BinaryOperator(int(line), operator=Binary.MULTIPLICATION))
                case "-":
                    output.append(BinaryOperator(int(line), operator=Binary.SUBSTRACTION))
                case "+":
                    output.append(BinaryOperator(int(line), operator=Binary.ADDITION))
                case other:
                    raise BirdwayLexicalError(f"unknown operator ‘{other}’")
            cursor = m.end()
            continue

        if m := RE_ASSIGNMENT.match(source, cursor):
            output.append(Assignment(int(line)))
            cursor = m.end()
            continue

        if m := RE_IDENTIFIER.match(source, cursor):
            output.append(Identifier(int(line), name=m.group()))
            cursor = m.end()
            continue

        if m := RE_NEWLINE.match(source, cursor):
            line.inc()
            cursor = m.end()
            continue

        if m := RE_IGNORE.match(source, cursor):
            cursor = m.end()
            continue

        raise BirdwayLexicalError(
            f"unexpected character ‘{source[cursor]}’ at line {line}"
        )


def parse_formatted_string(source, output, cursor, line):
    buffer = str()

    while cursor < len(source):
        if m := RE_DOUBLEQUOTES.match(source, cursor):
            output.append(StringContent(int(line), value=buffer))
            buffer = str()
            output.append(FormattedStringDelimiter(int(line)))
            return m.end()

        if m := RE_FORMATEXPRESSION.match(source, cursor):
            output.append(StringContent(int(line), value=buffer))
            buffer = str()
            output.append(FormattingExpressionBegin(int(line)))
            cursor = parse_body(source, output, m.end(), line)

        if m := RE_VARIABLE.match(source, cursor):
            if m.group(2) == "":
                raise BirdwayLexicalError(f"missing variable name after ‘$’ at line {line}")
            output.append(StringContent(int(line), value=buffer))
            buffer = str()
            output.append(Variable(int(line), name=m.group(2)))
            cursor = m.end()
            continue

        buffer += source[cursor]
        cursor += 1

    raise BirdwayLexicalError(f"hit EOF while parsing string literal")


def parse_string(source, output, cursor, line):
    buffer = str()

    while cursor < len(source):
        if m := RE_SINGLEQUOTE.match(source, cursor):
            output.append(StringContent(int(line), value=buffer))
            buffer = str()
            output.append(StringDelimiter(int(line)))
            return m.end()

        buffer += source[cursor]
        cursor += 1

    raise BirdwayLexicalError(f"hit EOF while parsing string literal")
