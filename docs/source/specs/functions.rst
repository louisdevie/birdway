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