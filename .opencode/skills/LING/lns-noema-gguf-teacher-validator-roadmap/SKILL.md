---
name: noema-gguf-teacher-validator-roadmap
priority: 3
description: >
  >
---
# NOEMA and GGUF Teacher-Validator Roadmap v2.1

## Contents

- **1. Roles**: ```text NOEMA       retrieval, routing, nonlocal card/operator access, local subgraph selection CIELingo    structured p
- **2. Non-goals**: This policy does not claim that a dense GGUF model executes only a selected subset of internal weigh - shorter context, 
- **3. Teacher-validator loop**: ```text CIELingo proposes analysis → local validator checks invariants → NOEMA checks graph consistency → if confidence 
- **4. Confidence policy**: ```text if local_confidence >= 0.85 and validator_pass and no_noema_conflict: do_not_call_gguf elif unresolved_scope_or_
- **5. Canonicality rule**: ```text GGUF verdict alone cannot make a card, relation, operator mapping, or translation canonical. ``` A canonical ite
- **6. Planned v2.2 implementation**: The next implementation patch should add: - `src/lingophysics/noema_index.py` - `src/lingophysics/noema_router.py` - `sr

## Key Points

- shorter context,
- fewer model calls,
- fewer repair retries,
- local graph/rule resolution,
- confidence-based escalation,
- possible future sparse/adapted execution.
- schema validity,
- card ontology validity,
- relation/invariant validation,
- diagnostic graph consistency,
- explicit status and audit trail,
- source/provenance or human review when factual.

## Code

```
## 2. Non-goals

This policy does not claim that a dense GGUF model executes only a selected subset of internal weights. A dense local model still usually runs full inference for generated tokens. Energy reduction is expected mainly from:

- shorter context,
- fewer model calls,
- fewer repair retries,
- local graph/rule resolution,
- confidence-based escalation,
- cache reuse,
- possible future sparse/adapted execution.

## 3. Teacher-validator loop
```

---
*Extracted from: `src/ciel_lingophysics_lns_repo_v2_3/docs/41_NOEMA_GGUF_TEACHER_VALIDATOR_ROADMAP.md` (73 lines, 2292B)*