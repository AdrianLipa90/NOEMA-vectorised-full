# M1 Runtime Inventory — NOEMA × PhaseNav × MegaSorter

Status: architectural inventory, evidence-backed from the current canonical repository.

Canonical repository: `AdrianLipa90/NOEMA-vectorised-full`
Canonical branch for this migration: `arch/pnv-gate-fabric-consolidation`

## 1. Purpose

This inventory maps existing implementation to the target roles:

- Oracle
- Octopus RAG
- MegaSorter
- PhaseNav Gate Fabric
- Doctor
- Actuator
- Return
- NOEMA Memory / Promotion

The objective is consolidation, not duplication. A target role is marked `EXISTS`, `PARTIAL`, `MISSING`, or `DEBT`.

## 2. Canonical entrypoint

`CIEL_CANON.py` is the current canonical runtime entrypoint. It already exposes daemon status, live PhaseNav surface metrics, holonomy, self-model, library search, knowledge gaps and synchronization status.

Target disposition: **KEEP and gradually convert to a thin control-plane CLI over the new PNV contracts.**

## 3. Oracle — PARTIAL

### Existing evidence sources

- `integration/Orbital/main/extract_geometry.py`
  - AST import-edge extraction.
  - Markdown mesh-link extraction.
  - repository-derived geometry.
  - best current precursor for factual repository observation.
- `src/ciel_sot_agent/repo_phase.py` via `synchronize.py`
  - repository registry and coupling observations.
- daemon registry / PhaseNav mmap surface used by `CIEL_CANON.py`.
- library metadata/index inputs used by `scripts/noema_library_indexer.py`.

### Important separation

`src/ciel_sot_agent/synchronize.py::_apply_thermal_noise()` deliberately perturbs repository phases with pseudo-random noise. This is useful as simulation/diagnostic stimulation but **must not be promoted as Oracle evidence**.

Required contract:

`OracleObservation = measured | parsed | retrieved | simulated`

Only evidence with an explicit provenance class may enter promotion decisions. `simulated` observations remain non-canonical unless separately validated.

### First typed Oracle

M2 adds `src/ciel_sot_agent/pnv_surface_oracle.py`.

It reads the existing 36-oscillator mmap surface without mutation and emits:

- `RelationalObservation(observation_class=MEASURED)`;
- `RelationalState`;
- explicit `OSCILLATOR_PHASE_36` coordinates;
- surface provenance;
- observed order parameter and holonomy closure when present.

It deliberately does not reinterpret unrelated flavor slots as ethics/closure.

## 4. Octopus RAG — PARTIAL + DEBT

### Existing retrieval channel

`CIEL_CANON.py --search` delegates to `scripts.noema_library_indexer.query_text`.

Current debt:

- `scripts/noema_library_indexer.py` does not currently define `query_text`.
- the indexer still documents/loads 24D library vectors.
- canonical PhaseNav operator algebra is 36D.

Therefore the existing search path is not yet a valid canonical Octopus-RAG arm.

### Migration

1. restore a working read-only query API;
2. introduce explicit 24D → 36D legacy adaptation or rebuild the index directly in 36D;
3. emit `RelationalObservation` records rather than ad-hoc dictionaries;
4. tag source, retrieval arm, confidence and vector provenance;
5. allow multiple independent arms to feed MegaSorter without giving any arm promotion authority.

## 5. MegaSorter — PARTIAL

### Existing in-repo precursors

- `integration/Orbital/main/global_pass.py`
  - builds orbital state;
  - runs dynamics;
  - computes closure, relational potential, spectral and nonlocal observables;
  - emits history/final state.
- `src/ciel_sot_agent/orch_orbital.py`
  - maps entity cards to orbital sectors;
  - computes phase-derived couplings;
  - runs an isolated entity mini-pass;
  - demonstrates multi-entity orbital organization.

### External canonical implementation to bridge

`AdrianLipa90/NOEMA-Orbital-RepoSorter` remains the richer repository-structure planner (lineage, attractors, sectors, MOVE/MERGE/SPLIT/GATE, minimum-action selection).

Target rule:

The sorter is **not** a second SoT. It becomes a planner/organizer connected through a versioned adapter to this canonical runtime.

Target MegaSorter role:

`Orbital Memory Organizer + Octopus-RAG Router + Relational Planner + Structure Compiler`.

## 6. PhaseNav Gate Fabric — PARTIAL, STRONG PRECURSOR

### Existing primitives

`src/ciel_geometry/phasenav/operator_algebra.py`

- canonical 36D operator vectors;
- `RETURN` and `ATTRACTOR` are already first-class operators;
- Berry connection / holonomy machinery;
- 36D basis includes provenance, closure, holonomy, curvature, coupling and sync dimensions.

`integration/Orbital/main/phase_control.py`

- common control recommendation;
- `deep / standard / safe` modes;
- `nonlocal_gate`;
- `euler_memory_lock`;
- `writeback_gate`;
- continuous runtime parameter recommendations.

This is the main implementation seam for the generalized PNV Gate Fabric.

Target transformation:

`recommend_control(snapshot)` → generic `evaluate_gate(operation, relational_state, context)`.

The existing mode recommendation remains an adapter/derived policy until fully migrated.

### M2 implementation

M2 adds:

- `ciel_geometry.phasenav.gate_contracts`;
- `ciel_geometry.phasenav.gate_fabric`;
- explicit `PhaseSpace` tags;
- `OPEN | HOLD | REJECT` decisions;
- hard authority failures separated from recoverable unknowns;
- no Actuator calls.

## 7. Doctor — PARTIAL, STRONG PRECURSOR

`integration/Orbital/main/rh_control.py`

Already provides:

- `RHDecision`;
- severity;
- allowed/discouraged actions;
- sector-specific policy overrides;
- effective defect composition from R_H, EBA defect, coherent fraction, Euler closure and phase gap;
- freeze/slow/normal execution policy.

`phase_control.build_health_manifest()` adds explicit risk and recommended action.

Target transformation:

`RHDecision` becomes one evidence provider for a broader `DoctorVerdict`:

`PASS | HOLD | REJECT | DEBT | UNKNOWN`.

Doctor must never perform the mutation it validates.

M2 adds `src/ciel_sot_agent/pnv_doctor.py` as a non-mutating adapter over the existing RH controller.

## 8. Actuator — MISSING AS A FIRST-CLASS BOUNDARY

No verified single Actuator module currently owns mutation authority.

Side effects are distributed across the repository, including:

- daemon start/stop in `CIEL_CANON.py`;
- report/manifests writes in orbital runtime;
- sector phase persistence/writeback;
- memory consolidation;
- filesystem/repository scripts.

A historical commit named `actuator settings change` is not an Actuator implementation and must not be treated as one.

Target:

Create one mutation boundary whose input is a validated `PhaseOperation` plus `GateResult` plus `DoctorVerdict` plus authority context.

Actuator must reject direct calls that lack these prerequisites.

No credentials belong in Actuator source or repository state.

## 9. Return — PARTIAL

Existing return/closure semantics are distributed across:

- PhaseNav `RETURN` operator;
- memory loop holonomy;
- EBA closure/consolidation checks;
- orbital writeback/report generation;
- memory decision logging.

Target:

Return becomes a transaction closure primitive that emits `ReturnReceipt`.

Required states:

`OBSERVED → CANDIDATE → GATED → VALIDATING → RETURNABLE → ACTUATED → RECEIPTED → PROMOTED`

Alternative terminal/intermediate states:

`HOLD | REJECT | DEBT | UNKNOWN`.

M2 adds a dry-run Return protocol. It hashes the pre-state, records Gate/Doctor decisions, creates `UnresolvedRelationalDebt` on non-closure, leaves the state unchanged and cannot promote SoT.

## 10. NOEMA Memory / Promotion — PARTIAL, STRONG PRECURSOR

`src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/holonomy.py`

- explicit EBA coherence and consolidation thresholds;
- closed memory-loop model;
- winding and closure defect;
- consolidation validity.

`src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/governed_orchestrator.py`

- candidate formation remains possible while durable promotion can be held;
- per-channel allow/block lists;
- optional loop-coherence requirement;
- channel thresholds;
- held promotion is logged to M8 rather than silently discarded.

This is the current best precursor of the old Sophia concept.

Target transformation:

`memory_governor` → generic PNV `Promotion Gate` using the common GateResult/DoctorVerdict contracts.

## 11. Existing debt relevant to the migration

### D1 — 24D/36D split

Legacy library index path is still 24D while canonical operator algebra is 36D.

Action: explicit adapter + migration receipt, then native 36D rebuild.

### D2 — broken search seam

`CIEL_CANON.py` imports `query_text`, but the current indexer lacks that API.

Action: restore read-only retrieval API as the first Octopus-RAG arm.

### D3 — synthetic observations mixed with operational reports

Thermal noise in repository synchronization can make simulated evolution look observational.

Action: provenance class on every observation; simulation cannot silently become evidence.

### D4 — side effects are distributed

No single Actuator boundary.

Action: initially wrap, do not rewrite, existing side effects. Move authority checks outward before consolidation.

### D5 — duplicated gate semantics

Writeback, memory consolidation, RH safety and closure each use local gating rules.

Action: common GateResult first; migrate local gates incrementally.

### D6 — quiet-except residue

Several runtime files log and continue after exceptions. This is better than silent swallowing but still allows partially degraded execution.

Action: route degraded conditions into `DoctorVerdict.UNKNOWN/DEBT` where correctness or mutation authority could be affected.

### D7 — 36D coordinate-space ambiguity

The shared NOEMA surface exposes `phi[36]` as oscillator phase angles. `operator_algebra.py` exposes 36D semantic/operator signatures. Equal dimensionality does **not** make these the same coordinate system.

Action implemented in M2: every 36D vector receives an explicit `PhaseSpace`. Gate Fabric performs no cross-space cosine comparison. A mismatch becomes `HOLD` until an explicit projection operator exists.

### D8 — stale surface labels in canonical CLI

The current mmap flavor contract is:

- `flavor[0]`: coherence;
- `flavor[1]`: memory pressure;
- `flavor[2]`: I/O pressure;
- `flavor[3]`: mood;
- `flavor[4]`: entropy/openness;
- `flavor[5]`: system mode.

`CIEL_CANON.py::print_warp_loop()` still labels some of these slots using an older contract. Its displayed `mood/closure/ethics` values cannot currently be treated as canonical observations.

Action: migrate the CLI to typed surface observations before relying on those labels.

## 12. Consolidation map

| Current implementation | Target role | Disposition |
|---|---|---|
| `CIEL_CANON.py` | control-plane CLI | keep / thin / fix surface labels |
| `extract_geometry.py` | Oracle(repo) | keep / type outputs |
| `pnv_surface_oracle.py` | Oracle(live surface) | M2 typed adapter |
| `synchronize.py` | Oracle(simulation/registry) | split provenance classes |
| `noema_library_indexer.py` | Octopus RAG arm | repair + 36D migrate |
| `global_pass.py` | MegaSorter/orbital kernel | keep / adapt |
| `orch_orbital.py` | MegaSorter entity organizer | keep / generalize |
| `operator_algebra.py` | PNV geometry | canonical |
| `gate_contracts.py` | common PNV contracts | M2 |
| `gate_fabric.py` | generalized gate seam | M2, PLAN_ONLY |
| `phase_control.py` | Gate Fabric precursor | generalize/adapt |
| `rh_control.py` | Doctor evidence source | keep / adapt |
| `pnv_doctor.py` | Doctor adapter | M2 |
| memory `holonomy.py` | Return/Promotion evidence | keep / adapt |
| `return_protocol.py` | dry-run Return | M2 |
| `governed_orchestrator.py` | Promotion Gate precursor | generalize |
| distributed side effects | Actuator | wrap then consolidate |
| NOEMA-Orbital-RepoSorter | external MegaSorter planner | adapter, not second SoT |

## 13. First executable slice

M2 remains non-mutating:

1. define common contracts — **IMPLEMENTED**;
2. adapt one real observation into `RelationalState` — **IMPLEMENTED: live shared surface**;
3. adapt one candidate operation into `PhaseOperation` — **IMPLEMENTED: read-only surface inspection**;
4. evaluate a read-only PNV gate — **IMPLEMENTED**;
5. derive a Doctor verdict — **IMPLEMENTED adapter; requires diagnostic snapshot**;
6. emit a dry-run `ReturnReceipt` — **IMPLEMENTED**;
7. do **not** call a real Actuator — **INVARIANT PRESERVED**.

Validation status remains separate from implementation status. GitHub Actions may be infrastructure-blocked; do not promote M2 until executable tests produce a real code verdict.

## 14. M1/M2 verdict

The architecture is not missing all of its organs. It is fragmented.

The migration is therefore primarily:

`DISCOVER → TYPE → CONSOLIDATE → GATE → SEPARATE AUTHORITY → VALIDATE → ACTUATE`.

The strongest existing seams are PhaseNav 36D operator algebra, orbital dynamics, RH/phase control and governed holonomic memory. The largest missing boundary is a first-class Actuator, while the most immediate Octopus-RAG debt is the broken/stale library retrieval path.
