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

    for arg in ast.arguments.statements:
        if isinstance(arg, syntax.Parameter):
            if arg.modifier == ArgumentModifier.OPTIONAL:
                if arg.name in ast.script.context:
                    raise BirdwayNameError(f"found two parameters named {arg.name}")
                ast.script.context[arg.name] = (
                    var_count.register(),
                    Composite.Nullable(arg.type),
                )

    propagate(ast.script)


def propagate(node):
    if isinstance(node, syntax.Block):
        for child in node.statements:
            child.context = node.context.copy()
            propagate(child)

    elif isinstance(node, syntax.IfThenElse):
        for child in (node.condition, node.statements, node.alternative):
            child.context = node.context.copy()
            propagate(child)

    elif isinstance(node, syntax.UnaryOperation):
        node.operand.context = node.context.copy()
        propagate(node.operand)

    elif isinstance(node, syntax.ReadVariable):
        if node.name in node.context:
            node.id, node._t = node.context[node.name]

        else:
            raise BirdwayNameError(f'no entity named "{node.name}"')

    elif isinstance(node, syntax.PrintLine):
        node.content.context = node.context.copy()
        propagate(node.content)

    elif isinstance(node, syntax.FormattedString):
        for child in node.content:
            if not isinstance(child, str):
                child.context = node.context.copy()
                propagate(child)

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

        else:
            raise TypeError(f"can't check node of type {type(node)}")

    else:
        raise BirdwayTypeError(f"expected type <{expected}>, got <{node.type}>")
