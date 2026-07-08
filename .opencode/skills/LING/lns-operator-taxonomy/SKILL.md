---
name: operator-taxonomy
priority: 4
description: >
  >
---
# Operator Taxonomy

## Contents

- **Arity classes**: \[ Op^{(0)}, Op^{(1)}, Op^{(2)}, Op^{(3)}, Op^{(n)}, Op^{(Op)} \] - nullary: interjections, impulses, - unary: `Not(x)`,
- **Polymorphic operators**: Some surfaces map to multiple formal modes. These must be represented as operator families, not sing Example: ```text ma

## Formulas

- `Op^{(0)}, Op^{(1)}, Op^{(2)}, Op^{(3)}, Op^{(n)}, Op^{(Op)}`
- `Have(x,y) \rightarrow \{Own, HasPart, HasProperty, HasState, HasRelation\}`
- `Jak \rightarrow \{How, Like, AsRole, PatternMap, WhenIf\}`

## Key Points

- nullary: interjections, impulses,
- unary: `Not(x)`, `Must(T)`, `Very(P)`,
- binary: `Inside(x,y)`, `Contains(x,y)`,
- ternary: `Give(agent,object,recipient)`,
- higher-order: adverbs and modals acting on operators.

## Tables

| identity | identity / being | jest, to, być | is, be | `Be(x)`, `Equals(x,y)` |
| possession | attachment / ownership / property | ma, posiada | has, owns | `Have(x,y)` |
| containment | interior / inclusion | w, wewnątrz, zawiera | in, inside, contains | `Inside(x,y)`, `Contains(y,x)` |
| spatial | relative position | na, pod, nad, obok | on, under, above, near | `SpatialRel(x,y)` |
| temporal | order in time | przed, po, kiedy | before, after, when | `TemporalRel(e1,e2)` |
| logical | logic gates | i, albo, nie, jeśli | and, or, not, if | `And`, `Or`, `Not`, `IfThen` |
| causal | causality | bo, ponieważ, przez | because, due to, by | `Cause(x,y)` |
| modal | possibility / necessity | może, musi, powinien | may, must, should | `Modal(Op)` |

## Code

```
\[
Have(x,y) \rightarrow \{Own, HasPart, HasProperty, HasState, HasRelation\}
\]

Example:
```

---
*Extracted from: `src/ciel_lingophysics_lns_repo_v2_3/docs/15_OPERATOR_TAXONOMY.md` (55 lines, 2148B)*