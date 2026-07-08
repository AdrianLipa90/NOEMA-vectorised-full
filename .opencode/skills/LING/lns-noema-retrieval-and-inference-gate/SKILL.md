---
name: noema-retrieval-and-inference-gate
priority: 3
description: >
  >
---
# 43. NOEMA Retrieval and Inference Gate

## Contents

- **Principle**: ```text NOEMA routes first. CIELingo validates structurally. GGUF validates only when needed. ``` GGUF verdicts remain a
- **Pipeline**: ```text input query → tokenize / normalize → retrieve local NOEMA cards and operators → build routed context bundle → es
- **Gate levels**: ```text NO_LLM          resolved by cards/rules/validator SMALL_GGUF      low-risk phrasing or simple synthesis MEDIUM_G
- **Non-claim**: This layer does not claim that dense GGUF models execute only selected internal weights. Dense models usually still perf
- **Routing objects**: A NOEMA card is a lightweight routing entry referencing one or more canonical objects in the library. It may refer to co
- **Exit criteria for v2.2**: A valid v2.2 implementation must: 1. load a NOEMA index from JSON; 2. retrieve relevant cards for a query; 3. produce a 

## Code

```
GGUF verdicts remain advisory. They may increase confidence, reveal a conflict,
or request human review, but they cannot canonize a card or relation alone.

## Pipeline
```

```
## Non-claim

This layer does not claim that dense GGUF models execute only selected internal
weights. Dense models usually still perform dense inference. Energy reduction is
expected from reduced context, fewer model calls, cache reuse, routing, and
model-size gating. True partial model execution requires sparse routing,
Mixture-of-Experts, adapter gating, or modular specialist models.

## Routing objects

A NOEMA card is a lightweight routing entry referencing one or more canonical
objects in 
```

---
*Extracted from: `src/ciel_lingophysics_lns_repo_v2_3/docs/43_NOEMA_RETRIEVAL_AND_INFERENCE_GATE.md` (85 lines, 2634B)*