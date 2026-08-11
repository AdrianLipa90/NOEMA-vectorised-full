# M11 — Exact Bundle Identity

## Status

IMPLEMENTED CANDIDATE on top of M8–M10. Read-only. No deduplication apply, source deletion, manifest installation, CANON promotion, CURRENT update, or Actuator action.

## Goal

M9 derives one exact execution dependency closure per declared entrypoint. M11 answers the next question without introducing a package-name convention:

> When are two derived bundles the same bundle?

The answer is exact equality of a canonical closed relational graph invariant.

## Non-identity fields

The following fields are deliberately **not** identity-bearing:

- entrypoint name;
- source file path;
- filesystem folder;
- Python package directory name as presentation;
- upload/commit order;
- similarity score.

Those values remain provenance or presentation data but do not define bundle identity.

## Identity-bearing graph

For a CLOSED M9 bundle, M11 derives:

1. target relational function invariant;
2. multiset of all reachable CLOSED relational function invariants;
3. multiset of INTERNAL edges represented as `(source_relational, target_relational)`;
4. multiset of ENVIRONMENT edges represented as `(source_relational, environment_anchor)`;
5. exact pinned external requirements.

Multisets preserve multiplicity while avoiding source-path dependence.

The canonical payload is hashed with SHA-256 under schema:

`CIELPC_ENTRYPOINT_BUNDLE_IDENTITY_V1`.

The public identity is:

```text
bundle:<sha256>
```

## Why the graph is included

A set of functions alone is insufficient. The same nodes can be connected differently.

Therefore bundle identity contains edge multiplicities as well as node multiplicities. Two closures with the same relational identities but different dependency topology do not become the same bundle.

## Alias/path invariance

If two entrypoints in different modules have relationally equivalent target/helper functions and the same dependency topology, their source paths and entrypoint names may differ while the M11 bundle identity remains equal.

This is intentional:

```text
representation difference != bundle identity difference
```

provided the M8 relational identities and the complete closed dependency graph are equal.

## OPEN rule

Only a CLOSED M9 bundle can receive an M11 identity.

If the bundle is OPEN, UNRESOLVED, AMBIGUOUS, or INVALID:

```text
bundle_invariant = null
bundle_id = null
state = OPEN
```

Missing proof is never replaced by a provisional hash that could later be mistaken for identity.

## Consistency checks

Even for an input marked CLOSED, M11 independently verifies:

- every reachable occurrence has a CLOSED relational identity;
- every INTERNAL edge stays inside the bundle closure;
- every INTERNAL target has a CLOSED relational identity;
- every ENVIRONMENT edge has an anchor;
- no non-closed binding exists inside the claimed CLOSED bundle;
- the target has a CLOSED relational identity.

Any inconsistency downgrades identity derivation to OPEN with blockers.

## Equivalence groups

M11 groups only `DERIVED` bundle identities by exact `bundle_invariant` equality.

An equivalence group contains:

- one bundle ID;
- all entrypoint names that derive that same identity;
- the exact requirement tuple.

This is a **deduplication proposal surface**, not an apply operation.

## CLI

The existing report gains:

```text
bundle_identities.schema = CIELPC_ENTRYPOINT_BUNDLE_IDENTITY_V1
bundle_identities.thresholds = []
```

with:

- one identity record per entrypoint;
- exact node/edge multisets;
- requirements;
- blockers;
- equivalence groups.

Authority:

`DERIVED_READ_ONLY_NO_AUTOMATIC_DEDUP_APPLY`.

## Epistemic scope

M11 inherits the M8/M10 static-source scope. Equal M11 IDs prove equality of the derived static execution dependency graph under the supplied environment anchors. They do not independently prove that a mutable live Python namespace has not changed.

## Next derivation

An M11 equivalence group is sufficient to derive a read-only install/build manifest exactly once per unique bundle identity. That manifest should be content-addressed by the bundle ID and remain unapplied until an explicit Actuator-authorized step.
