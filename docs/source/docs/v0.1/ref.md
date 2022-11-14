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
`!=`, `>`, `>=`, `<`, `<=`, and the keywords `and` and `or`.


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

If the type of a binding or expression given to format is
incompatible with the formatting function, it should result in a type error.


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


#### 3.1.4. Integers

The `Int` type is a 32-bit signed integer. It thus can take values between
-2<sup>31</sup> (included) and 2<sup>31</sup> (excluded).


#### 3.1.5. Floating-point numbers

The `Float` type is a double precision (64 bits) floating-point number.


#### 3.1.6. Strings


#### 3.1.7. Files


#### 3.1.8. Signals


### 3.2. Composite types


#### 3.2.1. Nullable types


#### 3.2.2. Lists


#### 3.2.3. Dictionaries


#### 3.2.4. Tuples


#### 3.2.5. Function types


### 3.3. User-defined types


#### 3.3.1. Enumerations


#### 3.3.2. Structures


### 3.4. Implicit conversion


### 3.5. Type inference


### 3.5.1. Partial types


## 4. Expressions


### 4.1. Constant values


#### 4.1.1. Null

The keyword `null` is the value of the unit type [`Void`](#311-void).


#### 4.1.2. Boolean constants

The keywords `true` and `false` are the two values of the
[`Bool`](#312-booleans) type.


### 4.2. Composite types literals


#### 4.2.1. List literals


#### 4.2.2. Dictionary literals


#### 4.2.3. Tuple literals


#### 4.2.4. Structure literals


### 4.3. Bound values


#### 4.3.1. Constant bound values


### 4.4. Operations


#### 4.4.1. Unary operations


#### 4.4.2. Binary operations


#### 4.4.3. Field and module access


#### 4.4.4. Item access


#### 4.4.5. Operator precendence


### 4.5. If-then-else


### 4.6. Loops


#### 4.6.1. For loops


#### 4.6.2. While loops


### 4.7. Error handling


### 4.8. Functions


#### 4.8.1. Calling functions


##### 4.8.1.1. Overload resolution


#### 4.8.2. Anonymous functions


##### 4.8.2.1. Closures


### 4.9. I/O


### 4.10. Blocks


## 5. Operators


### 5.1. Arithmetic operators


#### 5.1.1. Addition


#### 5.1.2. Substraction


#### 5.1.3. Multiplication


#### 5.1.4. Division


#### 5.1.5. Integer division


#### 5.1.6. Modulo


### 5.2. Comparison operators


#### 5.2.1. Equal


#### 5.2.2. Not equal


#### 5.2.3. Less than


#### 5.2.4. Greater than


#### 5.2.5. Less or equal


#### 5.2.6. Greater or equal


### 5.3. Logical operators


#### 5.3.1. Logical NOT


#### 5.3.2. Logical OR


#### 5.3.3. Logical AND


### 5.4. Other operators


#### 5.4.1. Size


#### 5.4.2. Concatenation


#### 5.4.3. Union


#### 5.4.4. Isn't null


#### 5.4.5. Assignment


## 6. Statements


### 6.1. Unit-level statements


#### 6.1.1. Use statement


#### 6.1.2. Type declarations


##### 6.1.2.1. Enumeration declarations


##### 6.1.2.2. Structure declarations


#### 6.1.3. Command-line arguments


##### 6.1.3.1. Parameters


##### 6.1.3.2. Options and flags


#### 6.2.1. Constant declarations


#### 6.2.2. Function declarations


### 6.2. Block-level statement


#### 6.2.1. Constants and functions


#### 6.2.2. Bindings


##### 6.2.2.1. Mutable bindings


#### 6.2.3. Flow control


##### 6.2.3.1. Skip


##### 6.2.3.2. Break


##### 6.2.3.3. Return


##### 6.2.3.3. Throw


## 7. Modules and scope


### 7.1. Scope of constants and bindings


#### 7.1.1. Name resolution


### 7.2. Module exports


## 8. Signals


## 9. Built-ins


### 9.1. Input/Output


### 9.2. File Paths


### 9.3. Conversions


### 9.4. Mathematics


### 9.5. Operations on collections
