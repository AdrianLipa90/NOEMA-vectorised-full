# NOEMA Private Repository Vectorization v0.9

This append-only layer records the first complete private-repository snapshot routed through PhaseNav without repository-name, path, size, branch, repository-id, or manually assigned importance seeds.

## Canonical parent

PhaseNav merge:

`2cf1e433e21f4f3feab2f248218a38f5263e66ea`

Hard canon `1.4.0`, package `0.7.0`, Git-object vectorizer `0.9.0`.

## Snapshot

- 40 private repositories inventoried mechanically;
- 39 real Git heads;
- 39 unique 36D repository-state vectors;
- one archived empty repository with no invented vector.

Inventory SHA-256:

`d47ace603e52fdb3fbe77556b370ac272d4ac5f3d0232b0bda4fbc998a05ab70`

Vector-set SHA-256:

`a7e458063b3fb94d817f132c3c4dceee5a6ed7ade32237bec4acaff392640e0b`

## Source-of-vector rule

The numerical parent is the native Git object digest itself:

- commit for repository/history state;
- tree for directory state;
- blob for file state;
- annotated tag for tag state.

Human-readable repository names and paths remain aliases/localizers only. No separate string hash is inserted into the Git-content route.

## Relations

Containment/import/dependency relations do not receive fabricated vectors from their labels. Their geometry is computed from actual endpoint object vectors; relation labels and parse receipts remain evidence metadata.

## NOEMA boundary

NOEMA stores the snapshot identity, exact PhaseNav parent, aggregate hashes, and policy. It does not duplicate every vector because the complete vector set is deterministically reconstructible from the PhaseNav snapshot and Git object heads.

Historical v0.8 receipts remain immutable. v0.9 supersedes label-derived seeding only for Git content identity.

Vectorization does not promote mathematical, physical, semantic, or provenance claims.