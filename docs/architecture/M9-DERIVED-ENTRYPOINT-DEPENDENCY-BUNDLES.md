# M9 — Derived Entrypoint Dependency Bundles

## Status

IMPLEMENTED CANDIDATE on top of M8. Read-only. No package rewrite, file relocation, dependency deletion, CANON promotion, CURRENT update, or Actuator action is introduced.

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

and derives everything reachable from that callable through the exact M8 binding graph.

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

A bundle is `CLOSED` only if every occurrence in its reachable closure is relationally CLOSED and every reachable call binding is INTERNAL or ENVIRONMENT.

Any unresolved, ambiguous, dynamic, recursive, or otherwise open dependency propagates into bundle blockers and makes the bundle `OPEN`.

This preserves the invariant:

```text
OPEN child -> OPEN execution bundle
```

rather than silently treating missing dependency proof as optional.

## External requirements

M9 does not rescan arbitrary declarations to guess a requirement. It reuses M8 environment anchors.

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

## Runtime output

The existing `ciel-function-identity` report gains:

```text
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

## Known debt

Relative imports are conservatively represented by the M7 structural scanner and are not yet fully normalized to their package-qualified target in every case. This can leave real local dependencies OPEN. It cannot justify a false CLOSED bundle, but it should be repaired by an exact module-context relative-import resolver before considering M9 complete across the whole repository.

## Next derivations

1. exact relative-import normalization using source module/package context;
2. canonical identity for recursive SCCs;
3. bundle identity hash over target relational identity + exact closure + environment anchors;
4. exact equality-based deduplication of build/runtime bundles;
5. optional generation of dependency manifests from CLOSED bundles, still without automatic apply.
