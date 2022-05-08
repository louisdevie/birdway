import parser as syntax
from birdway import *
from exceptions import *
from nodes.base import check_type


class VariableCounter:
    def __init__(self):
        self._c = 0

    def register(self):
        self._c += 1
        return self._c


def resolve_variables(ast):
    var_count = VariableCounter()
    literal_count = VariableCounter()
    block_count = VariableCounter()

    if ast.arguments is not None:
        for i, arg in enumerate(ast.arguments):
            if isinstance(arg, syntax.Parameter):
                if arg.name in ast.script.context:
                    raise BirdwayNameError(f"found two parameters named {arg.name}")
                if arg.modifier == ArgumentModifier.OPTIONAL:
                    arg.id = f"const_{var_count.register()}"
                    ast.script.context[arg.name] = (
                        arg.id,
                        Composite.Nullable(arg.type),
                    )
                    if arg.type == Type.STRING:
                        ast.standard_features |= FEATURE_STRING
                elif arg.modifier == ArgumentModifier.MULTIPLE:
                    arg.id = f"const_{var_count.register()}"
                    ast.script.context[arg.name] = (
                        arg.id,
                        Composite.Table(arg.type),
                    )
                    if arg.type == Type.STRING:
                        ast.standard_features |= FEATURE_STRING

    ast.script._propagate(ast, var_count, literal_count, block_count)


def check_types(ast):
    check_type(ast.script, Type.VOID)
