from birdway import *
import parser as syntax

SUCCESS = 0


def transpile(ast, **kwargs):
    code = """/*=== GENERATED BY BIRDWAY VERSION PYA-7ABD5 ===*/
        #include <stdio.h>
        #include <stdbool.h>
        #include <stdlib.h>
        #include <stdint.h>"""
    code += features_types(ast, kwargs)
    code += generate_constants(ast, kwargs)
    code += features_functions(ast, kwargs)
    code += initialise_script(ast, kwargs)
    code += generate_argument_parser(ast, kwargs)
    code += transpile_script(ast, kwargs)
    code += generate_main_function(ast, kwargs)
    return code


def generate_constants(ast, kwargs):
    return f"""
        const char BIRDWAY_APPLICATION_IDENTIFICATION[] = "{kwargs.get("name", "[unnamed]")}";
        const uint32_t NULL_REPR[6] = {{60, 110, 117, 108, 108, 62}};"""


def generate_main_function(ast, kwargs):
    return f"""
        int main(int argc, char **argv)
        {{
            {
                (
                    "".join([
                        initialise_argument(*arg)
                        for arg in enumerate(ast.arguments)
                    ])
                    + "void *argr["
                    + str(len(ast.arguments))
                    + "] = {"
                    + ", ".join([f"&arg{i}" for i, _ in enumerate(ast.arguments)])
                    + "};"
                ) if ast.arguments else "void**argr=NULL;"
            }
            int parsingResult = birdwayParseAllArguments(argc, argv, argr);
            if (parsingResult)
            {{
                return parsingResult;
            }}
            else
            {{
                return birdwayMain(argr);
            }}
        }}"""


def transpile_script(ast, kwargs):
    return f"""
        int birdwayMain(void **globals) 
        {{
            int err = {SUCCESS};
            {transpile_node(ast.script, 'tmp')}
            return err;
        }}"""

def transpile_node(node, tui):
    match node:
        case syntax.PrintLine(content=c):
            return f"""
                {transpile_node(c, tui+"1")}
                birdwayPrintln({reference_node(c, tui+"1")});"""

        case syntax.StringLiteral(id=n, string=v):
            return f"""
                struct BirdwayString {tui};
                birdwayStringLiteral(&{tui}, {n}, {len(v)});"""

        case syntax.Block(id=block):
            return f"""
                err = {block}({"".join([node.context[v][0] for v in node.using])});
                if (err) return err;"""

        case syntax.IfThenElse(condition=cond, statements=res, alternative=alt):
            return f"""
                {transpile_node(cond, tui+"1")}
                if ({reference_node(cond, tui+"1")})
                {{
                    {transpile_node(res, tui+"2")}
                }}
                else
                {{
                    {transpile_node(alt, tui+"3")}
                }}"""

        case syntax.UnaryOperation(operand=val, operator=op):
            if op == Unary.ISDEF:
                return f"""{transpile_node(val, tui+"1")}"""
            else:
                raise TypeError(f"unknown unary operator {op}")

        case syntax.ReadVariable(id=var):
            return ""

        case syntax.FormattedString(content=c):
            return f"""
                struct BirdwayString {tui};
                birdwayStringEmpty(&{tui});
                {
                    "".join([
                        transpile_node(n, tui+str(i))
                        + formatter(n, tui+str(i))
                        + (
                            f"birdwayStringConcat(&{tui}, &{tui}{i}F);"
                            if not n.type == Type.STRING
                            else f"birdwayStringConcat(&{tui}, &{tui}{i});"
                        )
                        for i, n in enumerate(c)
                    ])
                }"""

        case other:
            raise TypeError(f"no implementation for node of type {type(other)}")

def initialise_script(ast, kwargs):
    return initialise_node(ast.script)

def initialise_node(node):
    match node:
        case syntax.PrintLine(content=value):
            return initialise_node(value)

        case syntax.StringLiteral(id=name, string=value):
            # TODO : pre-build the string in the stack
            return f"""
                const uint32_t {
                    name
                }[{
                    len(value)
                }] = {{{
                    ', '.join([str(ord(char)) for char in value])
                }}};"""

        case syntax.Block(id=block):
            return f"""
                {"".join([initialise_node(s) for s in node.statements])}
                int {block}({
                    "".join(
                        [
                            ctype(node.context[v][1]) + "*" + node.context[v][0]
                            for v in node.using
                        ]
                    )
                }) {{
                    int err = {SUCCESS};
                    {"".join([transpile_node(s, "tmp"+str(i)) for i, s in enumerate(node.statements)])}
                    return err;
                }}"""

        case syntax.IfThenElse(condition=cond, statements=res, alternative=alt):
            return f"""
                {initialise_node(cond)}
                {initialise_node(res)}
                {initialise_node(alt)}"""

        case syntax.UnaryOperation(operand=val):
            return f"""
                {initialise_node(val)}"""

        case syntax.ReadVariable():
            return ""

        case syntax.FormattedString(content=content):
            return "\n".join(
                [
                    initialise_node(lit)
                    for lit in content
                    if isinstance(lit, syntax.StringLiteral)
                ]
            )

        case other:
            raise TypeError(f"can't initialise node of type {type(other)}")

def reference_node(node, tui):
    match node:
        case syntax.ReadVariable(id=var):
            return var

        case syntax.UnaryOperation(operand=val, operator=op):
            if op == Unary.ISDEF:
                return f"""({reference_node(val, tui+"1")}) != NULL"""
            else:
                raise TypeError(f"unknown unary operator {op}")

        case other:
            return "&" + tui

def generate_argument_parser(ast, kwargs):
    return f"""
        int birdwayParseAllArguments(int argc, char **argv, void **output)
        {{
            bool isShort;
            char *name;
            char *value;
            int pos = -1;
            for (int i=1; i<argc; i++)
            {{
                if (birdwayParseOneArgument(argv[i], &pos, &isShort, &name, &value))
                {{
                    return 1;
                }}
                {
                    "".join([
                        generate_argument_checker(*arg)
                        for arg in enumerate(ast.arguments)
                    ]) if ast.arguments else ""
                }
            }}
            return 0;
        }}"""


def features_types(ast, kwargs):
    std_types = ""

    if kwargs.get("features", 0) & FEATURE_STRING:
        std_types += f"""
            struct BirdwayChar
            {{
                uint32_t ucp;
                struct BirdwayChar *next;
            }};
            struct BirdwayString
            {{
                struct BirdwayChar *start;
                struct BirdwayChar *end;
                size_t length;
            }};"""

    return std_types

def features_functions(ast, kwargs):
    std_funcs = f"""
        int birdwayParseOneArgument(char *arg, int *pos, bool *isShort, char **name, char **value)
        {{
            *isShort = false;
            *name = NULL;
            *value = arg;
            ++*pos;
            return 0;
        }}"""

    if kwargs.get("features", 0) & FEATURE_STRING:
        std_funcs += f"""
            int birdwayStringEmpty(struct BirdwayString *str)
            {{
                str->start = NULL;
                str->end = NULL;
                str->length = 0;
            }}
            int birdwayStringFromASCII(struct BirdwayString *str, char *src)
            {{
                birdwayStringEmpty(str);
                while (*src)
                {{
                    if (str->end == NULL)
                    {{
                        str->end = malloc(sizeof (struct BirdwayChar));
                        str->start = str->end;
                    }}
                    else
                    {{
                        str->end->next = malloc(sizeof (struct BirdwayChar));
                        str->end = str->end->next;
                    }}
                    str->end->ucp = *src;
                    str->end->next = NULL;
                    ++str->length;
                    ++src;
                }}
            }}
            int birdwayStringLiteral(struct BirdwayString *str, const uint32_t *src, size_t len)
            {{
                birdwayStringEmpty(str);
                str->end = malloc(sizeof (struct BirdwayChar));
                str->start = str->end;
                str->end->ucp = src[0];
                str->end->next = NULL;
                for (int i=1; i<len; i++)
                {{
                    str->end->next = malloc(sizeof (struct BirdwayChar));
                    str->end = str->end->next;
                    str->end->ucp = src[i];
                    str->end->next = NULL;
                }}
                str->length = len;
            }}
            int birdwayStringConcat(struct BirdwayString *str1, struct BirdwayString *str2)
            {{
                str1->end->next = str2->start;
                str1->length += str2->length;
            }}"""

    if kwargs.get("features", 0) & FEATURE_FORMATTING:
        std_funcs += f"""
            int birdwayFormatNullableString(struct BirdwayString **input, struct BirdwayString *output)
            {{
                if (*input == NULL)
                {{
                    birdwayStringLiteral(output, NULL_REPR, 6);
                }}
                else
                {{
                    *output = **input;
                }}
            }}"""

    if kwargs.get("features", 0) & FEATURE_PRINTLN:
        std_funcs += f"""
            int birdwayPrintln(struct BirdwayString *content)
            {{
                struct BirdwayChar *cursor = content->start;
                while(cursor != NULL)
                {{
                    putchar(cursor->ucp);
                    cursor = cursor->next;
                }}
                putchar(10);
            }}"""

    return std_funcs


def generate_argument_checker(i, node):
    return f"""
        if (pos == {node.id})
        {{
            output[{i}] = malloc(sizeof (struct BirdwayString));
            birdwayStringFromASCII(output[{i}], value);
        }}"""


def initialise_argument(i, node):
    return f"""
        struct BirdwayString *arg{i} = NULL;"""

def formatter(node, tui):
    if node.type == Type.STRING:
        return ""

    else:
        return f"""
            struct BirdwayString {tui}F;
            err = birdwayFormat{nameof(node.type)}({reference_node(node, tui+"1")}, &{tui}F);
            if (err) return err;\n"""



def nameof(T):
    match T:
        case Type.STRING:
            return "String"

        case Composite.Nullable(val=val):
            return "Nullable"+nameof(val)

        case other:
            raise TypeError(f"no type name for <{other}>")

def ctype(T):
    match T:
        case Type.STRING:
            return "struct BirdwayString "

        case Composite.Nullable(val=val):
            return ctype(val)+"*"

        case other:
            raise TypeError(f"no internal type for <{other}>")