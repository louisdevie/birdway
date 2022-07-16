Signals
=======

Signals are codes that are propagated down the stack until they're *received*.
If a signal reach the bottom of the stack, the signal code is displayed and the program stops.


Error signals
-------------

Error signals are used to stop the program after something went wrong (e.g. a division by zero),
or if the program has successfully finished.
They can be received by a :ref:`try` statement.


Loop break signals
------------------

The :ref:`break_next` statements emit a signal to stop the loop immediately,
and can only be received by loops.