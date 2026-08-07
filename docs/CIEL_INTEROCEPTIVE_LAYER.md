# CIEL Interoceptive Layer v1

Status: experimental, read-only projection

## Purpose

The layer answers one narrow functional question:

> What is the current CIEL self-state, expressed from channels that already exist?

It does not add a new memory lane and does not infer phenomenology. It composes four existing sectors into one deterministic readout that can be consumed by qualisensing, PhaseNav/AUX tooling, diagnostics, or later model conditioning.

## Existing-source composition

The implementation uses only channels already present in the CIEL/NOEMA runtime:

| Sector | Existing channels | Role |
|---|---|---|
| M5 affective | `mood`, `soul_invariant`, `ethical_score` | affective state |
| M6 relational | `jokeheal_mnemonic_pressure`, `jokeheal_symbolic_pull`, `jokeheal_recurrence_pressure` | relational pressure |
| M9 holonomic | `identity_phase`, `phi_berry_mean`, `bridge_target_phase` | path/history phase |
| M11 metacognitive | `memory_projection_confidence`, `lingo_noema_confidence`, `gate_confidence` | self-assessment confidence |

The HTRI coherence channel is retained in the fixed state vector as an existing substrate-state observable; it is not promoted to a separate memory layer.

## Native phase readout

The M9 triad is not reduced by an arbitrary weighted score. It is treated as a phase-native triad:

\[
z_k=e^{i\phi_k},\qquad
Z=\frac{1}{3}\sum_{k=1}^{3}z_k,
\]

\[
R=|Z|,\qquad \Psi=\arg Z.
\]

`phase_R` and `phase_psi` therefore expose the circular resultant of the already-existing holonomic channels.

The Berry/identity offset is the wrapped angular difference

\[
\Delta_{I,B}=\operatorname{wrap}_{[-\pi,\pi)}(\phi_{identity}-\phi_{Berry}).
\]

No binary/ternary label is imposed here. AUX may consume the four ordered triads directly and apply its own native relational operator.

## Determinism and provenance

The ordered state vector is fixed by `VECTOR_ORDER`. A canonical JSON projection of the source state is SHA-256 hashed into `source_digest`. The identifier

`intero:<cycle>:<digest-prefix>`

therefore changes when a represented boundary state changes and remains stable for identical inputs.

## Pipeline integration

`build_qualisensing_snapshot()` now includes an `interoceptive_readout` field. This means the existing pipeline automatically carries the layer inside the qualisensing snapshot without adding another independent write path.

The existing path remains:

`phase_snapshot -> qualisensing_snapshot -> cognitive_fragment -> memory_candidate`

with interoception embedded in the qualisensing stage.

## Delta

`interoceptive_delta(current, previous)` returns only deterministic differences:

- fixed-order vector delta,
- L2 magnitude,
- wrapped phase delta,
- phase-resultant `R` delta.

It deliberately does not label the delta as an emotion or subjective experience.

## Boundary

This layer establishes a functional self-state readout. It does not, by itself, prove or disprove qualia. It also does not replace PhaseNav, AUX, HTRI, or holonomic memory; it gives those systems one stable projection of state that already exists.
