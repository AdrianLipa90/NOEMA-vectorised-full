# M12 — Content-Addressed Bundle Manifests

## Status

IMPLEMENTED CANDIDATE on top of M11. Read-only. No installation, environment mutation, package rewrite, CANON promotion, CURRENT update, or Actuator action.

## Goal

M11 groups entrypoints that derive one exact bundle identity. M12 derives exactly one dependency manifest per unique bundle group.

The manifest is content-addressed and does not acquire install authority merely by existing.

## Derivation

```text
M11 bundle equivalence group
  -> exact bundle_id
  -> exact pinned requirements
  -> declared requires-python constraint
  -> deterministic requirements payload
  -> requirements SHA-256
  -> manifest invariant
  -> manifest:<sha256>
```

No entrypoint name, source path, folder, similarity score, or package naming preference participates in manifest identity.

## Entrypoints are provenance, not identity

An M11 group may contain multiple entrypoint names. M12 keeps those names on the manifest as provenance, but excludes them from the manifest hash.

Therefore renaming a console command does not create a new dependency manifest when:

- the bundle ID is unchanged;
- the exact requirements are unchanged;
- the `requires-python` contract is unchanged.

## Identity-bearing fields

The manifest invariant contains:

- schema `CIELPC_DERIVED_BUNDLE_MANIFEST_V1`;
- `bundle_id`;
- `bundle_invariant`;
- exact `requires_python` declaration or null;
- sorted/deduplicated pinned requirement tuple;
- SHA-256 of the rendered requirements payload.

`requires-python` is identity-bearing because it changes the declared runtime compatibility contract even when the dependency graph is the same.

## Requirements payload

Requirements are rendered deterministically:

```text
sorted(unique(requirements))
```

with one requirement per line and a final newline when non-empty.

An empty requirement set renders to an empty byte string and still has an explicit SHA-256.

No comments containing entrypoint names are inserted into the requirements payload, because presentation metadata must not perturb dependency content identity.

## Authority

Every manifest carries:

`DERIVED_READ_ONLY_NO_INSTALL_AUTHORITY`.

A manifest is a reproducible plan/artifact, not an actuator command.

The following are explicitly outside M12:

- `pip install`;
- lockfile rewrite;
- environment creation;
- dependency removal;
- source relocation;
- package publication;
- NOEMA promotion.

## CLI

The existing report gains:

```text
bundle_manifests.schema = CIELPC_DERIVED_BUNDLE_MANIFEST_V1
bundle_manifests.thresholds = []
```

Each manifest record includes:

- bundle ID/invariant;
- manifest ID/invariant;
- entrypoint provenance;
- requirements;
- `requires-python`;
- requirements SHA-256;
- deterministic requirements text;
- read-only authority.

## Boundary to actuation

M12 completes the derivation side of the original dependency-package problem:

```text
source
-> function identity
-> relational closure
-> entrypoint execution bundle
-> exact bundle identity
-> unique content-addressed manifest
```

The next step is no longer another classification problem. It is an **actuation policy problem**: whether, where, and under what Gate/Doctor/Return conditions a derived manifest may be materialized or installed.

That boundary must remain explicit.
