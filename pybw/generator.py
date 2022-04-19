from birdway import *
import parser as syntax
from nodes.base import ctype


def transpile(ast, **kwargs):
    code = """/*=== GENERATED BY BIRDWAY VERSION PYA-220416 ===*/
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
        struct BirdwayChar NULL_REPR[6] = {{{{60, NULL}}, {{110, NULL}}, {{117, NULL}}, {{108, NULL}}, {{108, NULL}}, {{62, NULL}}}};"""


def generate_main_function(ast, kwargs):
    return f"""
        int main(int argc, char **argv)
        {{
            {"".join([arg._initialise() for arg in ast.arguments])}
            int parsingResult = birdwayParseAllArguments({",".join(["argc", "argv"]+["&"+arg.id for arg in ast.arguments])});
            if (parsingResult)
            {{
                return parsingResult;
            }}
            else
            {{
                return birdwayMain({",".join(["&"+arg.id for arg in ast.arguments])});
            }}
        }}"""


def transpile_script(ast, kwargs):
    return f"""
        int birdwayMain({
            "".join(
                [
                    ctype(ast.script.context[v][1]) + "*" + ast.script.context[v][0]
                    for v in ast.script.using
                ]
            )
        }) 
        {{
            int err = 0;
            {ast.script._transpile('tmp')}
            return err;
        }}"""


def initialise_script(ast, kwargs):
    return ast.script._initialise()


def generate_argument_parser(ast, kwargs):
    return f"""
        int birdwayParseAllArguments({
            ",".join(
                ["int argc", "char **argv"] + [
                    ctype(ast.script.context[v][1]) + "*" + ast.script.context[v][0]
                    for v in ast.script.using
                ]
            )
        })
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
            void birdwayStringEmpty(struct BirdwayString *str)
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
                return 0;
            }}
            int birdwayStringLiteral(struct BirdwayString *str, struct BirdwayChar *src, size_t len)
            {{
                str->start = src;
                str->end = src + len - 1;
                str->length = len;
                for (int i = 0; i<(len-1); i++)
                {{
                    src[i].next = &src[i+1];
                }}
                return 0;
            }}
            void birdwayStringConcat(struct BirdwayString *str1, struct BirdwayString *str2)
            {{
                struct BirdwayChar *cur1 = NULL;
                struct BirdwayChar *cur2;
                if (str1->start == NULL)
                {{
                    if (str2->start != NULL)
                    {{
                        str1->start = malloc(sizeof (struct BirdwayChar));
                        str1->end = str1->start;
                        str1->start->ucp = str2->start->ucp;
                        str2->start->next = NULL;
                        cur1 = str1->start;
                        cur2 = str2->start->next;
                    }}
                }}
                else
                {{
                    cur1 = str1->end;
                    cur2 = str2->start;
                }}
                while (cur2 != NULL)
                {{
                    cur1->next = malloc(sizeof (struct BirdwayChar));
                    cur1 = cur1->next;
                    cur1->ucp = cur2->ucp;
                    cur1->next = NULL;
                    cur2 = cur2->next;
                }}
                str1->end = cur1;
            }}"""

    if kwargs.get("features", 0) & FEATURE_FORMATTING:
        std_funcs += f"""
            int birdwayStringAppendLiteral(struct BirdwayString *str, struct BirdwayChar *src, size_t len)
            {{
                if (str->end != NULL)
                {{
                    str->end->next = src;
                }}
                else
                {{
                    str->start = src;
                }}
                str->end = src + len - 1;
                str->length += len;
                for (int i = 0; i<(len-1); i++)
                {{
                    src[i].next = &src[i+1];
                }}
                return 0;
            }}
            int birdwayFormatNullableString(struct BirdwayString **input, struct BirdwayString *output)
            {{
                if (*input == NULL)
                {{
                    return birdwayStringLiteral(output, NULL_REPR, 6);
                }}
                else
                {{
                    *output = **input;
                    return 0;
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
                return 0;
            }}"""

    return std_funcs


def generate_argument_checker(i, node):
    return f"""
        if (pos == {i})
        {{
            *{node.id} = malloc(sizeof (struct BirdwayString));
            birdwayStringFromASCII(*{node.id}, value);
        }}"""
