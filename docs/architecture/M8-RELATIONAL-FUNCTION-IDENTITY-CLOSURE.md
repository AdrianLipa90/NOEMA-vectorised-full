# M8 — Relational Function Identity Closure

## Status

IMPLEMENTED CANDIDATE. Read-only. No CANON promotion, CURRENT update, Actuator, dependency rewrite, or module relocation is introduced by M8.

## Why M8 exists

M7 derives a **structural** callable fingerprint from alpha-normalized AST, signature shape, and explicit dependency symbols. That is useful, but it is not yet a closed system identity.

Two functions can have the same body:

```python
def f():
    return helper()
```

while `A.helper` and `B.helper` are different functions. Therefore:

`same structural invariant != proven relational identity`.

M8 closes identity over exact bindings before an invariant may be used as a system-level alias proof.

## Derivation

```text
Python callable occurrence
  -> M7 structural invariant
  -> exact dependency symbols
  -> exact internal binding / imported environment anchor / debt
  -> directed occurrence graph
  -> strongly connected components
  -> condensation DAG
  -> recursive relational hash on closed acyclic dependencies
  -> CLOSED relational identity or OPEN relational debt
```

No semantic similarity score, embedding distance, folder bonus, hand-authored weight, confidence threshold, or first-match rule participates in the derivation.

## Occurrence identity

Before relational closure, each concrete callable occurrence is distinguished by a deterministic locator:

```text
occurrence_key = SHA256(source_path, qualified_name, structural_invariant)
```

The locator is provenance for a concrete occurrence. It is not claimed to be semantic identity.

## Exact binding states

- `INTERNAL` — exactly one callable occurrence is resolved by exact symbol names.
- `ENVIRONMENT` — a dotted symbol is tied to an explicit imported environment identity.
- `AMBIGUOUS` — exact names resolve to more than one occurrence; no first-match selection is allowed.
- `UNRESOLVED` — no exact proof exists.
- `DYNAMIC` — the call target is not statically named.

### Environment anchors

M8 currently accepts only bindings whose provenance is explicit enough to avoid silent shadowing:

- dotted stdlib symbols normalized from explicit imports are anchored to the Python runtime identity;
- dotted external symbols may be anchored only to a uniquely resolved, versioned distribution requirement such as `numpy==2.0.0`;
- unversioned external distributions do not close identity;
- bare names such as `len()` remain OPEN because a module global may shadow the builtin and M8 does not yet carry a complete global binding table.

This is intentional: absence of shadowing evidence is not evidence of absence.

## Relational closure

For an acyclic occurrence whose every dependency is closed, the relational invariant is:

```text
SHA256(
  structural_invariant,
  sorted(dependency_anchors)
)
```

An internal dependency anchor contains the **relational invariant of the target**, not merely the textual target name.

Therefore two structurally identical callers of different helpers do not collapse to one alias.

## Recursive components

Strongly connected components are derived exactly from internal call edges. SCCs are useful as non-arbitrary functional components, but M8 does not yet assign a canonical semantic identity to a recursive cycle. Any member of a recursive SCC remains `OPEN` with explicit debt:

`recursive dependency component requires separate cycle proof`.

The SCC condensation graph is emitted because it is a DAG by construction and provides the next derivation surface for package/module topology.

## Relation verdicts

For M8 relational identities:

- same symbol + same CLOSED relational invariant -> `SAME_IDENTITY`;
- different symbols + same CLOSED relational invariant -> `ALIAS`;
- same symbol + different CLOSED relational invariants -> `CONFLICT`;
- incomplete closure or different symbols with different invariants -> `UNKNOWN`.

No OPEN identity can prove `ALIAS`.

## NOEMA bridge

M7 structural state is now explicitly represented as:

- `kind=function_structural_identity`;
- identity prefix `function-structural:`;
- authority `DERIVED_STRUCTURAL_NO_AUTHORITY`;
- relations `depends_on-symbol:*`.

M8 CLOSED state is represented as:

- `kind=function_relational_identity`;
- identity prefix `function-relational:`;
- authority `DERIVED_RELATIONAL_NO_AUTHORITY`.

M8 OPEN state remains occurrence-specific and uses:

- the `occurrence_key` as identity;
- authority `OPEN_RELATIONAL_DEBT_NO_AUTHORITY`;
- explicit closure-debt relations.

Neither bridge fabricates a PhaseNav vector. `phase36=None` and `PhaseSpace.UNKNOWN` remain mandatory until a separate derivation exists.

## CLI

The existing `ciel-function-identity` payload remains schema `CIELPC_FUNCTION_IDENTITY_SCAN_V1` for compatibility and gains:

```text
relational_closure.schema = CIELPC_RELATIONAL_FUNCTION_CLOSURE_V1
relational_closure.thresholds = []
```

The section contains occurrence identities, exact bindings, SCC components, condensation edges, and closure debt.

## Next derivation

The condensation DAG gives a threshold-free basis for deriving higher-level execution/dependency components. The next step must not call every SCC a package by fiat; it should derive package boundaries only from explicit entrypoints, dependency closure, authority/lifecycle boundaries, and distribution/runtime constraints.
