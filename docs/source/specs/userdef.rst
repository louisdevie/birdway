User-defined types
==================

.. _enum:
Enumerations
------------

Declaration
^^^^^^^^^^^

.. syntax::
   **enum** *name:* &IDENT **(** *{* *value:* &IDENT */* **,** *}* **)**



.. _struct:
Structures
----------

Structures are used to group together different types.
Each field is named and has a non-generic type.
Structures can be created literally
using the syntax ``MyStruct (field1: value1, field2: value2)``.