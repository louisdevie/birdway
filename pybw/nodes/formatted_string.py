from .base import *
from birdway import Type, FEATURE_STRING, FEATURE_FORMATTING
from .string_literal import StringLiteral


def formatter(node, tui):
    if node.type == Type.STRING:
        return ""

    else:
        return f"""
            struct BirdwayString {tui}F;
            err = birdwayFormat{nameof(node.type)}({node._reference(tui+"1")}, &{tui}F);
            if (err) return err;\n"""


def nameof(T):
    match T:
        case Type.STRING:
            return "String"

        case Composite.Nullable(val=val):
            return "Nullable" + nameof(val)

        case other:
            raise TypeError(f"no type name for <{other}>")


class FormattedString(SyntaxNodeABC, PrettyAutoRepr, Typed, InContext):
    def __init__(self):
        super().__init__()
        self.content = list()

    @classmethod
    def _parse(cls, parser):
        string = cls()

        while parser.remaining():
            match parser.peek(0):
                case FormattedStringDelimiter():
                    parser.eat()
                    return string

                case StringContent(value=val):
                    parser.eat()
                    literal = StringLiteral()
                    literal.string = val
                    string.content.append(literal)

                case Variable(name=var):
                    parser.eat()
                    formatting = ReadVariable()
                    formatting.name = var
                    string.content.append(formatting)

                case FormattingExpressionBegin():
                    parser.eat()
                    formatting = parser.parse_expression()
                    string.content.append(formatting)
                    if (invalid := parser.pop()) != ClosingParens():
                        raise BirdwaySyntaxError(
                                f"expected closing penthesis, got {invalid} at line {invalid._line}"
                            )

                case other:
                    raise BirdwaySyntaxError(
                        f"unexpected {other} at line {other._line} while parsing string"
                    )

        raise BirdwaySyntaxError("hit EOF while parsing string")

    def _type(self):
        return Type.STRING

    def _propagate(self, ast, vc, lc, bc):
        ast.standard_features |= FEATURE_STRING
        for child in self.content:
            if not isinstance(child, str):
                ast.standard_features |= FEATURE_FORMATTING
                child.context = self.context.copy()
                self.using |= child._propagate(ast, vc, lc, bc)
        return self.using

    def _check(self):
        for child in self.content:
            child._check()

    def _initialise(self):
        return "\n".join([lit._initialise() for lit in self.content])

    def _transpile(self, tui):
        return f"""
            struct BirdwayString {tui};
            birdwayStringEmpty(&{tui});
            {
                "".join([
                    (
                        f"birdwayStringAppendLiteral(&{tui}, {n.id}, {len(n.string)});"
                        if isinstance(n, StringLiteral)
                        else f"birdwayStringConcat(&{tui}, {n._reference()})"
                    )
                    if n.type == Type.STRING
                    else (
                        n._transpile(tui+str(i))
                        + formatter(n, tui+str(i))
                        + f"birdwayStringConcat(&{tui}, &{tui}{i}F);"
                    )
                    for i, n in enumerate(self.content)
                ])
            }"""
