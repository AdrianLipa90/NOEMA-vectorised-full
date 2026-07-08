---
name: auxiliary-losses-and-attention-bias
priority: 3
description: >
  >
---
# Auxiliary Losses and Attention Bias

## Contents

- **Auxiliary losses**: Auxiliary tasks teach a model to predict structural features: ```text L_total = L_lm + λ_op L_operator + λ_role L_event_
- **Attention bias**: Given ordinary attention logits: ```text A_ij = Q_i K_j^T / sqrt(d) ``` CIEL adds a structural bias: ```text A'_ij = A_i
- **Validator loop**: A generated output is accepted only if: - required operators are preserved, - event-frame roles are not swapped, - scope

## Key Points

- w_conflict * invariant_conflict(i,j)
- required operators are preserved,
- event-frame roles are not swapped,
- scope status is resolved or explicitly marked unresolved,
- antonym/synonym phase constraints are respected,
- cross-language reconstruction cost remains below a configured threshold.

## Code

```
The weights are configuration values, not claims about reality.

## Attention bias

Given ordinary attention logits:
```

---
*Extracted from: `src/ciel_lingophysics_lns_repo_v2_3/docs/38_AUXILIARY_LOSSES_AND_ATTENTION_BIAS.md` (59 lines, 1473B)*