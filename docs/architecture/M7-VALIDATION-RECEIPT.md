# M7 Validation Receipt — Function Identity Kernel

Status: **IMPLEMENTED / CORE LOGIC ISOLATED-PASS / FULL REPO CI UNKNOWN**

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
- nested helper binding normalization
- conservative nested-scope internals
- default values remain identity-bearing
- outer-scope default expression preservation (`def f(x=x)` trap)
- dependency partition derivation
- NOEMA relational bridge preserves UNKNOWN phase
- dependency relations are explicit
- CLI schema and threshold-free contract

## Isolated core logic execution

A standalone Python harness reproducing the M7 core normalization/comparison logic
was executed after the scope fixes.

Observed PASS cases:

- alpha-renamed implementation -> `ALIAS`
- changed constant -> `UNKNOWN`
- same qualified symbol with changed invariant -> `CONFLICT`
- same qualified symbol + alpha rename -> `SAME_IDENTITY`
- `numpy as np` / `numpy as alias` -> same `numpy.asarray` dependency + `ALIAS`
- function-local import alias does not leak into another function
- changed default constant remains non-identical
- outer-scope defaults (`x=x` vs `y=y`) remain non-identical
- nested helper rename with identical nested body -> `ALIAS`
- changed nested internal binding -> `UNKNOWN`

Classification: **CORE IDENTITY LOGIC ISOLATED-PASS**.

This is not a substitute for executing the repository's actual pytest suite.

## GitHub Actions

Latest checked run for M7 head lineage:

- workflow: `ci`
- run: `31383063265` (#234)
- job: `all-in-one-quality-gate` (`93437295760`)
- conclusion: `failure`
- `logs_url=null`
- `steps=null`

No Python traceback, assertion, setup step, Ruff result, pytest result, or build
result is observable. Therefore this run is classified as:

**INFRA_BLOCKED / NO STEP EVIDENCE**

It establishes neither code PASS nor code FAIL.

## Authority / mutation

- no CANON promotion
- no `CURRENT` update
- no Actuator invocation
- no repository rewrite based on scanner output
- scanner is read-only

## Verdict

```text
implementation                 = IMPLEMENTED CANDIDATE
core identity isolated logic   = PASS
repository pytest/quality gate = UNKNOWN / INFRA_BLOCKED
PhaseNav projection            = UNKNOWN (intentionally absent)
mutation authority             = NONE
```
