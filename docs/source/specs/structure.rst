.. warning::
   This section is incomplete


Structure of a Birdway script
=============================

A Birdway script is divided into five parts:

* `metadata`_
* `parameters`_
* `subcommands`_
* `types`_
* `program`_

The statements ``meta``, ``param``, ``option``, ``flag``,
``subcmd``, ``enum``, ``struct``, and ``run`` are the only ones that
can be used in a script body, and can only be used there.
They must be separated by semicolons.

.. _metadata:

The metadata
------------

The metadata of the application is defined with the ``meta`` statement.

.. syntax::
   **meta** field **=** value

``value`` need to be of type ``str``, and field must be one of:

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Key
     - Value

   * - ``name``
     - the name of the application

   * - ``ver``
     - the version of the application

   * - ``auth'``
     - the authors of the application, separated by semicolons

   * - ``url``
     - a link to the homepage of the application

   * - ``desc``
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
   **flag** *[* modifier *]* name *[* **(** description **)** *]*

As ``name`` will be a constant,
it should be all uppercase with underscores between words,
like ``MY_FLAG``. The flag name will be the same, but lowercase
and with hyphens in place of the underscores. Thus, a flag
named ``MY_FLAG`` will be passed as ``--my-flag``.

If there is no modifier, the flag can be passed only once,
and the result is a ``bool``, whether the flag was passed or not.

If the multiple modifier (an asterisk ``*``) is used,
the resulting value is the number of times the flag was passed (type ``size``).

The ``shortcut`` is an alias of one letter only for the flag.
The flag is then passed with a simple hyphen, like ``-a``.
Several flag shortcuts can be passed at once : ``-abcccd``
is equivalent to ``-a -b -c -c -c -d``.

Options
^^^^^^^

.. syntax::
   **option** *[* modifier *]* name **:** type *[* **=** default *]* *[* **(** description **)** *]*

Options are similar to flags, except they are followed by
an equal sign ``=`` and a value. Thus, a option named ``MY_OPTION``
will be passed as ``--my-option=34``.

If there is no modifier, the option may only be passed once,
and the result will be the value passed converted into a nullable ``type``.
If no value is passed, the result will be ``null``. If there is a
default value, the result will be a ``type`` instead of a ``type?``,
and when no value is passed, the result will be that default value.

If the multiple modifier ``*`` is used, the result will be a
:ref:`list table <table>` containing all the values given, and 
default values connot be used.

Option shortcuts can be used by passing ``-o=56``,
but they cannot be grouped together like flags.
   

Parameters
^^^^^^^^^^

.. syntax::
   **param** *[* modifier *]* name **:** type *[* **=** default *]* *[* **(** description **)** *]*

Parameters are always passed after options and flags. They're identified
by their position, so the order in which you declare them is important.

There can be : one or more parameters without modifier,
followed by one or more parameters with the optional modifier,
followed by only one parameter with the multiple modifier.


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