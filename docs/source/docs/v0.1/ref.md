@base

# Birdway 0.1 language reference

!!! warning
    This document is still a draft.


## 1. Program structure


### 1.1. Units


#### 1.1.1. File format


#### 1.1.2. Entry point


#### 1.1.3. Module units


### 1.2. Application structure


### 1.3. Package structure


## 2. Lexical elements


### 2.1. Whitespaces


### 2.2. Comments


### 2.3. Punctuation


### 2.4. Literal constants


### 2.5. Identifiers


#### 2.5.1. Reserved identifiers


##### 2.5.1.1. Keywords


##### 2.5.1.2. Primitive types


## 3. Types


### 3.1. Primitive types


#### 3.1.1. Void


#### 3.1.2. Booleans


#### 3.1.4. Integers


#### 3.1.5. Floating-point numbers 


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


## 4. Expressions


### 4.1. Constant values


### 4.2. Composite types literals


#### 4.2.1. List literals


#### 4.2.2. Dictionary literals


#### 4.2.3. Tuple literals


#### 4.2.4. Structure literals


### 4.3. Bound values


#### 4.3.1. Constant bound values


#### 4.3.2. Field access


### 4.4. Operations


#### 4.4.1. Unary operations


#### 4.4.2. Binary operations


#### 4.4.3. Operator precendence


### 4.5. Ranges


### 4.6. If-then-else


### 4.7. Loops


#### 4.7.1. For loops


#### 4.7.2. While loops


### 4.8. Error handling


### 4.9. Functions


#### 4.9.1. Calling functions


##### 4.9.1.1. Overload resolution


#### 4.9.2. Anonymous functions


##### 4.9.2.1. Closures


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


## 6. Declarations


### 6.1. Unit-level declarations


#### 6.1.1. Use statement


#### 6.1.2. Type declarations


##### 6.1.2.1. Enumeration declarations


##### 6.1.2.2. Structure declarations


#### 6.1.3. Command-line arguments


##### 6.1.3.1. Parameters


##### 6.1.3.2. Options and flags


### 6.2. Block-level declarations


#### 6.2.1. Constant declarations


#### 6.2.2. Function declarations


#### 6.2.3. Bindings


##### 6.2.3.1. Mutable bindings


#### 6.2.4. Flow control


##### 6.2.4.1. Skip


##### 6.2.4.2. Break


##### 6.2.4.3. Return


##### 6.2.4.3. Throw


## 7. Modules and scope


### 7.1. Scope of constants and bindings


#### 7.1.1. Name resolution


### 7.2. Module exports


## 8. Built-ins


### 8.1. Input/Output


### 8.2. File Paths


### 8.3. Conversions


### 8.4. Mathematics


### 8.5. Operations on collections