---
name: implementation-roadmap
priority: 3
description: >
  >
---
# CIELingo Implementation Roadmap v2.1

## Contents

- **1. Repository direction**: CIELingo is not an ordinary dictionary project. It is a typed linguistic-physics system built from c Core rule: ```text 
- **2. Current baseline**: The current implemented local baseline is `v2.0 Diagnostic Geometry Layer`: - 72 concept cards across 5 languages: PL, E
- **P0 — Foundation complete, v0.6-v2.0**: Goal: establish the formalism, typed card layers, first concept batches, operator algebra, diagnosti Exit condition: loc
- **P1 — Roadmap and governance correction, v2.1**: Goal: define the staged plan and add the NOEMA-first / GGUF teacher-validator policy. Deliverables: - updated `docs/11_I
- **P2 — NOEMA Retrieval and Inference Gate, v2.2**: Goal: route a prompt to the smallest sufficient subgraph and avoid model calls when structural valid The gate must selec
- **P3 — GGUF Teacher-Validator Learning Loop, v2.3**: Goal: use GGUF/LLM as an advisory validator during learning and hard-case review, not as the canonic Rule: ```text GGUF 
- **P4 — CIELingo Validator Hardening, v2.4**: Goal: promote validators from file-level checks to semantic quality gates. Validator must catch false equivalences invol
- **P5 — Batch03 Controlled Expansion, v2.5**: Goal: add 20 concept cards × 5 languages using strengthened diagnostics. Batch size now decreases because dependency den

## Key Points

- 72 concept cards across 5 languages: PL, EN, DE, FR, ES.
- operator cards and operator algebra.
- case gauge, dynamic deixis, event frames, ontological aspect, TAM-E, scope/quantifier/negation.
- transformer interface skeleton with feature tensors, attention bias, auxiliary tasks, and validator loop.
- diagnostic geometry: cross-language reconstruction costs, operator density, relation matrices, conflict/unresolved registry.
- updated `docs/11_IMPLEMENTATION_ROADMAP.md`
- `docs/41_NOEMA_GGUF_TEACHER_VALIDATOR_ROADMAP.md`
- `data/roadmap/cielingo_stage_plan_v2_1.{json,yaml,csv}`
- `data/roadmap/gguf_teacher_validator_policy_v2_1.{json,yaml}`
- `data/roadmap/noema_inference_gate_policy_v2_1.{json,yaml}`
- roadmap schema, module and tests
- scope: `not every` vs `none`

## Tables

| Semantic dependency explosion | Decrease batch size, maintain relation deltas and unresolved registry. |
| GGUF over-trust | Keep GGUF verdict advisory, never canonical alone. |
| Manual seed treated as dictionary authority | Keep `curated_seed`, `draft`, `needs_review`, `unknown` statuses. |
| Cross-language flattening | Use case gauge, TAM-E, scope, event frames, ontological aspect and reconstruction costs. |
| Storage failure | Use JSON/JSONL fallback with explicit report. |
| Metaphorical language polluting claims | Keep repository documentation technical and auditable. |

## Code

```
## 2. Current baseline

The current implemented local baseline is `v2.0 Diagnostic Geometry Layer`:

- 72 concept cards across 5 languages: PL, EN, DE, FR, ES.
- operator cards and operator algebra.
- case gauge, dynamic deixis, event frames, ontological aspect, TAM-E, scope/quantifier/negation.
- transformer interface skeleton with feature tensors, attention bias, auxiliary tasks, and validator loop.
- diagnostic geometry: cross-language reconstruction costs, operator density, relation matrices
```

```
### P3 — GGUF Teacher-Validator Learning Loop, v2.3

Goal: use GGUF/LLM as an advisory validator during learning and hard-case review, not as the canonical source of truth.

Rule:
```

```
### P4 — CIELingo Validator Hardening, v2.4

Goal: promote validators from file-level checks to semantic quality gates.

Validator must catch false equivalences involving:

- scope: `not every` vs `none`
- case roles: `pies gryzie kota` vs `kota gryzie pies`
- operator duals: `Inside(x,y)` vs `Contains(y,x)`
- ontology: `ser` vs `estar`, `koto` vs `mono`
- unresolved deictic anchors

### P5 — Batch03 Controlled Expansion, v2.5

Goal: add 20 concept cards × 5 languages using strengthened diagnost
```

---
*Extracted from: `src/ciel_lingophysics_lns_repo_v2_3/docs/11_IMPLEMENTATION_ROADMAP.md` (169 lines, 5653B)*