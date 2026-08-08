# NOEMA Private Repository Semantic Observation Boundary v0.11

This append-only layer records a strict separation between private Git content identity and semantic observations.

PhaseNav parent:

`6f55d48983b1bc3d2e786a68c5b7c33cedf7f543`

Hard canon `1.6.0`, package `0.9.0`, semantic observation contract `0.11.0`.

## Identity is already deterministic

The v0.9 snapshot mechanically inventoried 40 private repositories and produced digest-native 36D identity vectors for all 39 real repository heads. v0.10 added the native Git tree/blob scanner and frozen-head gates.

Git identity is not semantic similarity. A cryptographic digest vector is retained for routing/provenance only.

## Meaning is an observation, not a hash property

v0.11 binds exact Git blob bytes to the existing native CIEL semantic runtime:

- `Ciel-Semantic-Model-` release `0.8.1`, code `0a4a1b57217fc876ed0535829686cfed8ccd0d8f`;
- `cielingo-canon` runtime `ab097f99d46eb446836833ac90b2bc3cf9d219e1`;
- AUX request V2 / packet V3;
- native semantic state V1;
- 36D native spinor 4pi;
- 12 MemoryFabric lanes.

A valid observation binds exact blob identity plus request/packet, native semantic graph, MemoryReadSet and NOEMA receipts. The same blob may have multiple contextual observations without changing its Git identity vector.

## No arbitrary semantic collapse

No single intrinsic file-semantic vector is invented here. In particular:

- hash distance does not imply semantic similarity;
- repository/path/name/extension are not semantic parents;
- ASIR is not averaged into one ad-hoc file vector;
- missing CIEL receipts do not trigger filename/extension/hash fallbacks;
- binary/non-text blobs receive no invented text semantics.

## Current execution state

- private repo-head identity vectors: `COMPLETE_39_OF_39_REAL_HEADS`;
- complete frozen tree/blob scan across 39 private checkouts: `NOT_RUN`;
- private blob semantic observations through pinned CIEL runtime: `NOT_RUN`.

This distinction is intentional and append-only. NOEMA stores what is known and what remains unexecuted; it does not fill missing semantic state with guesses.