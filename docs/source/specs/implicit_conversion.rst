.. _iconv:

Implicit Conversion
===================

When two values of different types are assigned to the same variable,
there can be an implicit conversion of the values into an unique type.


Nullable Implicit Conversion
----------------------------

When a variable is assigned both ``T`` and ``void`` values, the variable
ends up of type ``T?`` and all the values are converted into that type.


Numeric Implicit Conversion
---------------------------

When a ``float`` variable is assigned ``int`` values, these will be
converted into ``float`` implicitly.


.. note::
	The two conversions above can happen for the same variable,
	that is, if a variable is assigned ``int``, ``float`` and ``void``
	values, they will all be converted into ``float?``.