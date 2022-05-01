from .base import *
from birdway import Type, ArgumentModifier, Composite


class Option(SyntaxNodeABC, PrettyAutoRepr, Identified):
    def __init__(self):
        self.type = Type.UNKNOWN
        self.modifier = ArgumentModifier.NONE
        self.name = str()
        self.shortcut = str()
        self.description = str()

    @classmethod
    def _parse(cls, parser):
        option = cls()

        if parser.peek(0) == UnaryOperator(operator=Unary.ISDEF):
            raise BirdwaySyntaxError(
                "The optional modifier ‘?’ can't be used on options"
            )
        elif parser.peek(0) == UnaryOperator(operator=Unary.ISNTDEF):
            parser.eat()
            option.modifier = ArgumentModifier.UNIQUE
        elif parser.peek(0) == BinaryOperator(operator=Binary.MULTIPLICATION):
            raise BirdwaySyntaxError(
                "The multiple modifier ‘*’ can't be used on options"
            )

        match parser.peek(0):
            case TypeName(type=t):
                parser.eat()
                option.type = t

            case other:
                raise BirdwaySyntaxError(
                    f"""expected type{
                        ' or modifier' if option.modifier == ArgumentModifier.NONE else ''
                    }, got {other} at line {other._line}"""
                )

        match parser.peek(0):
            case Identifier(name=ident):
                parser.eat()
                option.name = ident

            case other:
                raise BirdwaySyntaxError(
                    f"expected identifier, got {other} at line {other._line}"
                )

        match parser.peek(0):
            case Identifier(name=ident):
                parser.eat()
                option.shortcut = ident

        if parser.peek(0) == FormattedStringDelimiter():
            parser.eat()
            option.description = parser.parse_formatted_string()
        elif parser.peek(0) == StringDelimiter():
            parser.eat()
            option.description = parser.parse_string()

        return option

    def _initialise(self):
        if self.modifier == ArgumentModifier.OPTIONAL:
            T = Composite.Nullable(self.type)
            init = "= NULL"
        else:
            raise NotImplementedError()
        return f"{ctype(T)} {self.id} {init};\n"
