# Knowledge-to-Action System Canon

## Purpose

This document defines the canonical NOEMA knowledge-to-action subsystem.
It is a thin orchestration layer, not a new theory engine.

The system combines:
- retrieval from local NOEMA evidence,
- CIELingo semantic interpretation,
- Doctor diagnostics,
- policy gating,
- Sapiens/UI rendering.

The design goal is reliability first:
- read-only analysis before execution,
- explicit evidence before action,
- a single decision path,
- no hidden fallback logic.

## Canonical flow

```mermaid
flowchart LR
    A[Input text<br/>φ[ingest]] --> B[Retriever<br/>φ[retrieve]]
    B --> C[CIELingo<br/>φ[meaning]]
    C --> D[Doctor<br/>φ[diagnose]]
    D --> E[Policy Kernel<br/>φ[decide]]
    E --> F[Executor Hint<br/>φ[act]]
    E --> G[Sapiens View<br/>φ[explain]]
    G --> H[UI<br/>φ[render]]

    B -. evidence .-> C
    C -. phase frame .-> D
    D -. health state .-> E
    E -. trace .-> H
```

The Mermaid diagram is intentionally compact so it can be rendered in plain Markdown viewers and in interactive renderers.

## Roles

### Retriever

Collects local evidence from NOEMA without mutating state:
- wave archive hits,
- chat history hits,
- memory context bundle.

### CIELingo

Converts text into a structured semantic frame:
- concept tokens,
- operator tokens,
- phase metadata,
- projection confidence,
- composition validity.

### Doctor

Evaluates codebase and runtime health:
- manifest integrity,
- closure/error signals,
- static findings,
- overall status.

### Policy Kernel

Turns evidence into a bounded decision:
- `allow`
- `defer`
- `repair`
- `block`

The policy kernel should stay deterministic and conservative.

### Sapiens/UI

Builds the human-facing trace:
- what was retrieved,
- what CIELingo understood,
- what Doctor reported,
- what policy decided,
- what the next step should be.

## Public surface

The canonical module is:

- `src/ciel_sot_agent/knowledge_action_system.py`

Its public entrypoints are:
- `collect_retrieval_bundle()`
- `build_policy_bundle()`
- `score_action()`
- `build_ui_bundle()`
- `run_knowledge_action_system()`
- `KnowledgeActionSystem`

## Failure modes

- Missing evidence should not force action.
- Invalid composition should route to `repair`.
- Binding or policy violations should route to `block`.
- Safe/read-only mode should not pretend to execute.
- Empty retrieval should not be silently upgraded to confidence.

## Implementation rule

The first version of this system is analysis-only.
Execution is a future port and must be added as an explicit, separately testable step.
