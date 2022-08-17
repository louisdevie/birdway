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