---
name: scope-quantifiers-negation
priority: 4
description: >
  >
---
# 28. Scope, Quantifiers and Negation Layer

## Contents

- **Canonical examples**: ```text PL: Nie każdy człowiek wie. EN: Not every human knows. FORM: ¬∀x Human(x) => Know(x) NORM: ∃x Human(x) ∧ ¬Know(x
- **Scope phase**: Each quantifier and negation placement receives a phase contribution. Two statements may have simila ```text φ_scope = φ
- **Cross-language mapping**: Languages without rich case or with fixed word order often surface scope through word order, auxilia

## Code

```
In CIEL-LNS/Ω, scope is represented as an ordered operator stack:
```

```
A sentence is not equivalent to another sentence unless its predicate frame, roles, polarity, TAM-E signature and scope signature are compatible.

## Canonical examples
```

```
These are not equivalent.

## Scope phase

Each quantifier and negation placement receives a phase contribution. Two statements may have similar surface content but different scope phase and therefore different semantic trajectory.
```

---
*Extracted from: `src/ciel_lingophysics_lns_repo_v2_3/docs/28_SCOPE_QUANTIFIERS_NEGATION.md` (51 lines, 1489B)*