Composite datatypes
===================

These are types that are formed using other types.


.. _nullable:
Nullable types
--------------

.. syntax::
   | **(** <type> **) ?** *|* <type> **?**

Represents a type that may be uninitialised.
A nullable type ``T?`` can be either a value of type ``T`` or ``NULL``.
Everything that can be done with ``T`` can be done with ``T?``,
except that an error will occur if it is ``NULL``.
(Example: if ``a`` has type ``Int?``, then ``a + 5`` is valid and will compile,
but an error will be thrown at runtime if ``a`` happens to be ``NULL``.)

Void and nested nullables types (``Void?`` and ``T??`` for any type ``T``)
aren't valid types.


.. _list:
Lists
-----

A list is an ordered collection of values indexed by integers starting at 0.
Lists can be created literally using the following syntax :

.. syntax::
   | **[** *{ value:* <expr> */* **,** *}* **]**

List types are written as ``[T]`` where T is the type of the values :

.. syntax::
   | **[** <type> **]**

Void lists (``[Void]``) aren't valid.


.. _dict:
Dictionaries
------------

A dictionary is a collection mapping keys to values.
Dictionaries can be created literally using the following syntax :

.. syntax::
   | **[** *{ key:* <expr> **:** *value:* <expr> */* **,** *}* **]**

Dictionary types are represented as ``[K: T]``
where T is the type of the values and K the type of the keys :

.. syntax::
   | **[** <type> **:** <type> **]**

The keys type must be hashable and the values type cannot be ``Void``.


.. _union:
Tuples
------

An a tuple is a groups of multiple different types.
Tuples can be created literally using the following syntax :

.. syntax::
   | **(** *{ value:* <expr> */* **,** *}* **)** 

Unlike lists, the values can have different types. A tuple type
is represented as ``(T1, T2, T3, ...)`` where ``Tn`` is the type
of the nth field :

.. syntax::
   | **(** *{* <type> */* **,** *}* **)**

Tuples must have at least 2 fields,
as bare parentheses ``()`` are invalid and ``(value)`` evaluates to just ``value``.


.. _functype:
Function types
--------------

The type of a funtion is represented as ``(T1, T2, ...) -> (R)``
where ``Tn`` is the type of the nth argument and ``R`` the type of
the result :

.. syntax::
   | **(** *{* <type> */* **,** *}* **) -> (** <type> **)** 
   | *|* **(** *{* <type> */* **,** *}* **) ->** <type> 
   | *|* <type> **-> (** <type> **)**
   | *|* <type> **->** <type> 