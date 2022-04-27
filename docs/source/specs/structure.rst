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

The satements ``meta``, ``param``, ``option``, ``flag``,
``subcmd``, ``enum``, ``struct``, et ``run`` are the only ones that
can be used in a script body, and can only be used there.
They must be separated by semicolons.

.. _metadata:

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

   * - ``'name'``
     - the name of the application

   * - ``'version'``
     - the version of the application

   * - ``'authors'``
     - the authors of the application, separated by semicolons

   * - ``'url'``
     - a link to the homepage of the application

   * - ``'description'``
     - a short description


.. _subcommands:

Sub-commands
------------


.. _parameters:

The command-line parameters
---------------------------


Flags
^^^^^

.. syntax::
   **flag** [ modifier ] name [ shortcut ] [ description ]

Flags starts with two hyphens ``--``. As ``name`` is a constant,
it should be all uppercase with underscores between words,
like ``MY_FLAG``. The flag name will be the same, but lowercase
and with hyphens in place of the underscores. Thus, a flag
named ``MY_FLAG`` will be passed as ``--my-flag``.

If there is no modifier, the flag can be passed only once,
and the result is a ``bool``, wether the flag was passed or not.

If the multiple modifier (an asterisk ``*``) is used,
the resulting value is the number of times the flag was passed (type ``size``).

The ``shortcut`` is an alias of one letter only for the flag.
The flag is then passed with a simple hyphen, like ``-a``.
Several flag shortcuts can be passed at once : ``-abcccd``
is equivalent to ``-a -b -c -c -c -d``.

Options
^^^^^^^

.. syntax::
   **option** [ modifier ] type name [ shortcut ] [ description ]

Options are similar to flags, except they are followed by
an equal sign ``=`` and a value. Thus, a option named ``MY_OPTION``
will be passed as ``--my-option=34``.

If there is no modifier, the option may only be passed once,
and the result will be the value passed converted into a nullable ``type``.
If no value is passed, the result will be ``<null>``.

If the multiple modifier ``*`` is used, the result will be a
:ref:`list table <table>` containing all the values given.

Option shortcuts can be used by passing ``-o=56``,
but they cannot be grouped together like flags.
   

Parameters
^^^^^^^^^^

.. syntax::
   **param** [ modifier ] type name [ description ]


.. _types:

Type declarations
-----------------


Enumerations
^^^^^^^^^^^^


Structures
^^^^^^^^^^


.. _program:

The actual program
------------------