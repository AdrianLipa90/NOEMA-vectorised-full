# M8 — Relational Function Identity Closure

## Status

IMPLEMENTED CANDIDATE. Read-only. No CANON promotion, CURRENT update, Actuator, dependency rewrite, or module relocation is introduced by M8.

## Why M8 exists

M7 derives a **structural** callable fingerprint from alpha-normalized AST, signature shape, and explicit dependency symbols. That is useful, but it is not yet a closed relational identity.

Two functions can have the same body:

```python
def f():
    return helper()
```

while `A.helper` and `B.helper` are different functions. Therefore:

`same structural invariant != proven relational identity`.

M8 closes the **static source relation** over exact bindings before an invariant may be used as an alias proof at this layer.

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
  -> CLOSED static relational identity or OPEN relational debt
```

No semantic similarity score, embedding distance, folder bonus, hand-authored weight, confidence threshold, or first-match rule participates in the derivation.

## Static closure is not live runtime authority

`CLOSED` in M8 means that the **source-derived dependency relation** is closed under the evidence available to the static scanner. It does not assert that Python's live global namespace can never change.

A module global can be rebound after import or modified by another runtime actor. Therefore:

```text
CLOSED_STATIC_SOURCE_RELATION != VERIFIED_LIVE_RUNTIME_BINDING
```

M8 authority remains `DERIVED_RELATIONAL_NO_AUTHORITY`. Any claim about the live binding of mutable globals requires a separate runtime namespace snapshot/probe and receipt.

This is the same epistemic rule used elsewhere in NOEMA:

```text
absence of observed mutation != proof that mutation is impossible
```

## Occurrence identity

Before relational closure, each concrete callable occurrence is distinguished by a deterministic locator:

```text
occurrence_key = SHA256(source_path, qualified_name, structural_invariant)
```

The locator is provenance for a concrete occurrence. It is not claimed to be semantic identity.

## Exact binding states

- `INTERNAL` — exactly one callable occurrence is resolved by exact source-level symbol relations.
- `ENVIRONMENT` — a dotted symbol is tied to an explicit imported environment identity.
- `AMBIGUOUS` — exact names resolve to more than one occurrence; no first-match selection is allowed.
- `UNRESOLVED` — no exact static proof exists.
- `DYNAMIC` — the call target is not statically named.

### Environment anchors

M8 accepts only environment relations whose source-level provenance is explicit enough for static closure:

- dotted stdlib symbols normalized from explicit imports are anchored to the Python runtime identity;
- dotted external symbols may be anchored only to a uniquely resolved, versioned distribution requirement such as `numpy==2.0.0`;
- unversioned external distributions do not close identity;
- bare names such as `len()` remain OPEN because a module global may shadow the builtin and M8 does not carry a complete live global binding table.

These anchors identify the declared/static dependency environment. They do not freeze the live Python namespace.

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

The SCC condensation graph is emitted because it is a DAG by construction and provides the next derivation surface for dependency topology.

## Relation verdicts

For M8 static relational identities:

- same symbol + same CLOSED relational invariant -> `SAME_IDENTITY`;
- different symbols + same CLOSED relational invariant -> `ALIAS`;
- same symbol + different CLOSED relational invariants -> `CONFLICT`;
- incomplete closure or different symbols with different invariants -> `UNKNOWN`.

No OPEN identity can prove `ALIAS`.

## M10 module-context refinement

M10 preserves the M7 structural observation but supplies exact package-context rewrites to the M8 binder. For example:

```python
from .helper import helper
```

inside `pkg.main` may be observed structurally by M7 as `helper.helper`, while M10 derives the exact package-qualified target:

```text
observed_dependency_symbol = helper.helper
resolved dependency_symbol = pkg.helper.helper
```

Both values are retained in the binding receipt. Relative-import normalization therefore improves closure without rewriting history or erasing the original observation.

## NOEMA bridge

M7 structural state is explicitly represented as:

- `kind=function_structural_identity`;
- identity prefix `function-structural:`;
- authority `DERIVED_STRUCTURAL_NO_AUTHORITY`;
- relations `depends_on-symbol:*`.

M8 CLOSED static state is represented as:

- `kind=function_relational_identity`;
- identity prefix `function-relational:`;
- authority `DERIVED_RELATIONAL_NO_AUTHORITY`.

M8 OPEN state remains occurrence-specific and uses:

- the `occurrence_key` as identity;
- authority `OPEN_RELATIONAL_DEBT_NO_AUTHORITY`;
- explicit closure-debt relations.

Neither bridge fabricates a PhaseNav vector. `phase36=None` and `PhaseSpace.UNKNOWN` remain mandatory until a separate derivation exists.

## CLI

The existing `ciel-function-identity` payload remains schema `CIELPC_FUNCTION_IDENTITY_SCAN_V1` for compatibility and includes:

```text
module_context_dependencies.schema = CIELPC_MODULE_CONTEXT_DEPENDENCIES_V1
relational_closure.schema = CIELPC_RELATIONAL_FUNCTION_CLOSURE_V1
entrypoint_dependency_bundles.schema = CIELPC_ENTRYPOINT_DEPENDENCY_BUNDLES_V1
```

Every derived surface remains threshold-free and read-only.

## Remaining derivations

- live runtime/global binding proof from an explicit namespace snapshot or probe;
- canonical identity for recursive SCCs;
- exact equality-based bundle identity/deduplication;
- read-only generation of installable manifests from CLOSED execution bundles.
