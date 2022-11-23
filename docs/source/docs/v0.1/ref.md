@base


# Birdway 0.1 language reference

!!! warning
    This document is still a draft.

[TOC]


## 1. Program structure

Each source file is a unit.

A program is made of one [entry point unit](#112-entry-point) and zero or
more [module units](#113-module-units).


### 1.1. File format

Birdway source files should be encoded in ASCII or UTF-8 and have a `.bw`
extension.


### 1.2. Entry point

The unit designated to be the entry point of the program must contain a function
named `main`, without arguments, and returning `null`. This function will be
executed when the program starts, *after parsing command-line arguments*. The
command-line parameters declared in it will be used for the program. 


### 1.3. Module units

The other units used by the main one will have all their functions and constants
exposed.


## 2. Lexical elements

Characters in source files can be grouped into tokens, depending on the *lexical
context*. The context at the beginning of a file is always the main context.


### 2.1. Main context 


#### 2.1.1. Whitespaces

Horizontal tabs, line feeds, carriage return and spaces are always valid but
ignored.


#### 2.1.2. Comments

Line comments starts with two hyphens `--` and end at the next two hyphens or
line feed.

Block comments starts with three hyphens `---` and end at the next three
hyphens.

Comments are also ignored.


#### 2.1.3. Punctuation

The punctuators of the language includes: braces `{` `}`, parentheses `(` `)`,
square brackets `[` `]`, dots `.`, commas `,`, semicolons `;`, colons `:` and
double colons `::`, at symbols `@`, dollar signs `$`, single underscores `_`,
arrows `->` and equal signs `=`.


#### 2.1.4. Operators

The unary operators are `#`, `?` and the keyword `not`.

The only unary and binary operator is `-`.

The binary operators are `&`, `|`, `^`, `+`, `==`, `%`, `*`, `/`, `//`, `:=`,
`!=`, `>`, `>>`, `>=`, `<`, `<<`, `<=`, and the keywords `and` and `or`.


#### 2.1.5. Keywords

Below is a list of the keywords of the language (excluding keyword operators and
primitive types):

```
break     params
const     print
do        println
else      read
enum      readln
false     return
for       struct
from      then
func      throw
if        to
in        true
let       try
next      use
null      while
on
```


#### 2.1.6. Primitive type names

The primitive types are `Void`, `Bool`, `Int`, `Float`, `Str`, `File` and
`Signal`.


#### 2.1.7. Number literals 


##### 2.1.7.1. Decimal integer literals

Decimal integers can either be one or more decimal digits (`0123456789`) that
doesn't start by a zero, or a single zero.


##### 2.1.7.2. Hexadecimal integer literals

Hexadecimal integers are `0x` followed by one or more hexadecimal digits
(`0123456789aAbBcCdDeEfF`).


##### 2.1.7.3. Binary integer literals

Binary integers are `0b` followed by one or more binary digits (`01`).


##### 2.1.7.4. Floating-point literals

Floating-point literals are made of an integer part, followed by one or the two
of a fractional part and an exponent part.

The integer part is the same as a
[decimal integer](#2151-decimal-integer-literals).

The fractional part is a dot `.` followed by one or more decimal digits.

The exponent part is the letter E (either lowercase `e` or uppercase `E`),
followed by an optional sign (`+`, `-` or nothing) and a
[decimal integer](#2151-decimal-integer-literals).


#### 2.1.8. Identifiers

Identifiers are made of one or more of the following characters: lowercase and
uppercase ASCII letters, digits and undercores.

Identifiers may not start by a digit nor match a [keyword](#215-keywords) or
[keyword operator](#214-operators).


##### 2.1.8.1. Type names

Type names are identifiers with the additional constraint of not being any of
the [primitive type names](#216-primitive-type-names).


#### 2.1.9. String literals

Strings are delimited by double quotes `"`. After encountering one, the context
switch to the string context.


### 2.2. String context


#### 2.2.1. Escape sequences

Certain characters can be preceded by a backslash `\` to remove/give them a
special meaning:

Escape  |Expansion
--------|-----------------------------------------
`\\`    |`\`
`\"`    |`"`
`\{`    |`{`
`\n`    |A newline (ASCII character 10/LF)
`\t`    |A tabulation (ASCII character 9/TAB)
`\r`    |A carriage return (ASCII character 13/CR)

Any other character cannot be escaped.


#### 2.2.2. Formatting

An opening brace `{` mark the beginning of a formatting field. A field is made
of a value and formatting options. The three types of values are decribed in the
next sections.

The value may be an integer, an identifier, or an expression bewteen
parentheses. These expressions are read using the main context. 

The options can be a single interrogation mark `?`, two interrogation marks 
`??`, or nothing.


#### 2.2.3. End of string

Double quotes `"` mark the end of a string literal, switching back to the main
context.


#### 2.2.4. Text

Any other character is treated as string content.


## 3. Types


### 3.1. Primitive types


#### 3.1.1. Void

The `Void` type is the unit type and represents the absence of data. The only
value it can take is the [`null`](#411-null) constant.

There cannot be `Void` bindings, and it can't be used within most composite
types.


#### 3.1.2. Booleans

The `Bool` type can take only two values, the constants
[`true`](#412-boolean-constants) and [`false`](#412-boolean-constants).


#### 3.1.3. Integers

The `Int` type is a 32-bit signed integer.


#### 3.1.4. Floating-point numbers

The `Float` type is a double precision (64 bits) floating-point number.


#### 3.1.5. Strings

The `Str` type is a string of unicode characters.

A string is iterable with items of type `Str`, and indexable by
[`Int`](#313-integers) with items also of type `Str`.

Single characters are represented by strings of length 1.


#### 3.1.6. Files

The `File` type represents a text stream. It may be one or both of readable and
writeable.


#### 3.1.7. Signals

The `Signal` type represents an error. See [the dedicated section](#8-signals)
for more information.


### 3.2. Composite types

Composite types are built using primitive type or other composite types.


#### 3.2.1. Nullable types

```{ .ebnf title="Syntax" }
nullable type = type, "?";
```

A nullable type `T?` can hold values of type `T` and `null`.

`T` cannot be [`Void`](#311-void) or another nullable type.


#### 3.2.2. Lists

```{ .ebnf title="Syntax" }
list type = "[", type, "]";
```

A list type `[T]` is a dynamic collection of `T`.

`T` cannot be [`Void`](#311-void), and all the values should all have the same
type, or be able to be converted into a single type through
[implicit conversion](#34-implicit-conversion).

A list `[T]` is iterable with items of type `T`, and indexable by `int` with
items also of type `T`.

#### 3.2.3. Dictionaries

```{ .ebnf title="Syntax" }
dict type = "[", type, ":", type "]";
```

A dictionary type `[T: U]` is a mapping of `T` values to `U` values.

`T` and `U` cannot be [`Void`](#311-void), and `T` must be hashable (that is,
accepted by the [`hash`]() function).

The types of the keys must be the same (or beign compatible for
[implicit conversion](#34-implicit-conversion) like in lists) and the types of
the values as well.

A dictionary `[T: U]` is iterable with items of type `T`, and indexable by `T`
with items of type `U`.

#### 3.2.4. Tuples

```{ .ebnf title="Syntax" }
tuple type = "(", [ type, { ",", type } [ "," ] ] ")";
```

A tuple type `(T1, T2, ...)` is a group of different types.

Tuple fields cannot be [`Void`](#311-void), and a tuple with zero fields is
illegal. A tuple with only one field is the same as the type of its field.


#### 3.2.5. Function types

```{ .ebnf title="Syntax" }
function type = type, "->", type;
```

A function type `T -> R` is the type of a function that takes an argument of
type `T` and return a value of type `R`. A function type `(T1, T2, ...) -> R` is
the type of a function that takes zero, one or more arguments of type `T1`,
`T2`, ... and return a value of type `R`.


### 3.3. User-defined types


#### 3.3.1. Enumerations

Enumerations are primitive types that can take a specific list of values.


#### 3.3.2. Structures

Structures are groups of types like tuples, except that their fields are named. 


### 3.4. Never type

An expression that will only throw a signal have the never type, represented
`!` (for displaying purposes only, it is not valid syntax).

It is different from the unit type because it represents the absence of a
value, whereas [`Void`](#311-void) has one and only one value.


### 3.5. Implicit conversion

If a value can be of type `T` or [`Void`](#311-void), then its type will be
`T?`.

If a value can be of type [`Int`](#313-integers) or
[`Float`](#314-floating-point-numbers), then its type will be
[`Float`](#314-floating-point-numbers).

If an [`Int`](#313-integers) value is found where a
[`Float`](#314-floating-point-numbers) value was expected, it is also converted
to [`Float`](#314-floating-point-numbers) implicitly.

The never type `!` can be implictly converted into any other type.

A mutable type can be used where the immutable version of the same type is 
expected. 

Whenever several expressions are required to have the same type, it is valid if
different types that be converted implicitly into a single type are given. 


### 3.6. Type inference

The type of a binding, if omitted, is deduced from the value it is assigned,
and the types of function parameters are generic by default. A generic function
parameter can take any type that follows the [constraints](#37-type-constraints)
and is valid within the function.


#### 3.6.1. Partial types

Sometimes, the exact type of an expression is unknown, and in that case the
types that cannot be determined should represented as `~` (for displaying
purposes only like the `!` type).

For example, an empty list could be a list or dictionary of anything, and as
such its type will be `[~]`.

If a partial type is never resolved, the program is still valid because it means
that the actual type is not important.

### 3.7. Type constraints

Integers can be used where a type is expected, indicating a generic type. Two
generic types with the same number must then be resolved with the same type.


## 4. Expressions

Expressions are divided in three categories that defines their precedence: 

```{ .ebnf title="Syntax" }
primary expression = null
                   | boolean constant
                   | integer constant
                   | floating point constant
                   | string literal
                   | list literal
                   | dictionary literal
                   | tuple literal
                   | bound value
                   | black hole
                   | unary operation
                   | anonymous function;

secondary expression = field access
                     | item access
                     | function call
                     | primary expression;

expression = binary operation
           | secondary expression
           | if expression
           | for expression
           | while expression
           | try expression
           | function call
           | input output expression
           | block
           | block statements
           | flow control expressions;
```

Expressions in birdway are lazy, that is, they won't be evaluated until the
result is really needed.

### 4.1. Constant values

!!! note
    The types [`File`](#316-files) and [`Signal`](#317-signals) have no literal
    representation. They are created by or declared as built-ins.


#### 4.1.1. Null

The keyword `null` is the value of the unit type [`Void`](#311-void).


#### 4.1.2. Boolean constants

The keywords `true` and `false` are the two values of the
[`Bool`](#312-booleans) type.


#### 4.1.3. Integer constants

[Decimal](#2171-decimal-integer-literals),
[hexadecimal](#2171-hexadecimal-integer-literals) and
[binay](#2171-binary-integer-literals) integer literals evaluates to a value of
the [`Int`](#313-integers) type.


#### 4.1.4. Floating-point constants

[Floating-point literals](#2174-floating-point-literals) evaluates to a value of
the [[`Float`](#314-floating-point-numbers)](#314-floating-point-numbers) type.


#### 4.1.5. Strings

[String literals](#219-string-literals) evaluates to a value of the
[`Str`](#315-strings) type.

Formatting fields where the value is an integer will be left as-is to be
formatted later by [`fmt`](). Otherwise, if the value is an identifier, the
value bound to that identifier in the current scope will be used. Finally, if
the value is an expression, the result of this expression evaluated in the scope
of the string literal will be used.

No options means that [`to_string`]() will be used, and one or two interrogation
marks means that [`debug`]() will be used instead, with *inline* set to `true`
if a single `?` is used.

If the type of a binding or expression given to format is
incompatible with the formatting function, it should result in a type error.


### 4.2. Composite types literals

!!! note
    Nullable values are created through
    [implicit conversion](#34-implicit-conversion) and functions will be dealt
    with in [another section](#48-functions).


#### 4.2.1. List literals

```{ .ebnf title="Syntax" }
list literal = "[", [ expression, { ",", expression } [ "," ] ], "]";
```

List literals are values separated by commas and surrounded by square brackets.
A list containing `T` values will be of type `[T]` and an empty list will have
the partial type `[~]`.


#### 4.2.2. Dictionary literals

```{ .ebnf title="Syntax" }
key value = expression, ":", expression;

dict literal = "{", [ key value, { ",", key value } [ "," ] ], "}";
```

Dictionary literals are key-value pairs of the form `key: value` separated by
commas and surrounded by square brackets. A dictionary containing `T` keys and
`U` values will be of type `[T: U]`, and an empty dictionary will have the
partial type `[~: ~]`.


#### 4.2.3. Tuple literals

```{ .ebnf title="Syntax" }
tuple literal = "(", [ expression ], { ",", expression } [ "," ] ")";
```

List literals are values separated by commas and surrounded by parentheses. The
type of the tuple will be a [tuple type](#324-tuples) of the types of the
values.

A tuple cannot be empty, and a tuple with a single value will evaulate to that
value.


### 4.3. Bound values

The value of an identifier if the value bound to it via a `let` or `const`. 


### 4.4. Operations


#### 4.4.1. Unary operations

```{ .ebnf title="Syntax" }
unary operation = ( UNARY ONLY | UNARY OR BINARY ), primary expression;
```

Apply an unary operator to an expression.


#### 4.4.2. Binary operations

```{ .ebnf title="Syntax" }
unary operation = secondary expression,
                  ( UNARY OR BINARY | BINARY ONLY ),
                  expression;
```

Apply a binary operator to two expressions.

!!! note "See also"
    [The list of operators](#214-operators) and
    [their behavior](#5-operators)


#### 4.4.3. Field access

```{ .ebnf title="Syntax" }
field access = secondary expression, (* value *)
               ".",
               ( identifier | DECIMAL INTEGER ); (* field *)
```

If the value is a [`struct`](#332-structures), the field must be an identifier
and it will evaluate to the value of the corresponding struct field.

If the value is a [`tuple`](#324-tuples), the field must be an integer and it
will evaluate to the value of the tuple field at that index.

If the tuple or struct is mutable, then the field accessed is mutable too.

A field access is impossible with any other type. 


#### 4.4.4. Item access

```{ .ebnf title="Syntax" }
item access = secondary expression, (* value *)
              "[",
              expression, (* index *)
              "]";
```

Get the item at the specified index. The type of the value must be indexable by
the type of the index.

If the collection is mutable, then the item accessed is mutable too.


### 4.5. If-then-else

```{ .ebnf title="Syntax" }
if expression = "if", expression, (* condition *)
                "then", expression, (* result *)
                [ "else", expression ]; (* alternative *)
```

If the condition is true, evaluates to the result, and othwerwise to the
alternative. If the `else ...` part is missing, it evaluates to `null` in case
the condition is `false`.

The condition must be of type [`Bool`](#312-booleans), and the result and the
alternative must have the same type.


### 4.6. Loops


#### 4.6.1. For loops

```{ .ebnf title="Syntax" }
for expression = "for", ( declaration | "_" ), (* item *)
                 "in", expression, (* collection *)
                 "do", expression; (* expression *)
```

Evaluates to a list of expressions evaluated with the item taking each value
of the collection. The item is mutable if and only if the collection is mutable.

If the item is a single undercore `_`, the values inside the collection are
ignored and the loop just repeats the same expression for the length of the
collection.  

The collection must be iterable by the type of the variable. An iterable of any
type can be used with `_` as the item.

In case the expressions are of type [`Void`](#311-void), the loop just evaluates
to [`null`](#411-null).

If a break signal is caught, the loop stops and return the list of expressions
evaluated so far. If a continue signal is caught, the loop continues its
execution and ignore one of the expressions.


#### 4.6.2. While loops

```{ .ebnf title="Syntax" }
while expression = "while", expression, (* condition *)
                   "do", expression; (* expression *)
```

Evaluates to a list of expressions evaluated repeatedly while the condition is
`true`.

The condition must be of type [`Bool`](#312-booleans). 

In case the expressions are of type [`Void`](#311-void), the loop just evaluates
to [`null`](#411-null).

The break and continue signals are handled the same way as the for loop does.


### 4.7. Error handling

```{ .ebnf title="Syntax" }
try expression = "try", expression, (* expression *)
                 {
                    "catch", expression, (* signal *)
                    "do", expression (* handler *) 
                 },
                 [ "finally", expression ]; (* cleanup *)
```

Evaluates to the expression, but if an error is thrown and matches one of the
handled signals, then evaluates to the corresponding handler. After that, the
cleanup expression is evaluated (if present) and its value discarded.

The expression and the handlers must all have the same type. The signals
must be of type [`Signal`](#317-signals) and the cleanup of type
[`Void`](#311-void).


### 4.8. Functions


#### 4.8.1. Calling functions

```{ .ebnf title="Syntax" }
function call = secondary expression, "(",
                [ expression, { ",", expression }, [ "," ] ],
                ")";
```

Evaluate the body of a function with the given arguments.

If a return signal is caught, the function return immediately.


##### 4.8.1.1. Overload resolution

If a function is overloaded, the implementation that will be called is the one
wich match the number and the types of the arguments.

If a function has multiple overloads that accept the number and types of the
arguments, the least generic one (i.e. the one with the least generic
parameters) is chosen.


#### 4.8.2. Anonymous functions

```{ .ebnf title="Syntax" }
anonymous function = ( "(", 
                       [ IDENTIFIER, { ",", IDENTIFIER }, [ "," ] ],
                       ")"
                     | IDENTIFIER
                     ),
                     "->", expression; (* body *)
```

Creates an anonymous function with the specified parameters and body.


##### 4.8.2.1. Closures

When an anonymous function is evaluated, it is given a closure containing all
the local bindings used by the function. All bindings are captured by value the
moment it is evaluated.


### 4.9. I/O


#### 4.9.1. Output

```{ .ebnf title="Syntax" }
print expression = ( "print" | "println" ), expression, (* content *)
                   [ "to", expression ]; (* stream *)
```

Writes the content formatted using [`to_string`]() to the stream. If no stream
is specified, it defaults to the standard output.

If `println` is used, a newline is written after the content. 

The content must be a string or a valid argument to pass to [`to_string`](). The
stream must be of type [`File`](#316-files) and writeable. It always evaluates
to [`null`](#411-null).


#### 4.9.2. Input

```{ .ebnf title="Syntax" }
read expression = ( "read", [ expression (* limit *) ] | "readln" ),
                  [ "from", expression ]; (* stream *)
```

Reads the content of a stream and return it. If no stream is specified, it
defaults to the standard input.

If `read` is used, reads until the end of the stream, and if a limit is given,
reads at most that number of characters from the stream. If `readln` is used
instead, reads until a newline is encountered. The newline is read from the
stream and discarded.

The limit must be of type [`Int`](#313-integers) and the stream of type
[`File`](#316-files) and readable. The result is always a [`Str`](#315-strings).


### 4.10. Blocks

```{ .ebnf title="Syntax" }
block = "{",
        { expression | block statement, ";" },
        [ expression (* tail *) ],
        "}"; 
```

Evaluates each expression after another. The value of the block is the value of
the tail expression, if there is one, or [`null`](#411-null) otherwise.


### 4.11. The black hole

A single undercore `_` is the *"black hole"*. It acts like a binding, except its
type is `$Void`. It should behave like `null` under most circumstances.

!!! note "See also"
    [The assignment operator](#547-assignment)


#### 4.12. Flow control

The type of all these expressions is the [never type](#34-never-type).


##### 4.12.1. Continue

```{ .ebnf title="Syntax" }
continue expression = "continue";
```

Throws a *continue* signal. It can only be used inside of a loop.


##### 4.12.2. Break

```{ .ebnf title="Syntax" }
break expression = "break";
```

Throws a *break* signal. It can only be used inside of a loop.


##### 4.12.3. Return

```{ .ebnf title="Syntax" }
return expression = "return", [ expression (* return value *) ];
```

Sets the value of the expression as the return value of the function it is
inside of and throws a *return* signal. It can only be used inside of a
function.

If no return value is specified, then [`null`](#411-null) is returned.


##### 4.12.3. Throw

```{ .ebnf title="Syntax" }
throw expression = "throw", expression, (* signal *);
```

Throws an error signal.

The signal must be of type `Signal`.


## 5. Operators


### 5.1. Arithmetic operators


#### 5.1.2. Substraction

The `-` binary operator substract a number to another.

The types are the same as for the addition.


#### 5.1.1. Addition

The `+` binary operator adds two numbers.

Left operand    |Right operand   |Result
----------------|----------------|---------
`Int`           |`Int`           |`Int`
`Int`           |`Float`         |`Float`
`Float`         |`Int`           |`Float`
`Float`         |`Float`         |`Float`
*Any other type*|*Any other type*|*Invalid* 


#### 5.1.2. Substraction

The `-` binary operator substract a number to another.

The types are the same as for the addition.


#### 5.1.3. Multiplication

The `*` binary operator multiplies two numbers.

The types are the same as for the addition.


#### 5.1.4. Division

The `/` binary operator divide a number by another.

Left operand    |Right operand   |Result
----------------|----------------|---------
`Int`           |`Int`           |`Float`
`Int`           |`Float`         |`Float`
`Float`         |`Int`           |`Float`
`Float`         |`Float`         |`Float`
*Any other type*|*Any other type*|*Invalid*


#### 5.1.5. Integer division

The `//` binary operator gives the quotient of the division of two numbers. The
division is floored if the divider is positive, and ceilinged if it is negative.

Left operand    |Right operand   |Result
----------------|----------------|---------
`Int`           |`Int`           |`Int`
*Any other type*|*Any other type*|*Invalid*


#### 5.1.6. Modulo

The `%` binary operator gives the remainder of the division of two numbers. The
division is floored if the divider is positive, and ceilinged if it is negative.

The types are the same as for the integer division.


### 5.2. Comparison operators


#### 5.2.1. Equal

The `==` binary operator tests two values for equality.

* `null` values are always equal to themselves.
* Integers and floats are equal if they represent the exact same number.
* Strings are equal if they contain the same characters.
* Enumeration values and signals are equal if they are the same constant.
* Lists are equal if all their elements are equal.
* Dictionaries are equal if they contain the same key-value pairs.
* Tuples and structs are equal if each of their fields are equal.

The two operands must have the same type, and that type can't be `File` or any
composite type containing `File`.


#### 5.2.2. Not equal

The `!=` binary operator tests two values for inequality. It is the negation of
the equal operator. 


#### 5.2.3. Less than

The `<` binary operator tests if a value is strictly less than another.

Left operand    |Right operand   |Result
----------------|----------------|---------
`Int`           |`Int`           |`Bool`
`Int`           |`Float`         |`Bool`
`Float`         |`Int`           |`Bool`
`Float`         |`Float`         |`Bool`
*Any other type*|*Any other type*|*Invalid*


#### 5.2.4. Greater than

The `>` binary operator tests if a value is strictly greater than another.

The types are the same as for the less than operator.


#### 5.2.5. Less or equal

The `<=` binary operator tests if a value is less then or equal to another.

The types are the same as for the less than operator.


#### 5.2.6. Greater or equal

The `>=` binary operator tests if a value is greater then or equal to another.

The types are the same as for the less than operator.


### 5.3. Logical operators


#### 5.3.1. Logical NOT

The `not` unary operator negates a boolean value.

Operand         |Result
----------------|---------
`Bool`          |`Bool`
*Any other type*|*Invalid*


#### 5.3.2. Logical OR

The `or` binary operator is the logical *or* of two booleans. 

Left operand    |Right operand   |Result
----------------|----------------|---------
`Bool`          |`Bool`          |`Bool`
*Any other type*|*Any other type*|*Invalid*


#### 5.3.3. Logical AND

The `or` binary operator is the logical *and* of two booleans. 

The types are the same as for the logical *or* operator.


### 5.4. Other operators


#### 5.4.1. Size

The `#` unary operator gives the size of a collection.

Operand         |Result
----------------|---------
`Str`           |`Int`
`[T]`           |`Int`
`[T: U]`        |`Int`
*Any other type*|*Invalid*


#### 5.4.2. Concatenation

The `&` binary operator concatenates two collections of the same type.

Left operand    |Right operand   |Result
----------------|----------------|---------
`Str`           |`Str`           |`Str`
`[T]`           |`[T]`           |`[T]`
*Any other type*|*Any other type*|*Invalid*


#### 5.4.3. Prepending

The `>>` binary operator prepends a value to a list.

Left operand    |Right operand   |Result
----------------|----------------|---------
`T`             |`[T]`           |`[T]`
*Any other type*|*Any other type*|*Invalid*


#### 5.4.4. Appending

The `<<` binary operator appends a value to a list.

Left operand    |Right operand   |Result
----------------|----------------|---------
`[T]`           |`T`             |`[T]`
*Any other type*|*Any other type*|*Invalid*


#### 5.4.5. Union

The `|` binary operator gives the union of two dictionaries, the values of the
right-hand side overriding the values of the left-hand side.

Left operand    |Right operand   |Result
----------------|----------------|---------
`[T: U]`        |`[T: U]`        |`[T: U]`
*Any other type*|*Any other type*|*Invalid*


#### 5.4.6. Isn't null

The `?` unary operator tests if a nullable value is not [`null`](#411-null).

Operand         |Result
----------------|---------
`T?`            |`Bool`
*Any other type*|*Invalid*


#### 5.4.7. Assignment

The `:=` binary operator assign the value on the right-hand side to the variable
on the left-hand side, and evaluates to that value.

Left operand    |Right operand   |Result
----------------|----------------|---------
`$T`            |`T`             |`T`

If the expression assigned has not been computed yet because of laziness, it
gets computed before being assigned.

Any value can be assigned to the black hole binding, in wich case that value is
discarded and the assignment evaluates to `null`.


## 6. Statements


### 6.1. Unit-level statements

These statements can only be used directly in the body of the program. A unit is
made of zero or more of these statements, terminated by semicolons `;`.


#### 6.1.1. Use statement

```{ .ebnf title="Syntax" }
use statement = "use", IDENTIFIER;
```

Import another unit as a module from the file in the same directory as the
source, with the given name and a `.bw` extension.


#### 6.1.2. Type declarations


##### 6.1.2.1. Enumeration declarations

```{ .ebnf title="Syntax" }
enum declaration = "enum", TYPE NAME, "(",
                   [ IDENTIFIER, { ",", IDENTIFIER }, [ "," ], (* values *) ],
                   ")"; 
```

Declare an enum type that can take one of the values. All values are declared as
constants, and there must be at least one.


##### 6.1.2.2. Structure declarations

```{ .ebnf title="Syntax" }
struct field = IDENTIFIER, ":", type;

struct declaration = "struct", TYPE NAME, "(",
                     [ struct field, { ",", struct field }, [ "," ] ],
                     ")"; 
```

Declare a struct with the given fields. All the types must be non-generic,
complete types (i.e. not partial). There must be at least one field.

#### 6.1.3. Command-line arguments

```{ .ebnf title="Syntax" }
program parameter = IDENTIFIER, ":", type;

params declaration = "params", "(",
                     [ program parameter, { ",", program parameter }, [ "," ] ],
                     ")";
```

Declare command-line parameters. The following types can be used:

* `Str` will accept any value and return the argument as is.
* `Int` will accept only integers in the form [`to_int`]() expects.


#### 6.1.4. Constant declarations

```{ .ebnf title="Syntax" }
declaration = IDENTIFIER, [ ":", type ];

constant declaration = "const", declaration, "=", expression; 
```

Binds a value to a name, ensuring the expression is evaluated at compile time.

Constants are not captured by closures because of their static nature.


#### 6.1.5. Function declarations

```{ .ebnf title="Syntax" }
function parameter = [ "$" | "@" ], declaration;

function parameters = "(", [
                        function parameter,
                        { ",", function parameter },
                        [ "," ]
                      ], ")";

function delcaration = "func", IDENTIFIER, function parameters,
                       [ type ] (* return type *) "->", expression; (* body *)
```

Declares a function with a given name and parameters, and returning the body
when called.

By default, all arguments are passed by copy. They may actually be passed by
reference for optimisation reasons, but since they aren't mutable, it should
behave the same way.

When a parameter is preceded by a `$` modifier, arguments will be passed to it
by mutable reference, and as such, they must be mutable bindings.

When a parameter is preceded by a `@` modifier, arguments are still passed to it
by copy, but the binding inside the function is mutable.

If the return type is specified, the type of the body must be the same.
Otherwise, the return type of the function is inferred from the type of the
body.

Functions may be overloaded, that is, a function may have different
implementations with different parameters. 


### 6.2. Block-level statement

These statements can only be used inside [blocks](#410-blocks).


#### 6.2.1. Constants and functions

Constants and functions can also be declared inside blocks, just like in the
program body. The difference is that functions will have a closure like
anonymous functions do.


#### 6.2.2. Bindings

```{ .ebnf title="Syntax" }
binding = "let", [ "$" ], declaration, "=", value;
```

Binds a value to a name, but unlike constants, the value may be evaluated at
runtime.

The `$` modifier indicates that the binding is mutable. If the expression
assigned has not been computed yet because of laziness, it gets computed before
being assigned.


## 7. Scope and modules


### 7.1. Scope of constants and bindings

Functions, constants and binding are available in the scope they're declared in.

For constants and functions declared in the body of the program, they are
avaliable through the entire unit.

If they are declared inside block instead, they are available from their
declaration to the end of the block.

Functions have access to themselves inside their bodies to allow for recursion.
Constants and bindings do not.


#### 7.1.1. Shadowing

A declaration can shadow (i.e. have the same name as) another if they are not in
the same block.

A bindigs thus refers to the last one declared.


### 7.2. Module exports

When a module is imported, the declarations in its body (including the
declarations imported from another unit) are brought into the global scope of
the unit importing it.


## 8. Signals

When a signal is thrown, it interrupts the execution of the preogram and
propagate down the stack until it is caught. If it is not caught, the program
terminates.


### 8.1. Internal signals

Three signals should be available for interal use: a break signal, a continue
signal and a return signal. They can only be thrown using special statements,
and should always be caught (otherwise, it would mean that a `break` was outside
of a loop, for example).


### 8.2. Error signals

Other signal can be thrown and caught by the user, and occur anywhere in the
program. They are defined as [built-in constants](#106-signals). They may never
be caught and terminate the program.


## 9. Built-ins

Built-ins are functions and constants that are defined in any unit, and that may
be shadowed by user declarations, including inside the body. They should be
implemented by the compiler. 


### 9.1. Input/Output

`func open(path: Str) File`  
`func open(path: Str, mode: FileMode) File`

> Open the file at the specified path.
>
> **Parameters**
>
> <dl>
    <dt>`path`<dt>
    <dd>The path of the file, absolute or relative to the CWD.</dd>
    <dt>`mode`</dt>
    <dd>The mode to open the file with.</dd>
    </dl>
>
> **Returns**
>
> The opened file.
>
> **Throws**
>
> <dl>
    <dt>`ERR_NOTFOUND`</dt>
    <dd>If the file does not exists.</dd>
    <dt>`ERR_PERM`</dt>
    <dd>
      If the user doesn't have the permission to open the file with the
      specified mode.
    </dd>
    <dt>`ERR_NOTAFILE`</dt>
    <dd>If the path given points to a directory.</dd>
    </dl>

`enum FileMode (READ_ONLY, WRITE_ONLY, READ_WRITE)`

> File opening modes.

`func close($file: File) Void`

> Closes an opened file.
>
> **Parameters**
>
> <dl>
    <dt>`file`<dt>
    <dd>The file to close.</dd>
    </dl>
>
> **Throws**
>
> <dl>
    <dt>`ERR_VALUE`<dt>
    <dd>If the file was already closed.</dd>
    </dl>

### 9.2. Conversions

`func to_int(value: Bool) Int`  
`func to_int(value: Float) Int`  
`func to_int(value: String) Int?`

> If the value is a `Bool`, then `false` is mapped to `0` and `true` to `1`.
> 
> If the value is a `Float`, it gets truncated (i.e. rounded towards zero).
>
> If the value is a `Str`, it will be parsed as a decimal integer.
>
> **Parameters**
>
> <dl>
    <dt>`value`<dt>
    <dd>The value to convert.</dd>
    </dl>
>
> **Returns**
>
> The value converted to an integer, or `null` if the conversion fails.

`func to_float(value: Bool) Float`  
`func to_float(value: Int) Float`  
`func to_float(value: String) Float?`

> If the value is a `Bool`, then `false` is mapped to `0.0` and `true` to `1.0`.
>
> If the value is a `Str`, it will be parsed as a floating-point number.
>
> **Parameters**
>
> <dl>
    <dt>`value`<dt>
    <dd>The value to convert.</dd>
    </dl>
>
> **Returns**
>
> The value converted to a float, or `null` if the conversion fails.

`func to_string(value: Int) Str`  
`func to_string(value: Float) Str`

> Converts a number to its decimal representation.
>
> **Parameters**
>
> <dl>
    <dt>`value`<dt>
    <dd>The value to convert.</dd>
    </dl>
>
> **Returns**
>
> The value converted to a string.

`func debug(value: 1) Str`  
`func debug(value, inline: Bool) Str`

> Convert any value to its literal representation, or, in case it has no literal
> form, to a representation giving enough information to recreate the value. 
>
> **Parameters**
>
> <dl>
    <dt>`value`<dt>
    <dd>The value to convert.</dd>
    <dt>`inline`<dt>
    <dd>
        If set to `true`, the value is displayed on one line.
        Otherwise, the representation may use multiple lines to be more
        readable. Defaults to `true`.
    </dd>
    </dl>
>
> **Returns**
>
> The value converted to a string.

`func to_hex(value: Int) Str`

> Convert an integer to its hexadecimal representation. 
>
> **Parameters**
>
> <dl>
    <dt>`value`<dt>
    <dd>The value to convert.</dd>
    </dl>
>
> **Returns**
>
> The value converted to a string.

`func to_bin(value: Int) Str`

> Convert an integer to its binary representation. 
>
> **Parameters**
>
> <dl>
    <dt>`value`<dt>
    <dd>The value to convert.</dd>
    </dl>
>
> **Returns**
>
> The value converted to a string.


### 9.3. Operations on nullable values

`func unwrap(maybe: 1?) 1`

> Return the inner value of *maybe*, or throws an `ERR_NULL` if it was `null`.
>
> **Parameters**
>
> <dl>
    <dt>`maybe`<dt>
    <dd>A nullable value.</dd>
    </dl>
>
> **Returns**
>
> The inner value.
>
> **Throws**
>
> <dl>
    <dt>`ERR_NULL`<dt>
    <dd>If *maybe* was `null`.</dd>
    </dl>

`func default(maybe: 1?, default: 1) 1`

> Return the inner value of *maybe*, or *default* it was `null`.
>
> **Parameters**
>
> <dl>
    <dt>`maybe`<dt>
    <dd>A nullable value.</dd>
    </dl>
>
> **Returns**
>
> The inner value or *default*.

`func then(maybe: 1?, f: 1 -> 2) 2?`

> Return `null` if *maybe* is `null`, or the image of *maybe* by *f*.
>
> **Parameters**
>
> <dl>
    <dt>`maybe`<dt>
    <dd>A nullable value.</dd>
    <dt>`f`<dt>
    <dd>The mapping function.</dd>
    </dl>
>
> **Returns**
>
> A new nullable value.

`func expect(maybe: 1?, err: Signal) 1`

> Return the inner value of *maybe*, or throws *err* if it was `null`.
>
> **Parameters**
>
> <dl>
    <dt>`maybe`<dt>
    <dd>A nullable value.</dd>
    <dt>`err`<dt>
    <dd>An error to throw if *maybe* is `null`.</dd>
    </dl>
>
> **Returns**
>
> The inner value.
>
> **Throws**
>
> <dl>
    <dt>*err*<dt>
    <dd>If *maybe* was `null`.</dd>
    </dl>


### 9.4. Signals

`const SUCCESS: Signal = ....`

> Stop the program with success.
>
> *Exit code 0*

`const ERR_VALUE: Signal = ....`

> A value was not valid.
>
> *Exit code 70*

`const ERR_NULL: Signal = ....`

> A nullable value was `null`.
>
> *Exit code 70*

`const ERR_MATH: Signal = ....`

> A mathematical operation was not valid (e.g. division by zero) 
>
> *Exit code 70*

`const ERR_RANGE: Signal = ....`

> A numeric value overflowed.
>
> *Exit code 70*

`const ERR_OS: Signal = ....`

> Generic OS error.
>
> *Exit code 71*

`const ERR_IO: Signal = ....`

> I/O error.
>
> *Exit code 74*

`const ERR_NOTFOUND: Signal = ....`

> A file didn't exists.
>
> *Exit code 71*

`const ERR_PERM: Signal = ....`

> The user didn't have the permission to perform an operation.
>
> *Exit code 77*

`const ERR_NOTAFILE: Signal = ....`

> A path pointed to a directory when a file was expected.
>
> *Exit code 71*

`const ERR_NOTADIR: Signal = ....`

> A path pointed to a file when a directory was expected.
>
> *Exit code 71*

`const ERR_EXISTS: Signal = ....`

> A file already existed.
>
> *Exit code 71*

`const ERR_LOOKUP: Signal = ....`

> An [item access](#444-item-access) failed.
>
> *Exit code 70*

`const ERR_FORMAT: Signal = ....`

> A value was not in the correct format.
>
> *Exit code 65*

`const ERR_USERINT: Signal = ....`

> Thrown when the user interrupts the program with Ctrl+C.
>
> *Exit code 130*

`const ERR_MEMORY: Signal = ....`

> An error ocurred when trying to allocate dynamic memory.
>
> *Exit code 70*

`const ERR_APP: Signal = ....`

> Application-specific error.
>
> *Exit code 80*

`const FAIL: Signal = ....`

> Generic error.
>
> *Exit code 1*
