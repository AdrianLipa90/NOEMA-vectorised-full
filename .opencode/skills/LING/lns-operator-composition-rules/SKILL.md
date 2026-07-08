---
name: operator-composition-rules
priority: 4
description: >
  >
---
# Operator Composition Rules

## Contents

- **Duality**: A dual operator pair preserves a core invariant while reversing orientation or focus. \[ Inside(x,y) \Leftrightarrow Con
- **Inversion and negation**: Negation is not always the same as inverse. \[ Not(Inside(x,y)) \neq Outside(x,y) \] because `not inside` may mean outsi
- **Higher-order operators**: Adverbs and modals act on operators rather than objects: \[ Quickly(Run(x)) \] \[ Must(Do(agent,action)) \]
- **Composition safety**: Composition must preserve argument typing: \[ Op_2(Op_1(x,y)) \text{ is valid only if } codomain(Op_1) \subset domain(Op
- **Euler phase constraints**: Synonymic operator variants should be phase-aligned on their semantic axis: \[ Syn_\xi(a,b) \Rightarrow |e^{i(\phi_a^\xi

## Formulas

- `Inside(x,y) \Leftrightarrow Contains(y,x)`
- `Before(x,y) \Leftrightarrow After(y,x)`
- `From(x,y) \Leftrightarrow To(y,x)`
- `Not(Inside(x,y)) \neq Outside(x,y)`
- `Quickly(Run(x))`
- `Must(Do(agent,action))`

---
*Extracted from: `src/ciel_lingophysics_lns_repo_v2_3/docs/16_OPERATOR_COMPOSITION_RULES.md` (69 lines, 1328B)*