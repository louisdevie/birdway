Primitive datatypes
===================

.. _void:

Void
----

The ``void`` type means no data. It can't take any value, so there cannot be
void variables or constants, and should not be confused with null.
It also cannot be used within composite types.


.. _bool:

Boolean
-------

The type ``bool`` represents a boolean. It can take two values: ``TRUE`` or ``FALSE``.


.. _int:

Integer
-------
The type ``int`` represents a 64-bit signed integer.

.. note::
   This type can be implicitly converted into a
   a :ref:`byte` or a :ref:`float`.


.. _float:

Floating-point number
---------------------

The type ``float`` represents a 64-bit (double precision) floating-point number.


.. _str:

String
------

The type ``str`` represents an unicode string.
There is no character type, strings of length 1 are used instead.


.. _byte:

Byte
----

An unsigned 8-bit integer. Useful for manipulating binary data.