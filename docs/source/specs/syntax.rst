Entire language syntax
======================

Below is a complete (well, not yet) definition of the syntax of the language,
written in EBNF. 

.. code-block:: EBNF

   primary expression = void literal
                      | boolean literal
                      | numeric literal
                      | string literal
                      | name
                      | collection literal
                      | tuple literal
                      | struct literal
                      | block
                      | inline function
                      | function call
                      | method call;

   if statement = "if", expression, "then", expression, [ "else", expression ];

   switch statement = "switch", expression, { "case", expression, "do", expression }, [ "default", expression ];

   conditional = if statement | switch statement;

   for loop = "for", identifier, "in", expression, "do", expression;

   while loop = "while", expression, "do", expression;

   loop = for loop | while loop;

   unary only operator = "~" | "#" | "?" | "!" | "not";

   unary or binary operator = "-";

   binary only operator = "&"   | "&&"  | "|"   | "^"   | "+"
                        | "=="  | "%"   | "*"   | "**"  | "/"
                        | "//"  | "!="  | "<<"  | ">"   | ">="
                        | ">>"  | "and" | "or"  | "xor";

   binary or ternary operator = "<" | "<=";

   unary operator = unary only operator | unary or binary operator;

   binary operator = binary only operator
                   | unary or binary operator
                   | binary or ternary operator;

   ternary operator = binary or ternary operator;

   expression = unary operator, expression
              | primary expression, binary operator, expression
              | (
                   primary expression,
                   ternary operator,
                   primary expression,
                   ternary operator,
                   expression,
                )
              | primary expression
              | conditional
              | loop
              | try statement
              | io
              | control;

   primary type = identifier
                | decimal integer literal
                | "(", [ type { ",", type } [ "," ] ] ")"
                | "[", type, [ ":", type ], "]"
                | primary type, "?";

   type = primary type, "->", type
        | primary type;

   function parameter = [ "@" | "$" ], identifier, [ ":", type ];

   function definition = [ "pub" ], "func", [ "$" ], identifier, "(",
      [ function parameter { ",", function parameter } [ "," ] ]
      ")", "->", expression;

   meta statement = "meta", identifier, "=", expression;

   use statement = [ "pub" ], "use", identifier;

   param statement = "param", [ "?" | "*" ], identifier, ":", type,
      [ "(", expression, ")" ];

   option statement = "option", [ "*" ], identifier, ":", type, [ "=", expression ],
      [ "(", expression, ")" ];
   
   flag statement = "flag", [ "*" ], identifier,
      [ "(", expression, ")" ];

   command line parameter = param statement | option statement | flag statement;

   constant declaration = [ "pub" ], "const", identifier, "=", expression;

   enum declaration = [ "pub" ], "enum", identifier, "(",
      [ identifier { ",", identifier } [ "," ] ],
      ")";

   struct field = identifier, ":", type;

   struct declaration = [ "pub" ], "struct", identifier, "(",
      [ struct field { ",", struct field } [ "," ] ],
      ")";

   type declaration = enum declaration | struct declaration;

   program = {
      (
         meta statement
       | use statement
       | command line parameter
       | type declaration
       | constant declaration
       | function declaration
      ),
      ";"
   };
