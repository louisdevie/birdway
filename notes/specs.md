# Language Specifications


## Program structure

### Units

Each source code file is a unit, identified by its name. A unit may contain :

The main program is the unit given to the compiler. It must include a function named
`main`, with no arguments and returning `Void`.

The main program can *use* the functions, constants and types of antoher unit

## Lexical structure

By default, a Birdway source file should be read as UTF-8.

All whitespace characters are ignored, as well as comments.
Line comments begin with two consecutive hyphens `--` and end at the next line feed.
Block comments start with three consecutive hyphens `---` and end at the next triple-hypens.

> **Design choice**
> 
> Both `//` and `#` were already in use as operators,
> so I decided to use `--` for line comments, as it is not unusual
> (for example, Lua, Haskell, SQL and Ada uses this style of comments)
> and `---` for block comments for consistency and simplicity.


### Keywords

Any of the keywords defined in [appendix 1](#keywords), surrounded by word boundaries.


### Symbols

The language punctuation :

```
{    opening brace
}    closing brace
(    opening parenthesis
)    closing parenthesis
[    opening square bracket
]    closing square bracket
.    dot
,    comma
;    semicolon
:    colon
::   double colon
@    at symbol
$    dollar sign
_    underscore
```

### Operators


The different operators :

```
Unary-only operators

~     tilde
#     hash
?     question mark
!     exclamation mark
not   (keyword operator)


Unary or binary operators

-     hyphen


Binary-only operators

&     ampersand
&&    double ampersand
|     vertical bar
^     caret
+     plus sign
==    double equal sign
%     per cent sign
*     asterisk
**    doubme asterisk
/     slash
//    double slash
!=    exclamation mark and equal sign
<<    double less than sign
>     greater than sign
>=    greater than sign and equal sign
>>    doubel greater than sign
and   (keyword operator)
or    (keyword operator)
xor   (keyword operator)


Binary or ternary operators 

<     less than sign
<=    less than sign and equal sign
```

Keyword operators needs to be whole words (there must be a word boundary before and after).


### Identifiers

Identifiers starts with an alphabetic character (ASCII letters) or an underscore,
followed by zero or more alphanumeric characters (ASCII letters and numbers) or undercores.
It must not be a keyword, symbol, operator or literal.


### Delimiters

Double quotes `"` are string literals delimiters.


### Text

Any text inside string literals.

> **Note**
>
> Interpolations aren't text, they should be read the same way as
> the rest of the program. For example, the following :
>
> ```
> "Hi $name !"
> ```
>
> is read as
>
> ```
> string-delimiter   "
> text               Hi␣
> symbol             $
> identifier         name
> text               ␣!
> string-delimiter   "
> ```

### Keyword literals

The keyword `NULL`, `TRUE` and `FALSE`.


### Integer literals

A decimal integer is a single zero (`0`)
or a digit (except zero) followed by zero or more digits.

A binary integer is `0b` followed by one or more `1` and `0`.

An hexadecimal integer is `0x`
followed by one or more hexadecimal digits (one of `0123456789abcdefABCDEF`).


### Byte integer mark

A single quote `'` is a byte mark.


### Decimal literals

A decimal literal is composed of an integer part, a dot (`.`),
a decimal part, and an optional exponent part.

The integer part is a single zero (`0`)
or a digit (except zero) followed by zero or more digits.

The decimal part is one or more digits.

The exponent part is an E (`e` or `E`),
optionally followed by a plus (`+`) or a minus (`-`) sign,
and then a digit (except zero) followed by zero or more digits.

### Regular expressions

*[...]*


## ?

#### Metadata

Informations about the application, used in the help messages.
Metadata is declared using the `meta` statement:
`meta field = value`. The *field* may be one of `name`, `info`, `ver`, `auth` or `url`
an *value* must be be a constant string.

#### Type definitions

User-defined types, or aliases. An alias can be defined with the `type Name is type`
where *Name* is the alias and *type* any valid type. See [User-defined types] for
the definitions of new types.

#### Global constants

...

#### Command-line parameters




## Primitive datatypes


### Void

The `Void` type means no data. It can't take any value, so there cannot be
`Void` variables or constants. The constant `NULL` is of type `Void`,
and used with nullable variables.
It also cannot be used within composite types.


### Boolean

The type `Bool` represents a boolean. It can take two values: `TRUE` or `FALSE`.


### Integer

The type `Int` represents a 64-bit signed integer.
Decimal (`123`), hexadecimal (`0x7b`) and binary (`0b1111011`) literals are integers.

> **Note**
>
> This type can be implicitly converted into a [`Float`](#floating-point-number).
> See [](#implicit-conversion) for more information.


### Floating-point number

The type `Float` represents a 64-bit (double precision) floating-point number.
Float literals are written as `12.3` or `0.123e+2`
`Float`s doesn't support NAN and infinity values.

> **Note**
>
> Even if `123e+4` is technically an integer, it will be interpreted as a `Float`.


### String

The type `Str` represents an Unicode string.
There is no character type, strings of length 1 are used instead.
String literals are enclosed in double quotes : `"Hello"`.
They support variable interpolation (a dollar sign followed by the variable name, e.g. `"x = $x"`)
and expression interpolation (a dollar sign followed by
the expression wrapped in parentheses, e.g. `"x² = $(x**2)"`).

#### String escape sequences

Escape  |Expansion
========|=========================================
`\\`    |`\`
`\"`    |`"`
`\$`    |`$`
`\n`    |A newline (ASCII character 10/LF)
`\t`    |A tabulation (ASCII character 9/TAB)
`\r`    |A carriage return (ASCII character 13/CR)
`\uXXXX`|The Unicode character with code U+XXXX


### Byte

The `Byte` type is an unsigned 8-bit integer used to manipulate binary data.


### File

*[...]*


### Signal

*[...]*


## Composite datatypes

These are types that are formed using other types.


### Nullable types

A type that may have no value.
A nullable type `T?` can be either a value of type `T` or `NULL`.
(Example: if `a` has type `Int?`, then `a + 5` is valid and will compile,
but an error will be thrown at runtime if `a` happens to be `NULL`.)

Void and nested nullables types (`Void?` and `T??` for any type `T`)
aren't valid types.

### Lists

A list is an ordered collection of values indexed by integers starting at 0.
Lists can be created literally using the syntax `[val1, val2, ...]`.

List types are written as ``[T]`` where T is the type of the values.

Void lists (``[Void]``) aren't valid.


### Dictionaries

A dictionary is a collection mapping keys to values.
Dictionaries can be created literally using the syntax
`[key1: val1, key2: val2, ...]`.

Dictionary types are represented as ``[K: T]``
where T is the type of the values and K the type of the keys.

The keys type must be hashable and the values type cannot be ``Void``.


### Tuples

A tuple is a group of different types.
Tuples can be created literally using the syntax `(val1, val2, val3, ...)`.

Unlike lists, the values can have different types. A tuple type
is represented as ``(T1, T2, T3, ...)`` where ``Tn`` is the type
of the nth field.

Tuples must have at least 2 fields,
as bare parentheses ``()`` are invalid and ``(value)`` evaluates to just ``value``.


### Function types

The type of a funtion is represented as ``(T1, T2, ...) -> (R)``
where ``Tn`` is the type of the nth argument and ``R`` the type of
the result.


## User-defined types


### Enumerations

Declaration:

```
enum MyEnum (A, B, C, ...)
```

Create a type *MyEnum* and constants *A*, *B*, *C*, ... of that type.
Each constant is different, and they're ordered as they were declared:
*A* ≠ *B* and *A* < *B*.

Empty enumerations/enumerations with only one value are invalid.

### Structures

Declaration:

```
struct MyStruct (field1: T1, field2: T2, ...)
```

Structures are used to group together different types.
Each field is named and has a non-generic type.
Structures can then be created literally
using the syntax ``MyStruct (field1: value1, field2: value2)``.


```
.. _iconv:

Implicit Conversion
===================

When two values of different types are assigned to the same variable,
there can be an implicit conversion of the values into an unique type.


Nullable Implicit Conversion
----------------------------

When a variable is assigned both ``T`` and ``void`` values, the variable
ends up of type ``T?`` and all the values are converted into that type.


Numeric Implicit Conversion
---------------------------

When a ``float`` variable is assigned ``int`` values, these will be
converted into ``float`` implicitly.


.. note::
   The two conversions above can happen for the same variable,
   that is, if a variable is assigned ``int``, ``float`` and ``void``
   values, they will all be converted into ``float?``.
```

```
Operators
=========

Arithmetic
----------

Addition
^^^^^^^^

.. syntax::
   <expr> **+** <expr>

Returns the sum of two numbers.

+-------+-------+-----------+
| Operands      | Result    |
+=======+=======+===========+
| Int   | Int   | Int       |
+-------+-------+-----------+
| Float | Float | Float     |
+-------+-------+-----------+
| Float | Int   | Float     |
+-------+-------+-----------+
| *any other*   | *illegal* |
| *types*       |           |
+-------+-------+-----------+

Opposite
^^^^^^^^

.. syntax::
   **-** <expr>

Returns the additive inverse of a number

+-------------------+-----------+
| Operand           | Result    |
+===================+===========+
| Int               | Int       |
+-------------------+-----------+
| Float             | Float     |
+-------------------+-----------+
| *any other types* | *illegal* |
+-------------------+-----------+

Substraction
^^^^^^^^^^^^

.. syntax::
   <expr> **-** <expr>

Returns the difference between two numbers.
The types are the same as for addition.

Multiplication
^^^^^^^^^^^^^^

.. syntax::
   <expr> ***** <expr>

Returns the product of two numbers.
The types are the same as for addition.

Division
^^^^^^^^

.. syntax::
   <expr> **/** <expr>

Returns the quotient of two numbers. 

+-------+-------+-----------+
| Operands      | Result    |
+=======+=======+===========+
| Int   | Int   | Float     |
+-------+-------+-----------+
| Float | Float | Float     |
+-------+-------+-----------+
| Float | Int   | Float     |
+-------+-------+-----------+
| *any other*   | *illegal* |
| *types*       |           |
+-------+-------+-----------+

Integer division
^^^^^^^^^^^^^^^^

.. syntax::
   <expr> **//** <expr>

Returns the quotient of the integer division of two numbers.

+-------+-------+-----------+
| Operands      | Result    |
+=======+=======+===========+
| Int   | Int   | Int       |
+-------+-------+-----------+
| *any other*   | *illegal* |
| *types*       |           |
+-------+-------+-----------+

Modulo
^^^^^^

.. syntax::
   <expr> **%** <expr>

Returns the remainder of the integer division of two numbers.
The types are the same as for integer division.

Comparison
----------

Equal
^^^^^

.. syntax::
   <expr> **==** <expr>

Returns wether if two values are equal.


+-------------------+-----------+
| Operands          | Result    |
+===================+===========+
| *same types*      | Bool      |
+---------+---------+-----------+
| Void    | Void    | *illegal* |
+---------+---------+-----------+
| *different types* | *illegal* |
+-------------------+-----------+

Not equal
^^^^^^^^^

.. syntax::
   <expr> **!=** <expr> 

The types are the same as for equality.

Less than
^^^^^^^^^

.. syntax::
   <expr> **<** <expr>

Greater than
^^^^^^^^^^^^

.. syntax::
   <expr> **>** <expr>

Less or equal
^^^^^^^^^^^^^

.. syntax::
   <expr> **<=** <expr>

Greater or equal
^^^^^^^^^^^^^^^^

.. syntax::
   <expr> **>=** <expr>

Between (exclusive)
^^^^^^^^^^^^^^^^^^^

.. syntax::
   <expr> **<** <expr> **<** <expr>

Between (inclusive, exclusive)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. syntax::
   <expr> **<=** <expr> **<** <expr>

Between (exclusive, inclusive)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. syntax::
   <expr> **<** <expr> **<=** <expr>

Between (inclusive)
^^^^^^^^^^^^^^^^^^^

.. syntax::
   <expr> **<=** <expr> **<=** <expr>



Logical
-------

Negation
^^^^^^^^

.. syntax::
   **not** <expr>

OR
^^^

.. syntax::
   <expr> **or** <expr>

AND
^^^

.. syntax::
   <expr> **and** <expr>

Exclusive OR
^^^^^^^^^^^^

.. syntax::
   <expr> **xor** <expr>



Bitwise
-------

Negation
^^^^^^^^

.. syntax::
   **~** <expr>

OR
^^^

.. syntax::
   <expr> **|** <expr>

AND
^^^

.. syntax::
   <expr> **&** <expr>

Exclusive OR
^^^^^^^^^^^^

.. syntax::
   <expr> **^** <expr>

Left shift
^^^^^^^^^^

.. syntax::
   <expr> **<<** <expr>

Right shift
^^^^^^^^^^^

.. syntax::
   <expr> **>>** <expr>

Other
-----

Not null
^^^^^^^^

.. syntax::
   **?** <expr>

Is null
^^^^^^^

.. syntax::
   **!** <expr>

Size
^^^^

.. syntax::
   **#** <expr>

Concatenation
^^^^^^^^^^^^^

.. syntax::
   <expr> **&&** <expr>

Union
^^^^^

.. syntax::
   <expr> **||** <expr>
```

```
Conditional Statements
======================

.. _if:
If Statements
-------------

.. syntax::
   | **if** *condition:* <expr>
   | **then** *a:* <expr>
   | *[* **else** *b:* <expr> *]*

Takes the value *a* if *condition* is ``TRUE``, or *b* otherwise.

*condition* has to be a :ref:`bool` while *a* and *b* need to be
of the same type, which will be the type of the if statement.

The ``else`` part can be omitted, and the statement will take
the value ``NULL`` if *condition* is ``FALSE``.


.. _switch:
Switch Statements
-----------------

.. syntax::
   | **switch** *value:* <expr>
   | *{* **case** *case:* <expr> **do** *result:* <expr> */}*
   | *[* **default** *default:* <expr> *]*

Takes the value of the *result* of the first *case* that match *value*.

The types accepted for *value* are :ref:`integers <int>`, :ref:`bytes <byte>`
and :ref:`enumerations <enum>`. If a ``case`` have the same type as *value*,
it will match if the two values are equal; if it is a list of the type of *value*,
it will match if the value is in the list.
All *results* have to be of the same type, which will be the type of the statement.
```

```
Loops
=====


.. _break_next:

Break and Next
--------------

These two statements can be used inside any of the following loops.
If used inside a block, they will propagate and affect the containing loop.

.. syntax::
   **break**

Exits the loop immediately, skipping the ``then end`` part if there is one.

.. syntax::
   **next**

Jump to the next iteration of the loop immediately.


For Loop
--------

.. syntax::
   **for** variable **in** <table> **do** <expression> *[* **then** <end> *]*

``variable`` should be a valid identifier, and a *constant* with this name will
take the *values* inside ``table``. ``expression`` will be evaluated for each iteration
and the results will be collected in a list, followed by ``end``. The type of
the statement will be the type of ``expression``, and the type of ``variable`` is
deduced from the type of ``table`` : [int] maps to int, [[int]] maps to [int]
and [int: str] maps to str.

.. warning::
   ``variable`` isn't in scope when ``end`` is evaluated.


While Loop
----------

.. syntax::
   **while** condition **do** expression [**then** end]

``expression`` will be evaluated as long as ``condition`` is true, and
the results will be collected in a list, followed by ``end``. If the
condition is false from the start, there will be no iterations.

Until Loop
----------

.. syntax::
   **do** expression **until** condition [**then** end]

``expression`` will be evaluated until ``condition`` is false, and
the results will be collected in a list, followed by ``end``. Even
if the condition is false from the start, there will be at least
one iteration.
```

```
Blocks
======

Blocks are used to executes multiple statements one after another.

.. syntax::
   **{** *{ statement:* <expr> *|* <var-decl> *|* <func-decl> **;** */}* *[ tail-expression:* <expr> *]* **}**

Each statement is evaluated one after another,
and if a signal is sent by one of the statements,
the block stops its execution and propagate the signal.

If the *tail-expression* is present, the block takes that value.
Otherwise, the block is ``NULL``.
```

```
Functions
=========

Defining functions
------------------

.. syntax::
   | *[* **pub** *]* **func** name:* *[* **$** *]* &IDENT **(** *{*
   |   *[* **@** *|* **$** *] parameter:* &IDENT *[* **:** <type> *] /* **,**
   | *}* **) ->** *result:* <expr>

A function can be have multiple implementations with different types or number of parameters.
``func`` declarations are allowed in the program body and blocks.

Parameters
^^^^^^^^^^

By default, arguments are passed by immutable reference.
If the parameter name is preceded by an at symbol ``@``,
it will be passed by value (and mutable). If it is preceded
by a dollar sign ``$``, it will be passed by mutable reference.

.. why::
   Originally, function parameters were only passed by immutable reference,
   and if you wanted to have a copy of the value, you needed to do something like :

   .. code-block:: bw

      func f(x) -> {
          let $x = x;
      
          -- ...
      }

   So I used the at symbol, wich was the last ASCII symbol left unused
   at that time to act as a modifier to have cleaner code.

If a parameter isn't given a type, it becomes generic
and a different function will be implemented for each
type passed when calling the function, and the type is valid if the
function can be be compiled using this type.
For example, if we have this function :

.. code-block:: bw

   func add(a, b) -> a + b

We can call call this function with any numeric types because that's what is
required by the ``+`` operator. The operators and statements you
use in a function will determine what types can be passed to generic parameters.

The body
^^^^^^^^

After the arrow ``->``, there is the expression that will be the return value of the
function. If the body is a block, you can return a value using the ``return`` statement.
Note that if the control reach the end of that block, the function will return ``NULL``,
and make the return type nullable.

Anonymous functions
^^^^^^^^^^^^^^^^^^^

Functions can also be declared inline :

.. syntax::
   | **(** *{*
   |   *[* **@** *|* **$** *] parameter:* &IDENT /* **,**
   | *}* **) ->** *result:* <expr>


Return
------

.. syntax::
   | **return** *[ value:* <expr> *]*

Exit the function, returning *value* or ``NULL`` if no value is specified.


Calling functions
-----------------

.. syntax::
   <name> **(** *{ argument:* <expr> */* **,** *}* **)**

Call the implementation of the function that match
the types and the number of the arguments passed.
If multiples implementations match, the less ambiguous one
(the one with the least generic parameters) is used.


Method calls
^^^^^^^^^^^^

.. syntax::
   <expr> **::** <name> **(** *{ argument:* <expr> */* **,** *}* **)**

The expression before the double-colon ``::`` will be passed as the first
argument of the function.

.. why::
   Instead of doing this :

   .. code-block:: bw

      f3(f2(f1(a)), b)

   this syntax lets you chain function calls like this :

   .. code-block:: bw

      a::f1()::f2()::f3(b)

   which is more readable.

   I chose a double colon because I wanted to reserve
   the dor ``.`` for accessing struct/tuple fields only.
```

```
Signals
=======

Signals are codes that are propagated down the stack until they're *received*.
If a signal reach the bottom of the stack, the signal code is displayed and the program stops.


Error signals
-------------

Error signals are used to stop the program after something went wrong (e.g. a division by zero),
or if the program has successfully finished.
They can be thrown by the user with a :ref:`throw` statement
and received by a :ref:`try` statement.


Others signals
------------------

The :ref:`return`, :ref:`break_next` statements throws specials signals that can't be
received by :ref:`try` statements.

```

```
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

```

```
Appendices
==========


.. _reserved:
List of all reserved names
--------------------------

Keywords
^^^^^^^^

.. code-block:: text

   break
   const
   do
   else
   enum
   flag
   for
   from
   func
   if
   in
   let
   limit
   meta
   on
   option
   param
   print
   println
   pub
   read
   readln
   return
   next
   struct
   then
   throw
   to
   try
   until
   use
   while


Operators
^^^^^^^^^

.. code-block:: text

   and
   not
   or
   xor


Literals
^^^^^^^^

.. code-block:: text

   FALSE
   NULL
   TRUE
```
