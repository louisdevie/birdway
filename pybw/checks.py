import parser as syntax
from birdway import *
from exceptions import *


class VariableCounter:
    def __init__(self):
        self._c = 0

    def register(self):
        self._c += 1
        return self._c


def resolve_variables(ast):
    var_count = VariableCounter()
    const_count = VariableCounter()

    if ast.arguments is not None:
        for i, arg in enumerate(ast.arguments.statements):
            if isinstance(arg, syntax.Parameter):
                if arg.modifier == ArgumentModifier.OPTIONAL:
                    if arg.name in ast.script.context:
                        raise BirdwayNameError(f"found two parameters named {arg.name}")
                    arg.id = str(i)
                    ast.script.context[arg.name] = (
                        str(i),
                        Composite.Nullable(arg.type),
                    )
                    if arg.type == Type.STRING:
                        ast.standard_features |= FEATURE_STRING

    propagate(ast, ast.script, var_count, const_count)


def propagate(ast, node, vc, cc):
    if isinstance(node, syntax.Block):
        for child in node.statements:
            child.context = node.context.copy()
            propagate(ast, child, vc, cc)

    elif isinstance(node, syntax.IfThenElse):
        for child in (node.condition, node.statements, node.alternative):
            child.context = node.context.copy()
            propagate(ast, child, vc, cc)

    elif isinstance(node, syntax.UnaryOperation):
        node.operand.context = node.context.copy()
        propagate(ast, node.operand, vc, cc)

    elif isinstance(node, syntax.ReadVariable):
        if node.name in node.context:
            node.id, node._t = node.context[node.name]

        else:
            raise BirdwayNameError(f'no entity named "{node.name}"')

    elif isinstance(node, syntax.PrintLine):
        ast.standard_features |= FEATURE_PRINTLN
        node.content.context = node.context.copy()
        propagate(ast, node.content, vc, cc)

    elif isinstance(node, syntax.FormattedString):
        ast.standard_features |= FEATURE_STRING
        for child in node.content:
            if not isinstance(child, str):
                child.context = node.context.copy()
                propagate(ast, child, vc, cc)

    elif isinstance(node, syntax.StringLiteral):
        ast.standard_features |= FEATURE_STRING
        node.id = f"STRING_LITERAL_{cc.register()}"

    else:
        raise TypeError(f"can't propagate context to node of type {type(node)}")


def check_types(ast):
    check_type_of(ast.script, Type.VOID)


def check_type_of(node, expected):
    if node.type == expected:
        if isinstance(node, syntax.Block):
            for child in node.statements:
                check_type_of(child, Type.VOID)

        elif isinstance(node, syntax.IfThenElse):
            check_type_of(node.condition, Type.BOOLEAN)
            check_type_of(node.statements, node.type)
            check_type_of(node.alternative, node.type)

        elif isinstance(node, syntax.UnaryOperation):
            pass

        elif isinstance(node, syntax.ReadVariable):
            pass

        elif isinstance(node, syntax.PrintLine):
            check_type_of(node.content, Type.STRING)

        elif isinstance(node, syntax.FormattedString):
            pass

        elif isinstance(node, syntax.StringLiteral):
            pass

        else:
            raise TypeError(f"can't check node of type {type(node)}")

    else:
        raise BirdwayTypeError(f"expected type <{expected}>, got <{node.type}>")
