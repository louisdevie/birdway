import parser as syntax
from birdway import *
from exceptions import *
from nodes.base import check_type


class VariableCounter:
    def __init__(self):
        self._last = 0

    def register(self):
        self._last += 1
        return self._last


def resolve_variables(ast):
    var_count = VariableCounter()
    literal_count = VariableCounter()
    block_count = VariableCounter()

    for i, param in enumerate(ast.parameters):
        if param.name in ast.script.context:
            raise BirdwayNameError(
                f"found two parameters/options/flags named {param.name}"
            )
        if param.modifier == ArgumentModifier.OPTIONAL:
            param.id = f"const{var_count.register()}"
            ast.script.context[param.name] = (
                param.id,
                Composite.Nullable(param.type),
                False,
            )
        elif param.modifier == ArgumentModifier.MULTIPLE:
            param.id = f"const{var_count.register()}"
            ast.script.context[param.name] = (
                param.id,
                Composite.Table(param.type),
                False,
            )
            ast.table_list_types.append(param.type)
        else:
            param.id = f"const{var_count.register()}"
            ast.script.context[param.name] = (
                param.id,
                param.type,
                False,
            )
    for i, opt in enumerate(ast.flags_and_options):
        if opt.name in ast.script.context:
            raise BirdwayNameError(
                f"found two parameters/options/flags named {opt.name}"
            )
        if isinstance(opt, syntax.Option):
            if opt.modifier == ArgumentModifier.UNIQUE:
                opt.id = f"const{var_count.register()}"
                ast.script.context[opt.name] = (
                    opt.id,
                    Composite.Nullable(opt.type),
                    False,
                )
            else:
                opt.id = f"const{var_count.register()}"
                ast.script.context[opt.name] = (
                    opt.id,
                    opt.type,
                    False,
                )
            if opt.type == Type.STRING:
                ast.standard_features |= FEATURE_STRING

    ast.script._propagate(ast, var_count, literal_count, block_count)


def check_types(ast):
    check_type(ast.script, Type.VOID)
