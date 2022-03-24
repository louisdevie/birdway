.. warning::
   This section is incomplete

Structure of a Birdway script
=============================

A birdway script is divided into five parts:

* `metadata`_
* `parameters`_
* `subcommands`_
* `types`_
* `program`_

The special satements ``meta``, ``param``, ``option``, ``flag``,
``subcmd``, ``enum``, ``struct``, et ``run`` are the only ones that
can be used in a script body, and can only be used there.
They must be separated by semicolons.

The metadata
------------

The metadata of the application is defined with the ``meta`` statement.

.. syntax::
   **meta** table

``table`` need to be a dictionary table of type ``[str:str]``,
with the following fields used:

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Key
     - Value

   * - name

   * - Row 2, column 1
     - Row 2, column 2
     - Row 2, column 3