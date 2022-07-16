Blocks
======

Blocks are used to executes multiple statements one after another.

.. syntax::
   **{** statement1 **;** *[* statement2 **;** *[ ... ]* *]* **}**

Each statement is evaluated one after another,
and if a signal is sent by one of the statements,
the block stops its execution and propagate the signal.