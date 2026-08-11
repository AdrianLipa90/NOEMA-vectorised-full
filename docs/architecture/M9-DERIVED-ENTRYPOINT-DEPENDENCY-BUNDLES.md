# M9 — Derived Entrypoint Dependency Bundles

## Status

IMPLEMENTED CANDIDATE on top of M8, refined by M10 module-context dependency derivation. Read-only. No package rewrite, file relocation, dependency deletion, CANON promotion, CURRENT update, or Actuator action is introduced.

## Problem

A traditional dependency package is often assembled top-down:

- choose a module/package boundary;
- collect imports inside it;
- decide which declarations belong together;
- write a dependency list.

Those boundaries may be useful conventions, but they are not necessarily derived from execution.

M9 reverses the direction. The system starts only from an explicit executable declaration already present in `pyproject.toml`:

```toml
[project.scripts]
name = "module:callable"
```

and derives everything reachable from that callable through the exact M8/M10 binding graph.

## Definition

For a declared entrypoint `e` with exactly resolved target occurrence `t`:

```text
Bundle(e) = transitive internal dependency closure(t)
```

plus the environment anchors observed on every occurrence in that closure.

This is an **execution dependency bundle**, not automatically a Python distribution package or filesystem directory.

## Derivation

```text
[project.scripts] declaration
  -> exact module:attribute parse
  -> exact qualified function target
  -> unique concrete occurrence
  -> M10 module/package context normalization
  -> M8 directed internal binding graph
  -> transitive reachable occurrence set
  -> SCC/component membership
  -> environment anchors
  -> pinned external requirements
  -> CLOSED bundle or explicit OPEN blockers
```

No score, similarity threshold, path proximity, folder membership, naming convention, manual weight, or first-match rule participates.

## Target resolution

- invalid `module:attribute` syntax -> `INVALID`;
- no exact target occurrence -> `UNRESOLVED`;
- more than one exact occurrence -> `AMBIGUOUS`;
- exactly one target -> derive its transitive closure.

An ambiguous entrypoint is never bound by lexical ordering.

## Bundle state

A bundle is `CLOSED` only if every occurrence in its reachable closure is relationally CLOSED and every reachable call binding is INTERNAL or ENVIRONMENT at the static-source layer.

Any unresolved, ambiguous, dynamic, recursive, or otherwise open dependency propagates into bundle blockers and makes the bundle `OPEN`.

This preserves the invariant:

```text
OPEN child -> OPEN execution bundle
```

rather than silently treating missing dependency proof as optional.

`CLOSED` remains a static-source verdict and does not itself verify a live mutable Python global namespace.

## External requirements

M9 does not rescan arbitrary declarations to guess a requirement. It reuses M8 environment anchors derived from the M10 dependency manifest.

For example:

```text
distribution:numpy==2.0.0:numpy.asarray
```

derives the requirement:

```text
numpy==2.0.0
```

Only already version-anchored external bindings can contribute requirements to a CLOSED bundle.

Stdlib runtime anchors remain environment provenance but do not become distribution requirements.

## Shared closure is allowed

Bundles are not forced to form a partition.

If two entrypoints share helper functions, their derived occurrence sets may overlap. Forcing disjoint ownership would reintroduce an arbitrary boundary.

If two entrypoints ultimately derive exactly the same closed dependency closure, they are different declared entrypoints into the same execution dependency structure. A later layer may deduplicate their build/runtime payload by exact bundle identity, but M9 does not impose that rewrite.

## SCC relation

M8 SCCs are included as component membership evidence. M9 does not equate one SCC with one package.

A recursive SCC is currently OPEN until a separate cycle identity proof exists, so any entrypoint reaching such a component is OPEN as well.

## M10 module-context refinement

M10 resolves relative-import syntax from the source module/package context and preserves both the structural observation and the package-qualified dependency target.

Example:

```python
# pkg/main.py
from .helper import helper

def main():
    return helper()
```

M7 may structurally observe `helper.helper`; M10 derives `pkg.helper.helper`, and M8 can resolve that exact internal target. The resulting M9 bundle can therefore include the actual helper occurrence rather than remaining falsely OPEN.

M10 also gathers imports across the whole AST, including imports that appear inside functions, so runtime-only dependency declarations are not omitted from the derived dependency manifest.

## Runtime output

The existing `ciel-function-identity` report includes:

```text
module_context_dependencies.schema = CIELPC_MODULE_CONTEXT_DEPENDENCIES_V1
entrypoint_dependency_bundles.schema = CIELPC_ENTRYPOINT_DEPENDENCY_BUNDLES_V1
entrypoint_dependency_bundles.thresholds = []
```

Each bundle records:

- entrypoint name;
- declared and qualified target;
- state;
- target occurrence and relational invariant when closed;
- exact reachable occurrences;
- qualified symbols;
- M8 component IDs;
- environment anchors;
- pinned distribution requirements;
- explicit blockers.

Authority remains:

`DERIVED_READ_ONLY_NO_AUTOMATIC_PACKAGE_REWRITE`.

## Remaining debt

- live runtime/global binding proof is separate from static source closure;
- recursive SCC identity remains OPEN pending cycle proof;
- exact bundle identity/deduplication is not yet implemented;
- generation of installable manifests from CLOSED bundles remains read-only future work.

## Next derivations

1. canonical identity for recursive SCCs;
2. bundle identity hash over target relational identity + exact closure + environment anchors;
3. exact equality-based deduplication of build/runtime bundles;
4. optional generation of dependency manifests from CLOSED bundles, still without automatic apply;
5. optional runtime namespace probe for live-binding validation.
