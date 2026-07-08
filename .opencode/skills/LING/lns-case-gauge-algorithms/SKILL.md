---
name: case-gauge-algorithms
priority: 3
description: >
  >
---
# 21. Case Gauge Algorithms

## Contents

- **Algorithm 1: decode Slavic case**: Input: ```text token, lemma, morphological_case, governing_operator, context ``` Output: ```text CaseRole(token, role, c
- **Algorithm 2: encode into weak-case language**: Input: ```text CaseRole(token, role), target_language ``` Output: ```text surface strategy: word order / preposition / c
- **Algorithm 3: check cross-language equivalence**: Two sentences are compatible if: ```text PredicateArgumentInvariant(S1) == PredicateArgumentInvariant(S2) CaseRoleInvari

## Code

```
Steps:

1. Read morphological `Case`.
2. Read the governing verb/adposition/operator.
3. Resolve valency.
4. Resolve noun animacy/personhood if relevant.
5. Return canonical CIEL case operator.

## Algorithm 2: encode into weak-case language

Input:
```

```
Steps:

1. Select the target language grammar profile.
2. Choose primary realization strategy.
3. Insert adposition or clitic if needed.
4. Place noun phrase according to target syntax.
5. Preserve predicate-argument invariant.

## Algorithm 3: check cross-language equivalence

Two sentences are compatible if:
```

---
*Extracted from: `src/ciel_lingophysics_lns_repo_v2_3/docs/21_CASE_GAUGE_ALGORITHMS.md` (66 lines, 1354B)*