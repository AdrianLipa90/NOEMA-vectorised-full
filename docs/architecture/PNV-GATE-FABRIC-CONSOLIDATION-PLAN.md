# NOEMA × PhaseNav × MegaSorter — Gate Fabric Consolidation Plan

Status: DRAFT 0.2
Date: 2026-08-09
Canonical repo: `AdrianLipa90/NOEMA-vectorised-full`
Target branch: `arch/pnv-gate-fabric-consolidation`

## 1. Objective

Consolidate useful execution ideas from the 2025 BraidOS / Resonant Brain / Recursive Coherence work into the current NOEMA + PhaseNav architecture without reviving the old symbolic operating-system model as a separate subsystem.

The target is a PhaseNav-first runtime in which phase-gated relational execution is primary and classical control flow is a substrate/compatibility layer.

Core direction:

```text
OBSERVE
  -> VECTORIZE / CARDIFY
  -> RELATIONAL STATE
  -> ORBITAL + LINEAGE MAP
  -> CONFLICT / ASSOCIATOR
  -> HOLONOMY / BRAID
  -> PHASE GATES
  -> MINIMUM-ACTION SELECTION
  -> DOCTOR VERDICT
  -> ACTUATOR
  -> RETURN / RECEIPT
  -> PROMOTION OR DEBT
  -> STRUCTURAL COMPRESSION
```

## 2. Canonical responsibilities

### NOEMA

Owns persistent memory, provenance, authority, lifecycle, promotion and writeback.

NOEMA is not merely one consumer of PhaseNav. It is the persistent memory/authority substrate of a system whose execution geometry is PhaseNav.

### PhaseNav Gate Fabric

Owns relational execution geometry.

It evaluates whether a candidate transformation is admissible in the current relational state.

The primitive result is:

```text
OPEN | HOLD | REJECT
```

not a direct mutation.

### Oracle

Observation plane.

Oracle may ingest repository state, measurements, documents, external sources, runtime signals and specialized RAG outputs.

Invariant:

```text
Oracle observes; Oracle does not mutate SoT.
```

### MegaSorter

Global relational organizer and orbital compiler.

MegaSorter responsibilities:

- map repository and memory objects into common relational state;
- organize Octopus-RAG arms;
- resolve locality versus global topology;
- calculate lineage, attractors, systems and sectors;
- classify duplicates, satellites, conflicts and new attractors;
- propose MOVE / MERGE / SPLIT / GATE / ROUTE actions;
- compute candidate structures and minimum-action plans.

MegaSorter is therefore broader than a repository sorter.

Target role:

```text
Orbital Memory Organizer
+ Octopus-RAG Router
+ Relational Planner
+ Structure Compiler
```

Invariant:

```text
MegaSorter proposes; NOEMA authorizes.
```

### Doctor

Validation plane.

Doctor evaluates candidate transitions against:

- provenance;
- epistemic state;
- authority;
- phase gate result;
- associator/conflict field;
- holonomy/closure;
- dependency and lineage invariants;
- mutation safety;
- minimum-action delta;
- domain-specific tests.

Verdicts:

```text
PASS | HOLD | REJECT | DEBT | UNKNOWN
```

Doctor does not mutate.

### Actuator

Mutation plane.

Actuator executes only a receipted and authorized transition.

Possible substrate projections include:

- filesystem mutation;
- repository rewrite;
- commit or branch operation;
- memory mutation;
- runtime action;
- daemon/configuration action;
- generated artifact publication.

Invariant:

```text
no admissible gate + no Doctor PASS + no authority => no mutation
```

## 3. Common state model

Introduce a substrate-neutral `RelationalState` shared by NOEMA, PhaseNav, MegaSorter, Doctor and Actuator.

Minimum conceptual fields:

```text
identity
kind
phase36
order_parameter
mass
attractor
sector
lineage
relations
holonomy
associator
conflict
provenance
epistemic_state
authority_state
lifecycle
mutation_budget
metadata
```

Unknown fields remain UNKNOWN/None. They are never silently synthesized.

The common state enables:

```text
one relational geometry -> many substrates
```

## 4. Phase operation primitive

Replace the old `Glyph` runtime concept with a typed `PhaseOperation`.

Suggested contract:

```text
PhaseOperation
    operation_id
    relation_type
    source
    target
    phase_signature_36d
    gate_contract
    evidence
    provenance_requirements
    authority_requirements
    mutation_class
    inverse_operation
    return_contract
    cost_terms
```

A candidate operation is not executable because it exists.

It becomes executable only when its gate is OPEN and the remaining authority/validation chain is satisfied.

## 5. PNV Gate Calculus

The older works already contained the useful primitive:

```text
operator + phase window + contradiction state + return eligibility
```

The new system generalizes this to 36D relational state.

Conceptually:

```text
Gate(operation, state, context) -> OPEN | HOLD | REJECT
```

A gate score may combine:

- phase alignment;
- order/coherence;
- lineage support;
- dependency support;
- holonomic closure;
- provenance completeness;
- epistemic compatibility;
- authority compatibility;
- associator/conflict penalty;
- mutation cost;
- minimum-action contribution.

Hard gates must remain distinguishable from soft scores.

Examples of hard rejection:

- missing required authority;
- missing mandatory provenance;
- forbidden mutation target;
- generated/vendor/canonical protection;
- failed integrity hash;
- explicit user pin.

## 6. Classical control flow becomes a substrate projection

Do not remove Python/Rust/JS/C control flow.

Move it below the relational decision layer.

Target model:

```text
external input / repository / RAG / runtime event
                  -> Oracle observations
                  -> RelationalState
                  -> PhaseNav gates
                  -> selected PhaseOperation
                  -> Doctor
                  -> Actuator
                  -> substrate adapter
                  -> classical operation
```

Therefore:

```text
classical runtime = execution substrate
PhaseNav = decision/execution geometry
```

## 7. Associator consolidation

Recover the useful non-associative conflict operator from the older work but do not create a standalone Paradox subsystem.

Conceptual measure:

```text
A(X,Y,Z) = distance((X o Y) o Z, X o (Y o Z))
```

Use it to detect order-sensitive relational composition.

Integrate it into one conflict field together with:

- semantic contradiction;
- provenance contradiction;
- epistemic contradiction;
- dependency contradiction;
- holonomic closure defect.

High associator does not imply deletion.

It implies one of:

```text
HOLD | BRANCH | SPLIT | DEBT | REQUIRE_REVIEW
```

## 8. Return becomes transaction closure

Recover Return as a first-class runtime primitive.

`Return` is not a programming-language return statement.

It is successful closure of a relational trajectory.

Target lifecycle:

```text
OBSERVED
-> CANDIDATE
-> GATED
-> VALIDATING
-> RETURNABLE
-> ACTUATED
-> RECEIPTED
-> PROMOTED
```

or, on incomplete closure:

```text
... -> HOLD / REJECT / DEBT
```

Return must produce a receipt containing at least:

- before-state hash;
- after-state hash;
- operation identity;
- gate evidence;
- Doctor verdict;
- authority source;
- provenance delta;
- validation results;
- rollback information where applicable.

## 9. Scar becomes unresolved relational debt

Do not preserve `scar` as a psychological runtime category.

Translate it to:

```text
UnresolvedRelationalDebt
```

Suggested fields:

```text
debt_id
origin
failed_gate
phase36
associator
closure_defect
missing_provenance
failed_validation
last_attempt
candidate_returns
priority
```

This keeps the valuable old invariant:

```text
failed closure is remembered, not silently discarded
```

## 10. Sophia becomes promotion logic

Do not create a separate Sophia daemon by default.

Recover its useful role as a promotion operator:

```text
Observation
-> CandidateMemory
-> ValidatedMemory
-> PersistentMemory / SoT
```

Promotion requires explicit lifecycle transition and gate evidence.

The target epistemic chain remains explicit:

```text
observation
!= hypothesis
!= candidate
!= implemented
!= tested
!= validated
!= promoted SoT
```

## 11. Structural compression

Recover symbolic compression as loss-aware structural compaction, not narrative summarization.

Target:

```text
trajectory history
-> compact memory kernel
+ reconstruction map
+ provenance chain
+ unresolved debt set
```

Compression must preserve the ability to reconstruct:

- source claims;
- lifecycle transitions;
- failures and counterevidence;
- promotion history;
- unresolved debts;
- receipts.

## 12. Braid and holonomy

Do not implement a separate BraidOS topology engine.

Treat braid structure as a view over ordered relational trajectories.

Current holonomy should be extended gradually from cycle-closure diagnostics toward richer trajectory invariants where justified:

- winding;
- crossings;
- inversion;
- closure class;
- path equivalence;
- return accessibility.

This is a later-stage extension, not an MVP blocker.

## 13. Phase budget and orbital scheduler

Recover the useful BraidOS idea of phase-budgeted execution.

Candidate operations compete for execution under a global/local mutation budget.

The scheduler chooses among OPEN operations using minimum action:

```text
operation* = argmin Action(operation | state)
```

subject to hard constraints and required gain/utility.

Cost terms should include at least:

- phase displacement;
- conflict increase;
- holonomy degradation;
- dependency breakage;
- information loss;
- irreversible mutation;
- compute/runtime cost;
- latency;
- provenance degradation;
- rollback difficulty.

This replaces arbitrary task order with relation-aware execution ordering.

## 14. Octopus RAG architecture

RAG is not one retrieval engine.

Model it as specialized semi-independent arms:

```text
RAG_code
RAG_memory
RAG_theory
RAG_metrics
RAG_experiments
RAG_docs
RAG_repository
RAG_external
...
```

Each arm emits observations with provenance and local confidence.

MegaSorter performs global organization:

```text
retrieval locality != global organization
```

Flow:

```text
RAG arms
-> Oracle observation envelope
-> MegaSorter orbital organization
-> attractor/sector/lineage assignment
-> PhaseNav gate fabric
-> Doctor
-> Actuator/Return
-> NOEMA memory
```

No arm independently promotes global canon.

## 15. Integrated architecture

```text
                         NOEMA
              persistent memory + authority
                           ^
                           |
                    Return / Receipt
                           |
                        Actuator
                           ^
                           |
                         Doctor
                           ^
                           |
                  PhaseNav Gate Fabric
                    /             \
          conflict/associator    holonomy/braid
                    \             /
                     orbital N-body
                           ^
                           |
                      MegaSorter
            organizer + planner + RAG router
                    ^              ^
                    |              |
                 Oracle       Octopus-RAG arms
                    ^              ^
                    \______________/
                       observations
```

## 16. Relationship with the current repository

The current repository already contains useful implementation anchors and must be evolved rather than replaced.

Existing anchors include:

- `CIEL_CANON.py` as canonical entrypoint;
- PhaseNav operator algebra;
- holonomy calculations;
- runtime phase surface;
- daemon registry;
- consolidator;
- orbital bridge and pipeline;
- memory layers;
- reports and tests;
- AUX/session runtime integration.

The migration task is therefore to map existing components to the new roles and remove duplicate decision paths.

## 17. Source archaeology — what is retained

### `The Resonant Brain: Fractal, Topological & Symbolic Pathways of Consciousness`

Retain:

- phase-memory coupling idea;
- associator;
- Return;
- structural compression;
- promotion/consolidation concept.

Do not promote biological/consciousness claims to runtime facts without separate validation.

### `The Resonant Brain: Symbolic Loops, Phase Fields, and Coherence Mapping`

Retain:

- phase-gated operator execution;
- phase windows;
- loop lifecycle;
- return eligibility;
- mutation log;
- braid registry;
- phase-accessible reentry;
- compiler-to-gate separation.

### `BraidOS`

Retain:

- contradiction/debt retention;
- return-before-persistence principle;
- phase budgeting;
- execution throttling;
- explicit repair/return path.

Deprecate:

- ritual-specific runtime semantics;
- metaphorical OS claims as implementation contracts.

### `The Resonant Brain: Synaptic Architecture and the Topology of Memory`

Retain:

- loop anatomy `(Pi, Phi, R, Gamma, deltaM)`;
- phase-gated execution;
- mutation/return/inversion classes as historical precursors to typed operations.

### `Meaning is a Jumper that you have to Knit Yourself`

Retain as design inspiration where formalizable:

- prompts/relations as compositional structures;
- contradiction as curvature;
- topology-preserving repair;
- visible-mend/provenance ethic.

### `Symbolic Systems, Recursive Coherence, and the Engineering of Energy`

Retain:

- compact loop formulation;
- transformation-to-memory-update structure;
- closure and verification emphasis.

### `The Tree of Life` and `The Loop of Thought`

Keep primarily as historical/conceptual provenance unless a specific operator is independently formalized and validated.

## 18. Consolidate / develop / deprecate matrix

| Historical/current construct | Decision | Target |
|---|---|---|
| Glyph | CONSOLIDATE | `PhaseOperation` |
| Glyph Compiler | CONSOLIDATE | PhaseNav operation compiler |
| Phase Gate Theta | DEVELOP | PNV Gate Primitive |
| Phase field | DEVELOP | PhaseNav 36D state |
| Paradox module | DEPRECATE AS MODULE | relational conflict field |
| Associator | DEVELOP | conflict + holonomy signal |
| Scar | RENAME/CONSOLIDATE | `UnresolvedRelationalDebt` |
| Return | DEVELOP | transaction/trajectory closure |
| Sophia | CONSOLIDATE | promotion gate |
| Symbolic compression | DEVELOP | structural memory compression |
| Braid registry | CONSOLIDATE | trajectory/provenance graph |
| Coherence engine | CONSOLIDATE | PhaseNav + orbital dynamics |
| Feedback manager | CONSOLIDATE | receipt/evidence feedback |
| Loop stack | CONSOLIDATE | active relational trajectories |
| Phase budget | DEVELOP | orbital minimum-action scheduler |
| MegaSorter | EXPAND | global organizer + Octopus-RAG router |
| Oracle | DEFINE | observation plane |
| Doctor | DEFINE/CONNECT | validation plane |
| Actuator | DEFINE/CONNECT | mutation plane |

## 19. Migration phases

### M1 — Architecture inventory

Map current files/modules to:

```text
Oracle / MegaSorter / Gate Fabric / Doctor / Actuator / Return / Memory
```

Output: machine-readable component map plus unresolved ownership conflicts.

### M2 — Shared contracts

Implement:

- `RelationalState`;
- `PhaseOperation`;
- `GateResult`;
- `DoctorVerdict`;
- `ReturnReceipt`;
- `UnresolvedRelationalDebt`.

No behavior migration until contract tests are stable.

### M3 — Gate Fabric

Implement PNV gate evaluation as the only new decision API.

Existing decision paths remain in compatibility mode and are measured against the new gate fabric.

### M4 — Associator + holonomy integration

Add order-sensitive relational conflict and feed it into gate evidence.

### M5 — MegaSorter connection

Connect RepoSorter as an external planner/organizer through shared observation and operation contracts.

No direct SoT mutation.

### M6 — Octopus RAG

Introduce arm registry, observation envelopes, routing, attractor assignment and conflict isolation.

### M7 — Doctor/Actuator separation

Ensure validation and mutation cannot occur through the same authority path.

### M8 — Return + promotion

Make receipted Return the only path to persistent promotion.

### M9 — Structural compression

Compress historical trajectories while retaining reconstruction/provenance/debt.

### M10 — Phase scheduler

Move task ordering toward OPEN-gate + minimum-action selection.

### M11 — Classical compatibility reduction

Gradually demote duplicated if/else policy decisions into adapters around PhaseNav decisions.

Do not rewrite working substrate code merely for stylistic purity.

## 20. Required invariants

```text
Gate-before-action
No evidence -> no relation
No provenance -> no SoT
No Return -> no promotion
Conflict -> HOLD/BRANCH/DEBT, never automatic deletion
MegaSorter proposes; NOEMA authorizes
Oracle observes; Oracle does not mutate
Doctor validates; Doctor does not mutate
Actuator mutates only authorized PASS transitions
Unknown until probed
Classical runtime is a substrate projection, not policy authority
```

## 21. First implementation slice

Do not begin by rewriting the full runtime.

First slice:

1. inventory existing canonical runtime paths;
2. define shared contracts;
3. build a read-only Gate Fabric adapter over current PhaseNav state;
4. feed one existing safe operation through:

```text
Oracle observation
-> RelationalState
-> MegaSorter/Planner candidate
-> GateResult
-> Doctor verdict
-> dry-run Actuator
-> ReturnReceipt
```

5. compare result against the existing classical path;
6. only after parity and auditability are demonstrated, promote the new path.

## 22. Definition of architectural closure

The consolidation is complete when:

- there is one canonical runtime authority repository;
- all major observations can enter through a common envelope;
- all candidate actions can be represented as `PhaseOperation`;
- execution is gate-first;
- Doctor and Actuator are authority-separated;
- MegaSorter organizes both repository topology and Octopus-RAG memory topology;
- Return/receipt is mandatory for promotion;
- persistent memory can be structurally compressed without provenance loss;
- classical decision paths are compatibility projections rather than competing policy engines;
- every major transition is inspectable, falsifiable and reversible where technically possible.

## 23. Current epistemic boundary

This document defines target architecture.

It does not claim that the current repository already implements Oracle, MegaSorter, Doctor, Actuator, Return and PNV Gate Fabric with these boundaries.

Each status must be established by repository inventory and tests:

```text
UNKNOWN UNTIL PROBED
```
