Signals
=======

Signals are codes that are propagated down the stack until they're *received*.
If a signal reach the bottom of the stack, the signal code is displayed and the program stops.


Error signals
-------------

Error signals are used to stop the program after something went wrong (e.g. a division by zero),
or if the program has successfully finished.
They can be thrown by the user with a :ref:`throw` statement
and received by a :ref:`try` statement.


Others signals
------------------

The :ref:`return`, :ref:`break_next` statements throws specials signals that can't be
received by :ref:`try` statements.
