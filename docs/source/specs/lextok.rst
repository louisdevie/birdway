.. _lex:

Lexical structure
=================

By default, a Birdway source file should be read as UTF-8.

All whitespace characters are ignored, as well as comments.
Line comments begin with two consecutive hyphens ``--`` and end at the next line feed.
Block comments start with three consecutive hyphens ``---`` and end at the next triple-hypens.

.. why::
   Both ``//`` and ``#`` were already in use as operators,
   so I decided to use ``--`` for line comments, as it is not unusual
   (for example, Lua, Haskell, SQL and Ada uses this style of comments)
   and ``---`` for block comments for consistency and simplicity.
   Plus it let you make nice arrow comments :

   .. code-block:: bw

      let a = 5;
      println a * 3; --> 15


Keywords (``&KEYWORD``)
-----------------------

Any of the keywords defined in :ref:`appendix 1 <reserved>`, surrounded by word boundaries.

You won't see it used often in syntax definitions, as keywords will be specified literally. 


Symbols (``&SYMBOL``)
---------------------

The language punctuation : ::

   {    opening brace
   }    closing brace
   (    opening parenthesis
   )    closing parenthesis
   [    opening square bracket
   ]    closing square bracket
   .    dot
   ,    comma
   ;    semicolon
   :    colon
   ::   double colon
   @    at symbol
   $    dollar sign
   _    underscore

Like keywords, they will often be specified literally.


Operators (``&OP-UN``, ``&OP-BIN``, ``&OP-UN-BIN``, ``&OP-BIN-TER``)
--------------------------------------------------------------------

The different operators : ::

   ~     tilde                            OP-UN
   #     hash                             OP-UN
   ?     question mark                    OP-UN
   !     exclamation mark                 OP-UN
   not   (keyword operator)               OP-UN

   -     hyphen                           OP-UN-BIN

   &     ampersand                        OP-BIN
   &&    double ampersand                 OP-BIN
   |     vertical bar                     OP-BIN
   ^     caret                            OP-BIN
   +     plus sign                        OP-BIN
   ==    double equal sign                OP-BIN
   %     per cent sign                    OP-BIN
   *     asterisk                         OP-BIN
   **    doubme asterisk                  OP-BIN
   /     slash                            OP-BIN
   //    double slash                     OP-BIN
   !=    exclamation mark and equal sign  OP-BIN
   <<    double less than sign            OP-BIN
   >     greater than sign                OP-BIN
   >=    greater than sign and equal sign OP-BIN
   >>    doubel greater than sign         OP-BIN
   and   (keyword operator)               OP-BIN
   or    (keyword operator)               OP-BIN
   xor   (keyword operator)               OP-BIN

   <     less than sign                   OP-BIN-TER
   <=    less than sign and equal sign    OP-BIN-TER

Keyword operators needs to be whole words (there must be a word boundary before and after).


Primitives (``&PRIMITIVE``)
--------------------------

Any of the type primitives defined in :ref:`appendix 1 <reserved>`, surrounded by word boundaries.


Identifiers (``&IDENT``)
------------------------

Identifiers starts with an alphabetic character (ASCII letters) or an underscore,
followed by zero or more alphanumeric characters (ASCII letters and numbers) or undercores.
It must not be a keyword, symbol, operator nor primitive.

.. note::
   An implementation of the language must support *at least* ASCII identifiers,
   but may support Unicode identifiers. 

Delimiters (``&STR-DELIM``)
----------------------------

Double quotes ``"`` are string literals delimiters.


Text (``&TEXT``)
----------------

Any text inside string literals.

.. note::
   Interpolations aren't text, they should be read the same way as
   the rest of the program. For example, the following :

   .. code-block:: bw

      "Hi $name !"

   is read as ::

      &STR-DELIM   "
      &TEXT        Hi␣
      &SYMBOL      $
      &IDENT       name
      &TEXT        ␣!
      &STR-DELIM   "