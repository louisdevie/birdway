Conditional Statements
======================


If Statements
-------------

.. note:: Syntax
   **if** condition **then** a **else** b

Takes the value ``a`` if ``condition`` is true, or ``b`` otherwise.
``condition`` has to be a boolean while ``a`` and ``b`` need to be
of the same type, wich will be the type of the if statement.
If ``a`` has type void, the ``else b`` part can be ommitted and nothing
will be done otherwise.


Switch Statements
-----------------

.. note:: Syntax
   **switch** value
   [ **case** case1 **do** value1
   [ **case** case2 **do** value2
   [ ... ] ] ]
   [ **default** defaultvalue ] 

Takes the value of the first ``case`` that match ``value``. The types
accepted for ``value`` are int, byte and enum E. If a ``case`` have
the same type as ``value`` it will match if the two values are equal,
if it is a list of the type of ``value`` (e.g. [int]) it will match if
the value is in the list, and any other type is invalid. All ``values``
have to be of the same type, wich will be the type of the statement.