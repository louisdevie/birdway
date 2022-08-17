# Predefinitions

Birdway *predefinitions* are functions, constants and types implemented by the compiler.



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

### `Enum Alignment`

Text alignment.

Values :
```
CENTER
LEFT
RIGHT
JUSTIFY
```


## Functions (math)

### `abs(x: Int) -> Int`
### `abs(x: Float) -> Float`

Returns the absolute value of *x*.

### `sqrt(x: Int|Float) -> Float`

Returns the square root of *x*.

### `root(x: Int|Float, i: Int|Float) -> Float`

Returns the *i*-th root of *x*.  

### `cos(x: Int|Float) -> Float`
### `sin(x: Int|Float) -> Float`
### `tan(x: Int|Float) -> Float`
### `acos(x: Int|Float) -> Float`
### `asin(x: Int|Float) -> Float`
### `atan(x: Int|Float) -> Float`

Trigonometry functions.

### `log(x: Int|Float) -> Float`
### `log(x: Int|Float, b: Int|Float) -> Float`

Return the logarithm of *x* to base *b*, or the natural logarithm (base ⅇ) if no base is given.

### `exp(x: Int|Float) -> Float`

The exponential function.

### `round(x: Float) -> Int`
### `round(x: Int|Float, r: Int) -> Int`
### `round(x: Int|Float, r: Float) -> Float`

Round *x* to the nearest integer, or the nearest multiple of *r* if given.

### `floor(x: Float) -> Int`
### `floor(x: Int|Float, r: Int) -> Int`
### `floor(x: Int|Float, r: Float) -> Float`

Round *x* to the nearest integer (or the nearest multiple of *r* if given) **less** than *x*.

### `ceiling(x: Float) -> Int`
### `ceiling(x: Int|Float, r: Int) -> Int`
### `ceiling(x: Int|Float, r: Float) -> Float`

Round *x* to the nearest integer (or the nearest multiple of *r* if given) **greater** than *x*.

### `next_pow(n: Int, b: Int) -> Int`

Returns the smallest integer p such that *b*^p ≥ *n*.

Example: the number of digits needed to write N in decimal is `next_pow(N, 10)`

### `eq(a: Float, b: Float, prec: Int) -> Bool`

Test *a* and *b* for equality with *prec* significant digits.

Example: `eq(3.14, PI, 3)` returns `TRUE`

### `div(a: Int|Float, b: Int|Float) -> Float?`

Returns *a / b*, or `NULL` if *b* = 0.



## Functions (collections)

### `size(a: Str|[~]|[~: ~]) -> Int`

Returns the size of *a*.

### `enumerate(a: Str) -> [(Int, Str)]`
### `enumerate(a: [0]) -> [(Int, 0)]`

Returns each element of *a* with its index.

The equivalent for dictionaries is `entries`.

### `reverse(a: Str) -> Str`
### `reverse(a: [0]) -> [0]`

Iterate from the end to the start.

### `zip(a: Str|Enum|[0], ...) -> [(Str|a|0, ...)]`

Iterate through multiple collections at once, stopping at the end of the shortest one.

### `zip_max(a: Str|Enum|[0], ...) -> [(Str?|a?|0?, ...)]`

Iterate through multiple collections at once, stopping at the end of the longest one.
If some collections stop before others, `NULL` will be used as a default value.

### `foldl(a: [0], f: (0, 0) -> 0) -> 0`
### `foldr(a: [0], f: (0, 0) -> 0) -> 0`

Reduce a list to a single value.

### `product(a: [0], b: [U], f: (0, U) -> V) -> [[V]]`

Creates a matrix containing the result of *f*
for each value of *a* and each value of *b*.

### `map(a: [0], f: 0 -> U) -> [U]`
### `map(a: [K: 0], f: 0 -> U) -> [K: U]`

Maps the elements from *a* to their image by *f*.

### `filter(a: [0], f: 0 -> Bool) -> [U]`
### `filter(a: [K: 0], f: 0 -> Bool) -> [K: U]`

Maps the elements from *a* for wich `f(elem)` is `FALSE`.

### `fill(len: Int, val: 0) -> [0]`

Creates a list of length *len* filled with *val*.

### `map_key(a: [1], f: (Int, 1) -> 3) -> [1]`
### `map_key(a: [2: 1], f: (2, 1) -> 3) -> [2: 3]`

Same as `map`, but the indexes / keys are passed to the mapping function

### `filter_key(a: [0], f: (Int, 0) -> Bool) -> [0]`
### `filter_key(a: [1: 0], f: (1, 0) -> Bool) -> [1: 0]`

Same as `filter`, but the indexes / keys are passed to the filtering function

### `fill_key(len: Int, f: Int -> 0) -> [0]`

Creates a list of length *len* where an element at index i is f(i).

### `values(dict: [0: 1]) -> [1]`

Iterate through the values of *dict*.

### `entries(dict: [0: 1]) -> [(0, 1)]`

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

Returns the unicode codepoint of a character
or the position of a value in an enumeration.



## Functions (conversion)

### `to_int(val: Bool) -> Int`
### `to_int(val: Str) -> Int?`

If *val* is a boolean, `FALSE` becomes `0` and `TRUE` becomes `1`.

If *val* is a string, it will be parsed for an integer literal.
If it is not a valid integer, `NULL` is returned.

Use `round`, `floor` or `ceiling` to convert a `Float` into an `Int`.

### `force_to_int(val: Str) -> Int`

Same as `to_int`, but throws an `ERR_VALUE` if the string is invalid. 

### `to_float(val: Bool) -> Int`
### `to_float(val: Str) -> Int?`

If *val* is a boolean, `FALSE` becomes `0.0` and `TRUE` becomes `1.0`.

If *val* is a string, it will be parsed for a float literal.
If it is not a valid decimal number, `NULL` is returned.

### `force_to_float(val: Str) -> Float`

Same as `to_float`, but throws an `ERR_VALUE` if the string is invalid.

### `to_byte(val: Bool) -> Byte`
### `to_byte(val: Int) -> Byte?`

If *val* is a boolean, `FALSE` becomes `'0` and `TRUE` becomes `'1`.

If *val* is an integer, is is converted to the equivalent `Byte`
if 0 ≤ *val* < 256. `NULL` is returned if *val* is outside the range.

### `force_to_byte(val: Int) -> Byte`

Same as `to_byte`, but throws an `ERR_VALUE` if the value is outside of the range.

### `to_bool(val: ~) -> Bool`

Converts anything into a boolean.

`NULL`, `'0`, `0`, `0.0`, `""`, `[]`, and a closed `File` are all converted to `FALSE`.
Anything else than that is converted to `TRUE`.

### `to_string(val: ~) -> Str`

Gives a representation of *val*, the same way `print val` does.

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

### `trim(text -> Str)`