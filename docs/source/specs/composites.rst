Composite datatypes
===================

These are types that are formed using other types.


.. _nullable:

Nullable types
--------------

Represents a type that may be uninitialised.
A nullable type ``T?`` can be either a value of type ``T`` or ``null``.
Everything that can be done with ``T`` can be done with ``T?``,
except that an error will occur if it is null.
(Example: if ``a`` has type ``int?``, then ``a + 5`` is valid and will compile,
but an error will be thrown at runtime if ``a`` happens to be null.)


.. _table:

Tables
------

Tables are data structure that maps keys to values,
with all the keys having the same type and all the values having the same type too.

List tables
^^^^^^^^^^^

In a list, the values are automatically indexed by integers starting at 0.
Lists can be created literally using the syntax ``[a, b, c, d, e]``.

List types are represented as ``[T]`` where T is the type of the values.

Dictionary tables
^^^^^^^^^^^^^^^^^^

In a dictionary, the values are indexed manully by any type.
Dictionaries can be created literally using the syntax ``[key1: a, key2: b, key3: c]``.

Dictionary types are represented as ``[U: T]``
where T is the type of the values and U the type of the keys.


.. _enum:

Enumerations
------------

Enumerations are a finite set of values,
declared with the ``enum`` statement in the ``types`` block.
An ``enum`` is an enumeration, while ``enum E`` is a value of ``E``.

.. _struct:

Structures
----------

Structure are used to group together different types.
Use the ``struct`` statement in the ``types`` block to declare a structure.
Each field is named and that name must always be explicitly stated,
there are no anonymous structures. Structures can be created literally
using the syntax ``MyStruct (field1: value1, field2: value2)``.