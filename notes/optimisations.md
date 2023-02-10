# List of possible optimisations

- [ ] when printing a string literal with interpolation,
      break down the statement into multiple print statements

- [ ] compute everything that is constant at compile-time

- [ ] transform any block like `{ expr }` into just `expr`

- [ ] transform any block like `{ expr; }` where `expr` has type `Void`
      into just `expr`

- [ ] transform function blocks like `{ return expr; }` into just `expr`

- [ ] TCO

- [ ] Inline functions

- [ ] If a binding is used only once, inline the expression
