# M7 Validation Receipt — Function Identity Kernel

Status: **TEST-SPECIFIED / EXECUTION PENDING**

## Implemented

- threshold-free `FunctionIdentity` derivation from Python AST
- alpha-normalization of local parameter/local binding names
- import-alias canonicalization
- exact `SAME_IDENTITY / ALIAS / CONFLICT / UNKNOWN` relation
- conservative scope handling for nested functions, `global`, `nonlocal`, and comprehensions
- repository import-root dependency manifest (`stdlib / local / external`)
- read-only bridge to NOEMA `RelationalState`
- no fabricated PNV36 projection
- JSON scan CLI payload with explicit `thresholds: []`

## Tests specified

- alpha-renaming invariance
- constants remain identity-bearing
- same-symbol conflict detection
- import alias invariance
- function-local alias isolation
- conservative nested-function behavior
- default values remain identity-bearing
- dependency partition derivation
- NOEMA relational bridge preserves UNKNOWN phase
- dependency relations are explicit
- CLI schema and threshold-free contract

## Authority / mutation

- no CANON promotion
- no `CURRENT` update
- no Actuator invocation
- no repository rewrite based on scanner output
- scanner is read-only

## Verdict

Executable test verdict is **UNKNOWN UNTIL RUN**.
