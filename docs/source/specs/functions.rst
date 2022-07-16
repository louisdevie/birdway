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
      *[* arg1 *[* **:** type1 *]* *[* **,** arg2 *[* **:** type2 *]* *[...]* *]* *]*
   **) ->** result

A function can be have multiple implementations with different types or number of parameters.
A block with a ``return`` statement inside can be used as the result of the function.


Forward definitions
-------------------

.. syntax::
   **func** function_name

A function declaration without parentheses and return value is a forward declaration.
All further function declarations with the same name will be moved there. 