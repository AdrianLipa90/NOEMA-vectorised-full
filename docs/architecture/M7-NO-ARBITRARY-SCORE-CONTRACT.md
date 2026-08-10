# M7 — No Arbitrary Score Contract

Function identity is not a ranking problem.

The M7 identity kernel therefore forbids:

- semantic similarity thresholds,
- manually tuned identity weights,
- path/name bonuses,
- folder-based authority,
- first-match dependency resolution.

A relation is emitted only from exact derived conditions:

```text
same symbol + same invariant -> SAME_IDENTITY
different symbol + same invariant -> ALIAS
same symbol + different invariant -> CONFLICT
otherwise -> UNKNOWN
```

Any future probabilistic or embedding-based search may propose candidates for
comparison, but it may not promote an identity relation. Promotion requires the
exact invariant proof or a stronger explicitly versioned proof system.
