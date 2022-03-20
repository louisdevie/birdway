Loops
=====


Break and Skip
--------------

These two statements can be used inside any of the following loops.
If used inside a block, they will propagate and affect the containing loop.

.. syntax::
   **break**

Exits the loop immediately, skipping the ``then end`` part if there is one.

.. syntax::
   **skip**

Skip to the next iteration of the loop immediately.


For Loop
----------

.. syntax::
   **for** variable **from** a **to** b [**step** increment] **do** expression [**then** end]

``variable`` should be a valid identifier, and a *constant* with this name will
take the values from ``a`` (included) to ``b`` (excluded). If no ``increment``
is specified, the step will be 1 if b ≥ a and -1 otherwise. The sign of the step
is checked at compile time. ``expression`` will be evaluated for each iteration
and the results will be collected in a list, followed by ``end``. The type of
the statement will be the type of ``expression``.

.. warning::
   ``variable`` isn't in scope when ``end`` is evaluated.

For each Loop
--------------

.. syntax::
   **foreach** variable **in** table **do** expression [**then** end]

``variable`` should be a valid identifier, and a *constant* with this name will
take the *values* inside ``table``. ``expression`` will be evaluated for each iteration
and the results will be collected in a list, followed by ``end``. The type of
the statement will be the type of ``expression``, and the type of ``variable`` is
deduced from the type of ``table`` : [int] maps to int, [[int]] maps to [int]
and [int: str] maps to str.

.. warning::
   ``variable`` isn't in scope when ``end`` is evaluated.


While Loop
------------

.. syntax::
   **while** condition **do** expression [**then** end]

``expression`` will be evaluated as long as ``condition`` is true, and
the results will be collected in a list, followed by ``end``. If the
condition is false from the start, there will be no iterations.

Until Loop
------------

.. syntax::
   **do** expression **until** condition [**then** end]

``expression`` will be evaluated until ``condition`` is false, and
the results will be collected in a list, followed by ``end``. Even
if the condition is false from the start, there will be at least
one iteration.