# BirdwayZero bootstrap interpreter

Although Birdway is meant to be a compiled language,
it's first implementation will be an interpreter written
in Python: the goal here is to have an implementation
of (a subset of) the language ASAP, at the expense of performance and reliability.

## Features

* simple command-line parameters
* primitive types : `Void`, `Bool`, `Int`, `Str` and `File` only
* composite types : lists and tuples only
* basic terminal and file I/O (read from file, write to standard output)