# M7 Validation Receipt — Function Identity Kernel

Status: **IMPLEMENTED / ISOLATED LOGIC PASS / FULL REPO CI UNKNOWN**

## Implemented

- threshold-free `FunctionIdentity` derivation from Python AST
- alpha-normalization of callable-local parameter/binding names
- outer-scope preservation for defaults/decorators/annotations
- import-alias canonicalization
- exact `SAME_IDENTITY / ALIAS / CONFLICT / UNKNOWN` relation
- conservative scope handling for nested functions, `global`, `nonlocal`, and comprehensions
- repository import-root dependency manifest (`stdlib / local / external`)
- distribution resolver with `RESOLVED / AMBIGUOUS / UNRESOLVED`
- derived requirements package with blocked unresolved/ambiguous imports
- declared-vs-derived `pyproject.toml` audit
- read-only bridge to NOEMA `RelationalState`
- no fabricated PNV36 projection
- CLI entrypoint `ciel-function-identity`
- JSON scan payload with explicit `thresholds: []`

## Identity logic isolated execution

A standalone Python harness reproducing the M7 normalization/comparison logic
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

## Dependency resolver isolated execution

Controlled metadata mapping produced:

```text
yaml -> PyYAML==6.0.2       RESOLVED
shared -> dist-a | dist-b   AMBIGUOUS
mystery -> no provider      UNRESOLVED
```

Only `PyYAML==6.0.2` entered the derived package; `shared` and `mystery` entered
`blocked_imports`. No first-match selection occurred.

Classification: **DEPENDENCY RESOLVER LOGIC ISOLATED-PASS**.

## Declaration audit isolated execution

TOML parsing and distribution-name normalization were exercised with core and
optional dependency groups. Derived distributions are compared to declarations
as claims only. Version compatibility is explicitly
`UNKNOWN_NOT_EVALUATED` in this slice.

Classification: **DECLARATION AUDIT LOGIC ISOLATED-PASS**.

## GitHub Actions

Latest checked run:

- workflow: `ci`
- run: `31383607516` (#245)
- job: `all-in-one-quality-gate` (`93439009832`)
- conclusion: `failure`
- `logs_url=null`
- `steps=null`

No setup step, Python traceback, Ruff result, pytest result, build result, or
assertion is observable. This is classified as:

**INFRA_BLOCKED / NO STEP EVIDENCE**

It establishes neither repository code PASS nor repository code FAIL.

## Authority / mutation

- no CANON promotion
- no NOEMA `CURRENT` update
- no Actuator invocation
- no dependency-file rewrite from audit output
- no automatic deletion of declared dependencies
- scanner and audits are read-only

## Verdict

```text
implementation                   = IMPLEMENTED CANDIDATE
core identity isolated logic     = PASS
dependency resolver logic        = PASS
declaration audit logic          = PASS
repository pytest/quality gate   = UNKNOWN / INFRA_BLOCKED
PhaseNav projection              = UNKNOWN (intentionally absent)
mutation authority               = NONE
```
