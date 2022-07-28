About syntax definitions
========================

The syntax of the language will be defined with syntax admonitions like this one :

.. syntax::
   <something>

A symbol or a keyword in bold is literal :

.. syntax::
   | **let**
   | **(** 
   | **;**


A name preceded by an ampersand is a lexical token (see :ref:`lex`) :

.. syntax::
   | &IDENT


A name between chevrons is a syntax construct :

.. syntax::
   | <expr>


A name followed by a colon is just an annotation to give a meaning to an element:

.. syntax::
   | *value:* <expr> 


A vertical bar indicates multiple possibilities :

.. syntax::
   | **@** *|* **$**


Parentheses are used to group elements together :

.. syntax::
   | *(* **:** <type> *)*


Square brackets indicate that something is optional :

.. syntax::
   | *[* **:** <type> *]*


Braces indicate that something may be present zero or more times.
The optional element after the slash is the separator, wich must be present
between each repeated part, and optionally at the end :


.. syntax::
   | *{* <expr> */}*
   | *{* <expr> */* **,** *}*