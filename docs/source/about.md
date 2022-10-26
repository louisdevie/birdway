@base

# About

The goal of this project is to design a programming language and implement a
compiler for it. This project started in June of 2021, and the language has
evolved a lot since then. I'm waiting to have a stable language specification
before writing a compiler.

The project is still in planning. 

## The language

The language, called *Birdway*, is meant to create command-line applications
by having I/O, argument parsing and TUI integrated into the language. Its main
features are described below.

### Functional and imperative programming

Birdway is mainly a functional programming language, while supporting imperative
programming features (loops, conditionals, ...), kind of like Rust.

### Immutablity by default

All bindings are immutable by default, but mutable variables can still be
declared explicitly.

### A very simple type system

Birdway has only eight primitive datatypes, a few composite ones and allows
user-defined structures and enumerations.

### First-class / anonymous functions

In Birdway, functions are first-class citizens and can be declared and used
anywhere like any other type.

### Full type inference

Birdway is statically and strongly typed, but doesn't require bindings,
function arguments and return values to be typed. The type of a value is
determined by how it is created and used.

### Other features

* Function overloading
* Command-line arguments parsing
* CFFI

## The compiler

The compiler, called *bw*, will compile Birdway code down to machine code,
creating small and fast standalone executables.
