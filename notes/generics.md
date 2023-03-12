## Rules

```
G{{T1, T2, ...}, {U1, U2, ...}} = Σ G{T, U}

G{T, α} = W{T}

G{Int, Int} = 0

W{Int} = 2

G{Int, Float} = 1

G{[T], [U]} = G{T, U}

W{[T]} = 1 + W{T}

G{(T1, T2, ...), (U1, U2, ...)} = Σ G{T, U}

W{(T1, T2, ...)} = σ (T1, T2, ...)

G{[T -> U], [V -> W]} = G(T, V) + G(U, W)

W{[T -> U]} = 1 + W{T} + W{U}

G{(T1, T2, ...) -> R, (U1, U2, ...) -> S} = G(R, S) + Σ G{T, U}

W{(T1, T2, ...) -> R} = 1 + W{R} + Σ W{T}
```

## Examples

```
G{[Int], [Int]} = G{Int, Int}
                = 0

G{[Int], [Float]} = G{Int, Float}
                  = 1

G{[Int], [α]} = G{Int, α}
              = W{Int}
              = 2

G{[Int], α} = W{[Int]}
            = 1 + W{Int}
            = 3
```

```
G{{Int, Float}, {Int, Float}} = G{Int, Int} + G{Float, Float}
                              = 0 + 0
                              = 0

G{{Int, Float}, {Float, Float}} = G{Int, Float} + G{Float, Float}
                                = 1 + 0
                                = 1

G{{Int, Float}, {Int, α}} = G{Int, Int} + G{Float, α}
                          = 0 + W{Float}
                          = 0 + 2
                          = 2

G{{Int, Float}, {Float, α}} = G{Int, Float} + G{Float, α}
                            = 1 + W{Float}
                            = 1 + 2
                            = 3

G{{Int, Float}, {α, α}} = 
```