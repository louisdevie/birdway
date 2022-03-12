from birdway import *
import parser as syntax

SUCCESS = 0


def transpile(ast, **kwargs):
    code = """/*=== GENERATED BY BIRDWAY VERSION PYA-EA853 ===*/
        #include <stdio.h>
        #include <stdbool.h>
        #include <stdlib.h>
        #include <stdint.h>"""
    code += generate_string_constants(ast, kwargs)
    code += features(ast, kwargs)
    code += initialise_script(ast, kwargs)
    code += generate_argument_parser(ast, kwargs)
    code += transpile_script(ast, kwargs)
    code += generate_main_function(ast, kwargs)
    return code


def generate_string_constants(ast, kwargs):
    return f"""
        const char BIRDWAY_APPLICATION_IDENTIFICATION[] = "{kwargs.get("name", "[unnamed]")}";"""


def generate_main_function(ast, kwargs):
    return f"""
        int main(int argc, char **argv)
        {{
            {
                (
                    "".join([
                        initialise_argument(*arg)
                        for arg in enumerate(ast.arguments.statements)
                    ])
                    + "void *argr["
                    + str(len(ast.arguments.statements))
                    + "] = {"
                    + ", ".join([f"&arg{i}" for i, _ in enumerate(ast.arguments.statements)])
                    + "};"
                ) if ast.arguments is not None else "void**argr=NULL;"
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
            {transpile_node(ast.script, 'tmp')}
            return {SUCCESS};
        }}"""

def transpile_node(node, tui):
    match node:
        case syntax.PrintLine(content=c):
            return f"""
                {transpile_node(c, f"{tui}1")}
                birdwayPrintln(&{tui}1);"""

        case syntax.StringLiteral(id=n, string=v):
            return f"""
                struct BirdwayString {tui};
                birdwayStringLiteral(&{tui}, {n}, {len(v)});"""

        case other:
            raise TypeError(f"no implementation for node of type {type(other)}")

def initialise_script(ast, kwargs):
    return initialise_node(ast.script)

def initialise_node(node):
    match node:
        case syntax.PrintLine(content=value):
            return initialise_node(value)

        case syntax.StringLiteral(id=name, string=value):
            return f"""const uint32_t {
                name
            }[{
                len(value)
            }] = {{{
                ', '.join([str(ord(char)) for char in value])
            }}};"""

        case other:
            raise TypeError(f"can't initialise node of type {type(other)}")


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
                        for arg in enumerate(ast.arguments.statements)
                    ]) if ast.arguments is not None else ""
                }
            }}
            return 0;
        }}"""


def features(ast, kwargs):
    std_types = ""

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
            }}"""

    if kwargs.get("features", 0) & FEATURE_FORMATTING:
        std += f"""
            """

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

    return std_types + std_funcs


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
