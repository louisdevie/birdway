Functions
=========

Calling functions
-----------------

.. syntax::
   function_name **(** *[* argument1 *[* **,** argument2 *[...]* *]* *]* **)**

Call the implementation of the function that match
the types and the number of the arguments passed.
If multiples implementations match, the less ambiguous one
(the one with the least generic types) is used.

Defining functions
------------------

.. syntax::
   **func** function_name **(**
      *[* argument1 *[* **:** type1 *]*
         *[* **,** argument2 *[* **:** type2 *]*
            *[...]*
         *]*
      *]*
   **) ->** result

A function can be have multiple implementations with different types or number of parameters.
A block with a ``return`` statement inside can be used as the result of the function.

Forward definitions
-------------------

.. syntax::
   **func** function_name

A function declaration without parenthesis nor return value is a forward declaration
and a function with the same name must be defined in the same scope as the forward declaration.
