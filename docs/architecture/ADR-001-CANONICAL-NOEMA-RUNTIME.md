# ADR-001 — Canonical NOEMA Runtime Repository

Status: PROPOSED
Date: 2026-08-09
Owner: USER007 / Adrian Lipa

## Decision

`AdrianLipa90/NOEMA-vectorised-full` is the canonical private implementation repository for the integrated NOEMA runtime.

It is the primary implementation surface for:

- NOEMA persistent memory and authority;
- PhaseNav execution geometry and phase-gated routing;
- Oracle observation ingestion;
- MegaSorter relational/orbital organization and Octopus-RAG routing;
- Doctor validation and verdicts;
- Actuator-authorized mutation;
- Return, receipts, writeback, and promotion;
- runtime adapters and compatibility with classical control flow.

Specialized repositories such as `noema-phasenav-core`, `noema-orbital-memory`, `noema-holonomic-doctor`, `NOEMA-Orbital-RepoSorter`, and transport/interface repositories remain valid component repositories, laboratories, mirrors, or extraction targets, but they do not independently define the integrated runtime Source of Truth.

## Rationale

The repository already contains the canonical entrypoint `CIEL_CANON.py`, a live orbital/runtime bridge, PhaseNav operator algebra and holonomy hooks, memory/consolidation machinery, daemon coordination, reports, tests, and the current AUX/session integration trajectory. It therefore has the smallest architectural distance to the intended integrated system.

Creating another integration repository would duplicate authority and increase synchronization debt.

## Authority invariant

```text
component repository != integrated runtime authority
```

The integrated authority chain is:

```text
NOEMA persistent state
    -> PhaseNav gate fabric
    -> Doctor verdict
    -> Actuator authorization
    -> Return/receipt
    -> promotion/writeback
```

MegaSorter may propose structural or memory transformations but cannot promote them to SoT by itself.

Oracle may observe but cannot mutate.

Doctor may validate but cannot mutate.

Actuator may mutate only a transformation carrying the required gate, verdict, provenance, and authority.

## Branch policy

Architecture consolidation work starts on:

`arch/pnv-gate-fabric-consolidation`

No merge to the default branch is implied by this ADR.

## Epistemic status

This ADR is an architectural decision proposal. It does not by itself prove that every currently implemented runtime path already conforms to the target architecture. Existing implementation must be mapped and migrated incrementally.
