Conditional Statements
======================

.. _if:
If Statements
-------------

.. syntax::
   | **if** *condition:* <expr>
   | **then** *a:* <expr>
   | *[* **else** *b:* <expr> *]*

Takes the value *a* if *condition* is ``TRUE``, or *b* otherwise.

*condition* has to be a :ref:`bool` while *a* and *b* need to be
of the same type, which will be the type of the if statement.

The ``else`` part can be omitted, and the statement will take
the value ``NULL`` if *condition* is ``FALSE``.


.. _switch:
Switch Statements
-----------------

.. syntax::
   | **switch** *value:* <expr>
   | *{* **case** *case:* <expr> **do** *result:* <expr> */}*
   | *[* **default** *default:* <expr> *]*

Takes the value of the *result* of the first *case* that match *value*.

The types accepted for *value* are :ref:`integers <int>`, :ref:`bytes <byte>`
and :ref:`enumerations <enum>`. If a ``case`` have the same type as *value*,
it will match if the two values are equal; if it is a list of the type of *value*,
it will match if the value is in the list.
All *results* have to be of the same type, which will be the type of the statement.