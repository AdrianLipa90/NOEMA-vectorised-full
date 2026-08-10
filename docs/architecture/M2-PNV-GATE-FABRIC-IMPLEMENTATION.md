# M2/M3 — PNV Gate Fabric Implementation State

Status date: 2026-08-10
Branch: `arch/pnv-gate-fabric-consolidation`
Base: canonical `master`
Mode: **PLAN_ONLY / NO LIVE ACTUATION**

## 1. Epistemic status

This document separates four states:

- **IMPLEMENTED** — code exists on the branch.
- **TEST-SPECIFIED** — executable regression/contract tests exist in the repository.
- **VALIDATED** — tests actually executed and returned a code-level PASS.
- **PROMOTED** — merged/promoted into canonical `master`/runtime SoT.

Current branch status:

- architecture: IMPLEMENTED;
- core contracts: IMPLEMENTED;
- tests: TEST-SPECIFIED;
- GitHub Actions code verdict: **UNKNOWN / INFRA_BLOCKED** because workflow jobs terminate without executable step records;
- live Actuator: NOT IMPLEMENTED;
- promotion to `master`: NOT PERFORMED.

No component in this branch should be described as production-validated until an executable validation run exists.

## 2. Implemented architecture

The current reference flow is:

```text
Oracle / Octopus RAG
        ↓
RelationalObservation
        ↓
MegaSorter envelope
        ↓
candidate PhaseOperation
        ↓
PhaseNav Gate Fabric
OPEN / HOLD / REJECT
        ↓
Doctor
PASS / HOLD / REJECT / DEBT / UNKNOWN
        ↓
Return (dry-run in current slice)
        ↓
ReturnReceipt + optional RelationalDebt
        ↓
Promotion Gate / governed memory metadata
        ↓
HOLD until a real validated Actuator returns APPLIED
```

A separate minimum-action scheduler may rank only candidates that have already received Gate OPEN and Doctor PASS.

## 3. Common contracts — IMPLEMENTED

Module: `src/ciel_geometry/phasenav/gate_contracts.py`

Defines:

- `RelationalObservation`;
- `RelationalState`;
- `PhaseOperation`;
- `GateResult`;
- `DoctorVerdict`;
- `ReturnReceipt`;
- `UnresolvedRelationalDebt`;
- epistemic / observation / gate / doctor enums;
- explicit `PhaseSpace` labels.

Invariant:

**equal dimensionality does not imply equal coordinates.**

Current named spaces include:

- `OSCILLATOR_PHASE_36` — live mmap oscillator phase state;
- `PNV_PRECISE_PHASE_36` — canonical `M_sentence_phase_precise` compatible text/concept phase geometry;
- `OPERATOR_SIGNATURE_36` — operator feature/signature space;
- other spaces remain explicit and require registered metrics/projections.

No cross-space comparison is performed implicitly.

## 4. Canonical precise PNV36 kernel — IMPLEMENTED

Module: `src/ciel_geometry/phasenav/pnv_precise.py`

Consolidates the minimal substrate-neutral formula from `noema-phasenav-core` needed by NOEMA, Octopus RAG and MegaSorter:

- Collatz indexing hash;
- Decimal phase reduction;
- 36D precise sentence phase;
- circular order parameter;
- circular alignment / angular distance;
- project semantic-mass formula;
- explicit source descriptor.

Encoder id:

`PHASENAV_PNV_RUNTIME_CANON_PRECISE_V1`

This is a consolidated mathematically compatible kernel, not a claim of byte-identical implementation to every historical `pnv_runtime.py` revision.

## 5. Oracle — IMPLEMENTED FIRST ADAPTER

Module: `src/ciel_sot_agent/pnv_surface_oracle.py`

Reads the existing shared NOEMA surface without mutation and emits measured typed observations.

It preserves the actual current mmap slot contract and does not relabel memory/I/O/entropy channels as unrelated concepts.

`CIEL_CANON.py` now uses this typed adapter for status display.

Simulated synchronization noise remains explicitly non-canonical evidence.

## 6. Octopus RAG — IMPLEMENTED FIRST ARM

Module: `src/ciel_sot_agent/pnv_rag_arm.py`

Current arm:

`OCTOPUS_RAG:KNOWLEDGE_DB`

Evidence ranking:

- existing knowledge database / TF-IDF similarity is retrieval evidence;
- canonical precise PNV36 circular alignment is an additive geometric signal;
- legacy raw-angle cosine similarity is preserved for audit only and has no authority.

`scripts/noema_library_indexer.py` remains a legacy 24D migration utility. Its live `query_text()` compatibility path delegates to the typed RAG arm.

`CIEL_CANON.py --search` now calls the typed RAG arm directly.

## 7. MegaSorter bridge — IMPLEMENTED CANONICAL SIDE

Module: `src/ciel_sot_agent/pnv_megasorter_bridge.py`

Schema:

`NOEMA_MEGASORTER_ENVELOPE_V1`

Properties:

- neutral/versioned JSON-compatible envelope;
- deterministic SHA-256 identifiers;
- PNV precise nodes;
- evidence-bearing relations;
- no automatic result↔result relations merely because two results were co-retrieved;
- PLAN_ONLY authority;
- MegaSorter proposals become candidate operations, never actuator commands.

Critical invariant:

A MegaSorter proposal cannot create its own evidence from `confidence` or `reason`.

Inbound candidate evidence is resolved against relations in the originating NOEMA envelope. If no matching relation exists, the candidate has no evidence and Gate Fabric returns HOLD.

The external `NOEMA-Orbital-RepoSorter` consumer adapter has **not yet** been added. This repository currently implements the canonical producer/inbound contract only.

## 8. Gate Fabric — IMPLEMENTED

Module: `src/ciel_geometry/phasenav/gate_fabric.py`

Decision:

`OPEN | HOLD | REJECT`

Hard structural/authority violations reject.
Recoverable unknowns hold.

Required evidence applies to read-only and mutating operations.

Metric dispatch:

- angle spaces → circular phase alignment;
- feature/signature spaces → cosine similarity;
- unregistered spaces → HOLD;
- mismatched spaces → HOLD until an explicit projection exists.

Current scalar weights and thresholds are **project implementation parameters**, not physical constants. They require calibration before canonical policy promotion.

## 9. Doctor — IMPLEMENTED ADAPTER

Module: `src/ciel_sot_agent/pnv_doctor.py`

Uses the existing `integration.Orbital.main.RHController` as one diagnostic evidence provider.

Doctor:

- does not mutate;
- propagates Gate HOLD/REJECT;
- returns UNKNOWN if diagnostic evidence is unavailable;
- can allow read-only diagnostics under high RH severity;
- rejects/holds mutation according to current RH policy.

## 10. Associator — IMPLEMENTED DIAGNOSTIC

Module: `src/ciel_geometry/phasenav/associator.py`

Generic definition:

`A(x,y,z) = d((x∘y)∘z, x∘(y∘z))`

No assumption is made that every PNV algebra is non-associative.

The first concrete diagnostic measures parenthesization sensitivity introduced by lossy equal-weight pairwise phase compression. Its normalized defect can later enter `RelationalState.associator_defect` and Doctor evidence.

## 11. Return — IMPLEMENTED DRY-RUN ONLY

Module: `src/ciel_geometry/phasenav/return_protocol.py`

Current Return:

- hashes pre-state;
- records Gate and Doctor decisions;
- leaves state unchanged;
- emits `ReturnReceipt`;
- creates `UnresolvedRelationalDebt` if closure is not admissible;
- uses `actuator_status=DRY_RUN`;
- cannot promote SoT.

## 12. Promotion / Sophia consolidation — IMPLEMENTED ADAPTER

Module: `src/ciel_sot_agent/pnv_promotion.py`

Promotion is post-Return.

Durable promotion requires:

- Gate OPEN;
- Doctor PASS;
- Actuator APPLIED;
- after-hash;
- provenance;
- no unresolved debt.

The adapter produces `memory_governor` metadata for the existing governed holonomic memory orchestrator rather than creating a second memory governor.

Current dry-run receipts therefore always result in `HOLD_PROMOTION`.

## 13. Actuator boundary — IMPLEMENTED PERMIT, NO SIDE EFFECT

Module: `src/ciel_sot_agent/pnv_actuator.py`

This is the first formal Actuator boundary.

It does **not** execute a mutation.

It may only issue an immutable `ActuationPermit` when:

- operation is actually mutating;
- Gate is OPEN;
- Doctor is PASS;
- verdict ids bind to the same operation;
- source matches pre-state;
- evidence exists;
- provenance exists;
- required authority is supplied;
- Return is mandatory;
- initial policy requires reversibility.

Permit status remains:

`PREPARED_NOT_APPLIED`

No concrete filesystem, memory, Git, daemon, or network actuator has been attached.

## 14. Structural compression — IMPLEMENTED

Module: `src/ciel_geometry/phasenav/structural_compression.py`

Not free-text summarization.

Only structurally identical events may coalesce. It preserves:

- reconstruction map;
- provenance;
- parent lineage;
- event identity reconstruction;
- unresolved debt ids.

Pinned events and debt events never coalesce.
Duplicate event ids are rejected.

The compressor internally verifies exact normalized reconstruction.

## 15. Minimum-action phase scheduler — IMPLEMENTED

Module: `src/ciel_geometry/phasenav/phase_scheduler.py`

The scheduler cannot open a closed Gate and cannot override Doctor.

It ranks only Gate OPEN + Doctor PASS candidates using an explicit normalized action vector.

Cost terms currently include:

- phase displacement;
- dependency disruption;
- holonomy defect;
- associator defect;
- conflict;
- mutation cost;
- information loss;
- rollback cost;
- compute cost.

Current weights are project parameters requiring empirical calibration.
Tie-break is deterministic by operation id.

## 16. Full PLAN_ONLY reference cycle — IMPLEMENTED

Module: `src/ciel_sot_agent/pnv_cycle.py`

Connects:

`MegaSorter proposal → candidate → Gate → Doctor → dry Return → PromotionPlan`

Expected current terminal state:

`HOLD_PROMOTION`

because no concrete Actuator has executed.

## 17. Canonical CLI corrections — IMPLEMENTED

`CIEL_CANON.py` now:

- reads shared-surface status through the typed Oracle;
- displays current flavor slots with their actual meanings;
- reads closure from the holonomy surface field;
- no longer displays stale flavor slots as `closure`/`ethics`;
- performs search through the typed Octopus RAG arm;
- shows TF-IDF evidence score separately from PNV phase alignment.

## 18. Test specification

Dedicated test modules now cover:

- common gate contracts and phase-space invariants;
- space-aware gate metrics;
- live surface Oracle adapter;
- precise PNV36 kernel;
- Octopus RAG arm;
- MegaSorter envelope/evidence recovery;
- Doctor/Return PLAN_ONLY cycle;
- Promotion Gate;
- Associator diagnostics;
- guarded Actuator permit;
- reconstructible structural compression;
- gate-constrained minimum-action scheduler.

These tests are **TEST-SPECIFIED, not yet VALIDATED**.

## 19. Current CI verdict

The repository CI workflow contains a normal `ubuntu-latest` quality-gate job with executable steps.

For current PR runs, GitHub reports workflow failure while the job API returns no step execution records (`steps=null` / empty) and no job logs.

Classification:

`INFRA_BLOCKED / CODE_VERDICT_UNKNOWN`

Do not classify this as a code FAIL, and do not classify the implementation as PASS until a runner executes the tests.

## 20. Remaining work before live mutation

1. obtain a real executable validation run;
2. fix any actual code failures revealed by that run;
3. add the external MegaSorter consumer adapter for `NOEMA_MEGASORTER_ENVELOPE_V1`;
4. calibrate Gate and scheduler parameters on real repository/memory traces;
5. define explicit projections only where two PhaseSpaces genuinely correspond;
6. wrap exactly one reversible existing side effect behind `ActuationPermit`;
7. validate Return receipt + rollback + Promotion end-to-end;
8. only then consider promotion/merge into canonical `master`.

## 21. Current verdict

The PNV architecture is no longer only a plan. Its non-mutating control spine is implemented on the feature branch.

The branch is intentionally fail-closed at the final mutation boundary:

```text
OBSERVE
→ ORGANIZE
→ GATE
→ VALIDATE
→ PREPARE
→ [NO LIVE ACTUATION YET]
→ RETURN DRY-RUN
→ PROMOTION HOLD
```

This is the intended state until executable validation is available.