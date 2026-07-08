---
name: scope-resolution-algorithms
priority: 4
description: >
  >
---
# 29. Scope Resolution Algorithms

## Contents

- **Pipeline**: ```text surface sentence → detect quantifier surface → detect negation surface → infer negation position → attach to pre
- **Core algorithm**: ```python q = encode_quantifier(surface_or_name) expr = normalize_scope(q, predicate, negation_position) ``` Negation po
- **Equivalence guard**: Two statements are not equivalent unless: ```text predicate_frame_equal roles_equal TAM-E compatible polarity compatible
- **Fallback rule**: If scope resolution cannot determine the position of negation, the output must be: ```text scope_status: unresolved ``` 

## Code

```
## Equivalence guard

Two statements are not equivalent unless:
```

```
The guard rejects false equivalences such as:
```

```
## Fallback rule

If scope resolution cannot determine the position of negation, the output must be:
```

---
*Extracted from: `src/ciel_lingophysics_lns_repo_v2_3/docs/29_SCOPE_RESOLUTION_ALGORITHMS.md` (64 lines, 1213B)*