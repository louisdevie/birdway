# Predefinitions

Birdway *predefinitions* are functions and constants implemented by the compiler.



## Constants (math)

### `PI: Float = 3.141592653589793`

An approxiamtion of π.



## Constants (I/O)

### `READ: Byte = 'b_0000_0001`

Read mode flag.

### `WRITE: Byte = 'b_0000_0010`

Write mode flag.

### `CREATE: Byte = 'b_0000_0100`

Create mode flag.

### `APPEND: Byte = 'b_0000_1010`

Append mode flag.

### `BINARY: Byte = 'b_0001_0000`

Binary mode flag.



## Functions (math)

### `abs(x: Int) -> Int`
### `abs(x: Float) -> Float`

Returns the absolute value of *x*.

### `sqrt(x: Float) -> Float`

Returns the square root of *x*.

### `root(x: Float, i: Float) -> Float`

Returns the *i*-th root of *x*.

### `cos(ang: Float) -> Float`
### `sin(ang: Float) -> Float`
### `tan(ang: Float) -> Float`
### `acos(cos: Float) -> Float`
### `asin(sin: Float) -> Float`
### `atan(tan: Float) -> Float`

Trigonometry functions, with the angles in radians.

### `ln(x: Float) -> Float`

Returns the natural logarithm of *x*.

### `log(x: Float, b: Float) -> Float`

Returns the base *b* logarithm of *x*.

### `exp(x: Float) -> Float`

The exponential function (e^*x*).

### `pow(x: Float, p: Float) -> Float`

Returns *x* to the power of *p*.

### `round(x: Float) -> Int`
### `round(x: Int|Float, r: Int) -> Int`
### `round(x: Int|Float, r: Float) -> Float`

Round *x* to the nearest integer, or the nearest multiple of *r* if given.

### `floor(x: Float) -> Int`
### `floor(x: Int|Float, r: Int) -> Int`
### `floor(x: Int|Float, r: Float) -> Float`

Round *x* to the nearest integer (or the nearest multiple of *r* if given) **less** than *x*.

### `ceil(x: Float) -> Int`
### `ceil(x: Int|Float, r: Int) -> Int`
### `ceil(x: Int|Float, r: Float) -> Float`

Round *x* to the nearest integer (or the nearest multiple of *r* if given) **greater** than *x*.

### `almost_eq(a: Float, b: Float, prec: Int) -> Bool`

Test *a* and *b* for equality with *prec* significant digits.

Example: `eq(3.14, PI, 3)` returns `TRUE`

### `idiv(a: Int, b: Int) -> (Int, Int)?`

Returns the quotient and the remainder of *a* divided by *b*,
or `NULL` if *b* = 0.

### `fdiv(a: Float, b: Float) -> Float?`

Returns *a* divided by *b*, or `NULL` if *b* = 0.



## Functions (collections)

### `enumerate(a: Str) -> [(Int, Str)]`
### `enumerate(a: [0]) -> [(Int, 0)]`

Returns each element of *a* with its index.

The equivalent for dictionaries is `entries`.

### `reverse(a: Str) -> Str`
### `reverse(a: [0]) -> [0]`

Iterate from the end to the start.

### `zip(a: Str, b: Str) -> [(Str, Str)]`
### `zip(a: [0], b: [1]) -> [(0, 1)]`

Iterate through multiple collections at once, stopping at the end of the shortest one.

### `zip_max(a: Str, b: Str) -> [(Str?, Str?)]`
### `zip_max(a: [0], b: [1]) -> [(0?, 1?)]`

Iterate through multiple collections at once, stopping at the end of the longest one.
If some collections stop before others, `NULL` will be used as a default value.

### `foldl(a: [0], f: (0, 0) -> 0) -> 0`
### `foldr(a: [0], f: (0, 0) -> 0) -> 0`

Reduce a list to a single value.

### `map(a: [0], f: 0 -> 2) -> [2]`
### `map(a: [1: 0], f: 0 -> 2) -> [1: 2]`

Maps the elements from *a* to their image by *f*.

### `filter(a: [0], f: 0 -> Bool) -> [0]`
### `filter(a: [1: 0], f: 0 -> Bool) -> [1: 0]`

Removes the elements from *a* for wich `f(item)` is `TRUE`.

### `fill(len: Int, val: 0) -> [0]`

Creates a list of length *len* filled with *val*.

### `map_key(a: [0], f: (Int, 0) -> 2) -> [0]`
### `map_key(a: [1: 0], f: (1, 0) -> 2) -> [1: 2]`

Same as `map`, but the indexes / keys are passed to the mapping function

### `filter_key(a: [0], f: (Int, 0) -> Bool) -> [0]`
### `filter_key(a: [1: 0], f: (1, 0) -> Bool) -> [1: 0]`

Same as `filter`, but the indexes / keys are passed to the filtering function

### `fill_key(len: Int, f: Int -> 0) -> [0]`

Creates a list of length *len* where an element at index i is f(i).

### `values(dict: [1: 0]) -> [0]`

Iterate through the values of *dict*.

### `entries(dict: [1: 0]) -> [(1, 0)]`

Iterate through the key-value pairs of *dict*.

### `sum(list: [Int]) -> Int`
### `sum(list: [Float]) -> Float`

Returns the sum of the values of *list*. 

### `min(list: [Int]) -> Int`
### `min(list: [Float]) -> Float`

Returns the smallest value in *list*.

### `max(list: [Int]) -> Int`
### `max(list: [Float]) -> Float`

Returns the greatest value in *list*.

### `any(list: [Bool]) -> Bool`

Returns `TRUE` if any value in *list* is `TRUE`, `FALSE` otherwise.

### `all(list: [Bool]) -> Bool`

Returns `TRUE` if all the values in *list* are `TRUE`, `FALSE` otherwise.

### `next(val: E) -> E?`

Returns the value after *val* in the enumeration *E*,
or `NULL` if *val* is the last value.

### `prev(val: E) -> E?`

Returns the value before *val* in the enumeration *E*,
or `NULL` if *val* is the first value.

### `loop_next(val: E) -> E`

Returns the value after *val* in the enumeration *E*,
or the first value if *val* is the last one.

### `loop_prev(val: E) -> E`

Returns the value before *val* in the enumeration *E*,
or the last value if *val* is the first one.

### `ord(a: Str|E) -> Int`

Returns the code of a character
or the position of a value in an enumeration.

## Functions (conversion)

### `to_int(val: Bool) -> Int`

Maps `FALSE` to `0` and `TRUE` to `1`.

### `to_int(val: Str) -> Int?`

Scan the string for an integer literal.
If it is not a valid integer, `NULL` is returned.

Use `round`, `floor` or `ceil` to convert a `Float` into an `Int`.

### `to_float(val: Bool) -> Int`

Maps `FALSE` to `0.0` and `TRUE` to `1.0`.

### `to_float(val: Str) -> Int?`

Scan the string for a float literal.
If it is not a valid decimal number, `NULL` is returned.

### `to_byte(val: Bool) -> Byte`

Maps `FALSE` to `'0` and `TRUE` to `'1`.

### `to_byte(val: Int) -> Byte?`

Converts *val* to the equivalent `Byte` if 0 ≤ *val* < 256.
`NULL` is returned if *val* is outside the range.

### `to_bool(val: 0) -> Bool`

Converts anything into a boolean.

`NULL`, `'0`, `0`, `0.0`, `""`, `[]`, and a closed `File` are all converted to `FALSE`.
Anything else than that is converted to `TRUE`.

Can be overloaded.

### `to_string(val: ~) -> Str`

Gives a representation of *val*, the same way `print val` does.

Can be overloaded.

### `bin(val: Byte|Int) -> Str`

Give the binary representation of *val*.

### `hex(val: Byte|Int) -> Str`

Give the hexadecimal representation of *val*.



## Functions (strings)

### `contains(text: Str, part: Str) -> Bool`

Returns wether *part* appears in *text*.

### `is_alpha(text: Str) -> Bool`
### `is_numeric(text: Str) -> Bool`
### `is_space(text: Str) -> Bool`

Return `TRUE` if *text* contains certain characters only.

### `trim(text: Str) -> Str`
### `triml(text: Str) -> Str`
### `trimr(text: Str) -> Str`

Removes spaces at the beginning and/or the end of a string.