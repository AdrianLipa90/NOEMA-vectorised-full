---
name: ciel-transformer-interface
priority: 3
description: >
  >
---
# CIEL-Transformer Interface v1.9

## Contents

- **Four integration levels**: 1. **Feature sidecar**: keep the model unchanged; attach CIEL tensors to examples. 2. **Auxiliary tasks**: predict CIEL 

## Key Points

- concept vs operator distinction,
- operator class and arity,
- event-frame compatibility,
- case-gauge role reconstruction,
- scope and negation status,
- dynamic deixis anchors,
- ontological aspect such as identity/state and thing/concept,
- synonym phase coherence and antonym Euler phase,
- graph distance between concept/operator cards.

## Code

```
This repository does not train a transformer yet. v1.9 defines an interface and deterministic reference functions that can be used as preprocessing, auxiliary supervision, attention-bias generation, or post-generation validation.

## Four integration levels

1. **Feature sidecar**: keep the model unchanged; attach CIEL tensors to examples.
2. **Auxiliary tasks**: predict CIEL labels during training.
3. **Attention bias**: add structural bias to attention logits.
4. **Validator loop**: reject or 
```

---
*Extracted from: `src/ciel_lingophysics_lns_repo_v2_3/docs/36_CIEL_TRANSFORMER_INTERFACE.md` (44 lines, 1515B)*