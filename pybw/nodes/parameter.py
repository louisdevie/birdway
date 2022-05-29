from .base import *
from birdway import Type, ArgumentModifier, Composite

from .string_literal import StringLiteral


class Parameter(SyntaxNodeABC, PrettyAutoRepr, Identified):
    def __init__(self):
        super().__init__()
        self.type = Type.UNKNOWN
        self.modifier = ArgumentModifier.NONE
        self.name = str()
        self.description = str()

    @classmethod
    def _parse(cls, parser):
        parameter = cls()

        if parser.peek(0) == UnaryOperator(operator=Unary.ISDEF):
            parser.eat()
            parameter.modifier = ArgumentModifier.OPTIONAL
        elif parser.peek(0) == UnaryOperator(operator=Unary.ISNTDEF):
            raise BirdwaySyntaxError(
                "The unique modifier ‘!’ can't be used on parameters"
            )
        elif parser.peek(0) == BinaryOperator(operator=Binary.MULTIPLICATION):
            parser.eat()
            parameter.modifier = ArgumentModifier.MULTIPLE

        match parser.peek(0):
            case TypeName(type=t):
                parser.eat()
                parameter.type = t

            case other:
                raise BirdwaySyntaxError(
                    f"""expected type{
                        ' or modifier' if parameter.modifier == ArgumentModifier.NONE else ''
                    }, got {other} at line {other._line}"""
                )

        match parser.peek(0):
            case Identifier(name=ident):
                parser.eat()
                parameter.name = ident

            case other:
                raise BirdwaySyntaxError(
                    f"expected identifier, got {other} at line {other._line}"
                )

        if parser.peek(0) == FormattedStringDelimiter():
            parser.eat()
            parameter.description = parser.parse_formatted_string()
        elif parser.peek(0) == StringDelimiter():
            parser.eat()
            parameter.description = StringLiteral._parse(parser)

        return parameter

    def _initialise(self):
        if self.modifier == ArgumentModifier.OPTIONAL:
            T = Composite.Nullable(self.type)
            init = " = NULL"
        elif self.modifier == ArgumentModifier.MULTIPLE:
            T = Composite.Table(val=self.type)
            init = ""
        else:
            T = self.type
            init = ""
        return f"{ctype(T)} {self.id}{init};\n"
