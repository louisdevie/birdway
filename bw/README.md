# Birdway Compiler

*Birdway* is both the name of the language and the compiler.

It is bootstrapping, that is, written in Birdway and compiles itself. 

Birdway code is compiled to intermediary C code,
then a C compiler and a linker native to the platform
are used to build the executable. This allows to port
the language to different platforms more easily.
A future version may use LLVM to stop relying on another compiler. 