.. _primitive:
Primitive datatypes
===================

.. _void:
Void
----

The ``Void`` type means no data. It can't take any value, so there cannot be
``Void`` variables or constants. The constant ``NULL`` is of type ``Void``,
and used with nullable variables.
It also cannot be used within composite types.


.. _bool:
Boolean
-------

The type ``Bool`` represents a boolean. It can take two values: ``TRUE`` or ``FALSE``.


.. _int:
Integer
-------
The type ``Int`` represents a 64-bit signed integer.
Decimal (``123``), hexadecimal (``0x7b``) and binary (``0b1111011``) literals are integers.

.. note::
   This type can be implicitly converted into a :ref:`float`.
   See :ref:`iconv` for more information.

.. warning::
   Using two's complement with hexadecimal or binary literals
   (e.g. ``0xffffffffffffff85``) will result in an overflow error.
   Negative literal numbers are written as ``-0x7b`` or ``-0b1111011``.


.. _float:
Floating-point number
---------------------

The type ``Float`` represents a 64-bit (double precision) floating-point number.
Float literals are written as ``12.3`` or ``0.123E+2``
(for scientific notation, the E must be uppercase,
the sign of the exponent must always be present,
and the number doesn't need to be be between 1 and 10).
``Float``s doesn't support NAN and infinity values.

.. warning::
   Even if ``123E+4`` is technically an integer, it will be interpreted as a ``Float``.


.. _str:
String
------

The type ``Str`` represents an Unicode string.
There is no character type, strings of length 1 are used instead.
String literals are enclosed in double quotes : ``"Hello"``.
They support variable interpolation (a dollar sign followed by the variable name, e.g. ``"x = $x"``)
and expression interpolation (a dollar sign followed by
the expression wrapped in parentheses, e.g. ``"x² = $(x**2)"``).

.. list-table:: String escape sequences
   :widths: 20 80
   :header-rows: 1

   * - Escape
     - Expansion
   * - ``\\``
     - ``\``
   * - ``\"``
     - ``"``
   * - ``\$``
     - ``$``
   * - ``\n``
     - A newline (ASCII character 10/LF)
   * - ``\t``
     - A tabulation (ASCII character 9/TAB)
   * - ``\r``
     - A carriage return (ASCII character 13/CR)
   * - ``\uXXXX``
     - | The Unicode character with code U+XXXX
       | (XXXX must be a hexadecimal number,
       | a valid Unicode code point and written with at least 4 digits)


.. _byte:
Byte
----

The ``Byte`` type is an unsigned 8-bit integer used to manipulate binary data.

.. note::
   This type can be implicitly converted into an :ref:`int` or a :ref:`float`.
   See :ref:`iconv` for more information.


.. _regex:
RegEx
-----


.. _stream:
Stream
------