Signals
=======

Signals are codes that are propagated in the stack until catched.
If a signal reach the bottom of the stack, the program stops and an error message is shown.


Error signals
-------------

Error signals are used to stop the program after something went wrog (e.g. a division by zero),
or if the program has successfully finished (:ref:`success` statement).
They can be recieved by a :ref:`try` statement.


Loop break signals
------------------

The :ref:`break_skip` statements emit a signal to stop the loop immediately,
and can only be recieved by loops.