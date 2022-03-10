from autorepr import AutoRepr, PrettyAutoRepr
from tokens import *
from birdway import Type, Composite
from exceptions import *
from enum import Enum, auto

class ArgumentModifier(Enum):
    NONE = auto()
    UNIQUE = auto()
    OPTIONAL = auto()
    VARIADIC = auto()

class SyntaxNodeABC:
    pass

class Program(SyntaxNodeABC, PrettyAutoRepr):
     def __init__(self):
        self.metadata = None
        self.arguments = None
        self.script = None

class Typed:
    def __getattr__(self, attr):
        if attr == 'type':
            return self._type()
        else:
            return super().__getattr__(attr)

    def _type(self):
        raise NotImplementedError()


class Table(SyntaxNodeABC, PrettyAutoRepr, Typed):
    def __init__(self):
        self.key_type = Type.UNKNOWN
        self.value_type = Type.UNKNOWN
        self.values = dict()
        
    def _type(self):
    	return Composite.Table(self.value_type, self.key_type)


class FormattedString(SyntaxNodeABC, PrettyAutoRepr, Typed):
    def __init__(self):
        self.content = list()

    def _type(self):
        return Type.STRING


class Block(SyntaxNodeABC, PrettyAutoRepr, Typed):
    def __init__(self):
        self.statements = list()


class Parameter(SyntaxNodeABC, PrettyAutoRepr):
    def __init__(self):
        self.type = Type.UNKNOWN
        self.modifier = ArgumentModifier.NONE
        self.name = str()
        self.description = str()
        
class IfThenElse(SyntaxNodeABC, PrettyAutoRepr, Typed):
    def __init__(self):
        self.condition = None
        self.statements = None
        self.alternative = None
        
    def _type(self):
    	return self.statements.type
        
class UnaryOperation(SyntaxNodeABC, PrettyAutoRepr, Typed):
    def __init__(self):
        self.operator = None
        self.operand = None
        
    def _type(self):
    	return OPERATION_RESULT[self.operator][self.operand]
        
class ReadVariable(SyntaxNodeABC, PrettyAutoRepr, Typed):
    def __init__(self):
        self.name = str()
        
class PrintLine(SyntaxNodeABC, PrettyAutoRepr, Typed):
    def __init__(self):
        self.content = None
        
def parse(tokens):
    parser = Parser(tokens)
    return parser.parse_program()


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens

    def peek(self, pos):
        return self.tokens[0]

    def eat(self, howmany=1):
        for _ in range(howmany):
            self.tokens.pop(0)
            
    def pop(self):
        return self.tokens.pop(0)

    def remaining(self):
        return len(self.tokens) > 0

    def parse_program(self):
        prog = Program()

        while self.remaining():
            match self.peek(0):
                case KeywordMeta():
                    self.eat()
                    prog.metadata = self.parse_expression()
                    if self.peek(0) != LineEnd():
                        raise BirdwaySyntaxError(
                            f"missing semicolon on line {self.peek(0)._line}"
                        )
                    self.eat()

                case KeywordArgs():
                    self.eat()
                    if self.peek(0) != BlockBegin():
                        raise BirdwaySyntaxError(
                            f"expected block on line {self.peek(0)._line}"
                        )
                    self.eat()
                    prog.arguments = self.parse_arguments_block()
                    if self.peek(0) != LineEnd():
                        raise BirdwaySyntaxError(
                            f"missing semicolon on line {self.peek(0)._line}"
                        )
                    self.eat()
                    
                case KeywordRun():
                    self.eat()
                    if self.peek(0) != BlockBegin():
                        raise BirdwaySyntaxError(
                            f"expected block on line {self.peek(0)._line}"
                        )
                    self.eat()
                    prog.script = self.parse_block()
                    if self.peek(0) != LineEnd():
                        raise BirdwaySyntaxError(
                            f"missing semicolon on line {self.peek(0)._line}"
                        )
                    self.eat()

                case other:
                    raise BirdwaySyntaxError(
                        f"unexpected {other} at line {other._line} while parsing program body"
                    )

        return prog

    def parse_expression(self):
        match self.peek(0):
            case TableBegin():
                self.eat()
                lhs = self.parse_table()

            case FormattedStringDelimiter():
                self.eat()
                lhs = self.parse_formatted_string()
            
            case KeywordIf():
                self.eat()
                lhs = self.parse_if()
            
            case KeywordPrintln():
                self.eat()
                lhs = self.parse_println()
            
            case Identifier(name=var):
                self.eat()
                lhs = ReadVariable()
                lhs.name = var
                
            case BlockBegin():
                self.eat()
                lhs = self.parse_block()
            
            case UnaryOperator(operator=op):
                self.eat()
                operation = UnaryOperation()
                operation.operator = op
                operation.operand = self.parse_expression()
                return operation
                
            case other:
                raise BirdwaySyntaxError(f"unexpected {other} at line {other._line} while parsing expression")

        return lhs

    def parse_table(self):
        table = Table()

        while self.remaining():
            val_or_key = self.parse_expression()

            if self.peek(0) == Association():
                self.eat()
                val = self.parse_expression()

                if table.key_type == Type.UNKNOWN:
                    table.key_type = val_or_key.type
                else:
                    if val_or_key.type != table.key_type:
                        raise BirdwayTypeError(
                            f"inconsistent table keys types (expected {table.key_type}, found {val_or_key.type}) around {self.peek(0)._line}"
                        )

                if table.value_type == Type.UNKNOWN:
                    table.value_type = val.type
                else:
                    if val.type != table.value_type:
                        raise BirdwayTypeError(
                            f"inconsistent table values types (expected {table.value_type}, found {val.type}) around {self.peek(0)._line}"
                        )

                table.values[val_or_key] = val

            else:
                if table.key_type == Type.UNKNOWN:
                    table.key_type = val_or_key.type
                else:
                    if val_or_key.type != table.key_type:
                        raise BirdwayTypeError(
                            f"missing table keys around {self.peek(0)._line}"
                        )

                if table.value_type == Type.UNKNOWN:
                    table.value_type = val.type
                else:
                    if val.type != table.value_type:
                        raise BirdwayTypeError(
                            f"inconsistent table values types (expected {table.value_type}, found {val.type})"
                        )

                table.values[val_or_key] = val

            if self.peek(0) == TableEnd():
                self.eat()
                return table

        raise BirdwaySyntaxError("hit EOF while parsing table")

    def parse_formatted_string(self):
        string = FormattedString()

        while self.remaining():
            match self.peek(0):
                case FormattedStringDelimiter():
                    self.eat()
                    return string

                case StringContent(value=val):
                    self.eat()
                    string.content.append(val)
                    
                case Variable(name=var):
                    self.eat()
                    formatting = ReadVariable()
                    formatting.name = var
                    string.content.append(formatting)

                case other:
                    raise BirdwaySyntaxError(
                        f"unexpected {other} at line {other._line} while parsing string"
                    )

        raise BirdwaySyntaxError("hit EOF while parsing string")

    def parse_arguments_block(self):
        block = Block()

        while self.remaining():
            match self.peek(0):
                case KeywordParam():
                    self.eat()
                    block.statements.append(self.parse_parameter())
                    if self.peek(0) != LineEnd():
                        raise BirdwaySyntaxError(f"missing semicolon on line {self.peek(0)._line} after parameter")
                    self.eat()
                    
                case BlockEnd():
                    self.eat()
                    return block

                case other:
                    raise BirdwaySyntaxError(
                        f"unexpected {other} at line {other._line} while parsing arguments block"
                    )

        raise BirdwaySyntaxError("hit EOF while parsing arguments block")

    def parse_parameter(self):
        parameter = Parameter()

        match self.peek(0):
            case TypeName(type=t):
                self.eat()
                parameter.type = t

            case other:
                raise BirdwaySyntaxError(f"expected type, got {other} at line {other._line}") 

        if self.peek(0) == UnaryOperator(operator=Unary.ISDEF):
            self.eat()
            parameter.modifier = ArgumentModifier.OPTIONAL

        match self.peek(0):
            case Identifier(name=ident):
                self.eat()
                parameter.name = ident

            case other:
                raise BirdwaySyntaxError(f"expected identifier or modifier, got {other} at line {other._line}")

        if self.peek(0) == FormattedStringDelimiter():
            self.eat()
            parameter.description = self.parse_formatted_string()
            
        return parameter
            
    def parse_block(self):
        block = Block()

        while self.remaining():
            match self.peek(0):
                case BlockEnd():
                    self.eat()
                    return block

                case _:
                    block.statements.append(self.parse_expression())
                    if self.peek(0) != LineEnd():
                        raise BirdwaySyntaxError(f"missing semicolon on line {self.peek(0)._line}")
                    self.eat()

        raise BirdwaySyntaxError("hit EOF while parsing block")
        
    def parse_if(self):
        ifthenelse = IfThenElse()
    
        ifthenelse.condition = self.parse_expression()
        
        tok = self.pop()
        if tok != KeywordThen():
            raise BirdwaySyntaxError(f"expected keyword then, got {tok} on line {tok._line}")

        ifthenelse.statements = self.parse_expression()
        
        if self.peek(0) == KeywordElse():
            self.eat()
            ifthenelse.alternative = self.parse_expression()
            
        return ifthenelse
            
    def parse_println(self):
        println = PrintLine()
    
        println.content = self.parse_expression()
        
        return println