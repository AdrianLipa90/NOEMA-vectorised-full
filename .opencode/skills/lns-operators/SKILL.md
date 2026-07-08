# Merge: lns-operators

Wszystkie skille z grupy lns-operators

---

## Importy

Ten skill agreguje poniższe skille źródłowe:

- `lns-dynamic-deictic-operators` → [`.opencode/skills/lns-dynamic-deictic-operators/SKILL.md`](.opencode/skills/lns-dynamic-deictic-operators/SKILL.md) (37 linii)
- `lns-functional-words-and-dual-operators` → [`.opencode/skills/lns-functional-words-and-dual-operators/SKILL.md`](.opencode/skills/lns-functional-words-and-dual-operators/SKILL.md) (39 linii)
- `lns-lingophysical-operator-algebra` → [`.opencode/skills/lns-lingophysical-operator-algebra/SKILL.md`](.opencode/skills/lns-lingophysical-operator-algebra/SKILL.md) (87 linii)
- `lns-ontological-aspect-and-being-operators` → [`.opencode/skills/lns-ontological-aspect-and-being-operators/SKILL.md`](.opencode/skills/lns-ontological-aspect-and-being-operators/SKILL.md) (37 linii)
- `lns-operator-card-model` → [`.opencode/skills/lns-operator-card-model/SKILL.md`](.opencode/skills/lns-operator-card-model/SKILL.md) (26 linii)
- `lns-operator-composition-rules` → [`.opencode/skills/lns-operator-composition-rules/SKILL.md`](.opencode/skills/lns-operator-composition-rules/SKILL.md) (27 linii)
- `lns-operator-disambiguation-and-argument-typing` → [`.opencode/skills/lns-operator-disambiguation-and-argument-typing/SKILL.md`](.opencode/skills/lns-operator-disambiguation-and-argument-typing/SKILL.md) (38 linii)
- `lns-operator-taxonomy` → [`.opencode/skills/lns-operator-taxonomy/SKILL.md`](.opencode/skills/lns-operator-taxonomy/SKILL.md) (50 linii)

---

## 1. lns-dynamic-deictic-operators

*Źródło: [`.opencode/skills/lns-dynamic-deictic-operators/SKILL.md`](.opencode/skills/lns-dynamic-deictic-operators/SKILL.md)*

---
name: dynamic-deictic-operators
priority: 3
description: >
  >
---

## Contents

- **Thesis**: Words such as **gdzieś**, **kiedyś**, **jakoś**, **dokądś**, and **skądś** are not ordinary concept  They do not name a 
- **Formal form**: A dynamic deictic operator is represented as: ```text D = (domain, anchor_type, resolution_state, scope, context_depende
- **Why this matters**: Mapping these words too early into precise locations or times creates false precision. In CIEL-LNS/Ω ```text Surface sim
- **Cross-linguistic note**: Polish can compactly encode indefinite deictic force through forms like `gdzieś`, `kiedyś`, `jakoś`, Therefore: ```text 

## Code

```
## Formal form

A dynamic deictic operator is represented as:
```

```
The generic resolution equation is:
```

```
where `C` is context, memory, grammar, goal, and active discourse frame.

## Why this matters

Mapping these words too early into precise locations or times creates false precision. In CIEL-LNS/Ω the unresolved state is meaningful and must be preserved until the context legitimately resolves it.
```

---
*Extracted from: `src/ciel_lingophysics_lns_repo_v2_3/docs/22_DYNAMIC_DEICTIC_OPERATORS.md` (53 lines, 1633B)*

---

## 2. lns-functional-words-and-dual-operators

*Źródło: [`.opencode/skills/lns-functional-words-and-dual-operators/SKILL.md`](.opencode/skills/lns-functional-words-and-dual-operators/SKILL.md)*

---
name: functional-words-and-dual-operators
priority: 3
description: >
  >
---

## Contents

- **`have / mieć`**: `have` is not one relation. It is a family of typed relations: ```text Have(possessor, possessed) HasPart(whole, part) H
- **`inside / contain`**: Dual pair: ```text Inside(x,y) ⇔ Contains(y,x) ``` The same invariant may surface in opposite grammatical orientation.
- **`how / jak`**: `how/jak` is polyfunctional: ```text How(T)        -> ask(Manner(T)) Like(x,y)     -> Sim(x,y) As(x,y)       -> MapPatte
- **Rule**: Do not encode functional words as normal concept cards unless they carry independent semantic body b ```text Nouns are m

## Code

```
## `inside / contain`

Dual pair:
```

```
The same invariant may surface in opposite grammatical orientation.

## `how / jak`

`how/jak` is polyfunctional:
```

```
## Rule

Do not encode functional words as normal concept cards unless they carry independent semantic body behavior.
```

---
*Extracted from: `src/ciel_lingophysics_lns_repo_v2_3/docs/13_FUNCTIONAL_WORDS_AND_DUAL_OPERATORS.md` (48 lines, 905B)*

---

## 3. lns-lingophysical-operator-algebra

*Źródło: [`.opencode/skills/lns-lingophysical-operator-algebra/SKILL.md`](.opencode/skills/lns-lingophysical-operator-algebra/SKILL.md)*

---
name: lingophysical-operator-algebra
priority: 3
description: >
  >
---

## Contents

- **Core correction**: A lexical item is not automatically a concept. In CIEL-LNS/Ω, ordinary lexical surfaces are separate ```text CONCEPT_CAR
- **Concept mass vs operator power**: Concepts carry semantic mass: \[ m_s(c) \ge 0 \] Operators carry structural power / curvature: \[ \kappa(Op)=f+structura
- **Sentence as operator application**: A sentence is not a bag of words. It is an operator expression over concepts. ```text The glass contains water. ``` \[ C
- **Required fields for operator cards**: Every operator card should define: ```yaml id: op:core:inside family: containment operator_type: spatial_topological ari
- **Rule**: ```text Concept cards are masses. Operator cards are forces. Grammar is geometry. Sentences are trajectories ```

## Formulas

- `\mathcal{L}_{phys}=(\mathcal{C},\mathcal{O}p,\mathcal{R},\circ,\otimes,\neg,\phi)`
- `m_s(c) \ge 0`
- `\kappa(Op)=f+structural\_power+ambiguity+composition\_depth+cross\_language\_variance`
- `Contains(Glass,Water)`
- `Inside(Water,Glass)`
- `Contains(y,x) \Leftrightarrow Inside(x,y)`

## Key Points

- \(\mathcal{C}\) is the library of concept cards,
- \(\mathcal{O}p\) is the library of operator cards,
- \(\mathcal{R}\) is the relation graph,
- \(\circ\) is operator composition,
- \(\otimes\) is structural coupling,
- \(\neg\) is polarity inversion,
- \(\phi\) is semantic phase.

## Code

```
The practical form of lingophysics is therefore:

\[
\mathcal{L}_{phys}=(\mathcal{C},\mathcal{O}p,\mathcal{R},\circ,\otimes,\neg,\phi)
\]

where:

- \(\mathcal{C}\) is the library of concept cards,
- \(\mathcal{O}p\) is the library of operator cards,
- \(\mathcal{R}\) is the relation graph,
- \(\circ\) is operator composition,
- \(\otimes\) is structural coupling,
- \(\neg\) is polarity inversion,
- \(\phi\) is semantic phase.

## Concept mass vs operator power

Concepts carry semantic mass:

\[
```

```
## Sentence as operator application

A sentence is not a bag of words. It is an operator expression over concepts.
```

```
\[
Inside(Water,Glass)
\]

The two expressions are dual:

\[
Contains(y,x) \Leftrightarrow Inside(x,y)
\]

The surface changes, but the topological containment invariant is preserved.

## Required fields for operator cards

Every operator card should define:
```

---
*Extracted from: `src/ciel_lingophysics_lns_repo_v2_3/docs/14_LINGOPHYSICAL_OPERATOR_ALGEBRA.md` (106 lines, 2341B)*

---

## 4. lns-ontological-aspect-and-being-operators

*Źródło: [`.opencode/skills/lns-ontological-aspect-and-being-operators/SKILL.md`](.opencode/skills/lns-ontological-aspect-and-being-operators/SKILL.md)*

---
name: ontological-aspect-and-being-operators
priority: 3
description: >
  >
---

## Contents

- **Koto / Mono**: Japanese `mono` tends toward concrete or object-like thinghood: ```text Mono(x) -> ConcreteOrObjectLikeThing(x) ``` Japa
- **Ser / Estar**: Spanish splits English/Polish `be` into at least two major operators: ```text Ser(x,y)   -> IdentityBe(x,y) Estar(x,s) -
- **Cross-language mapping**: English and Polish often collapse these distinctions into one surface `be/być`. CIELingo therefore t ```text EnglishBe -
- **Core rule**: ```text being is not one operator; being is an operator family. ``` That family must be catalogued before translation, o

## Code

```
Japanese `koto` tends toward abstract event, fact, situation, or proposition:
```

```
## Ser / Estar

Spanish splits English/Polish `be` into at least two major operators:
```

```
Important precision: `ser` is not simply permanent and `estar` is not simply temporary. The better split is identity/class/role/origin versus state/location/result condition.

## Cross-language mapping

English and Polish often collapse these distinctions into one surface `be/być`. CIELingo therefore treats them as polyfunctional operators that must be resolved by complement type, case, adjective, preposition, event frame, and context.
```

---
*Extracted from: `src/ciel_lingophysics_lns_repo_v2_3/docs/25_ONTOLOGICAL_ASPECT_AND_BEING_OPERATORS.md` (57 lines, 1817B)*

---

## 5. lns-operator-card-model

*Źródło: [`.opencode/skills/lns-operator-card-model/SKILL.md`](.opencode/skills/lns-operator-card-model/SKILL.md)*

---
name: operator-card-model
priority: 4
description: >
  >
---

## Code

```
A sentence becomes a composition of concept bodies and operators:
```

```
Surface differs, focus differs, but the topological invariant is shared:
```

---
*Extracted from: `src/ciel_lingophysics_lns_repo_v2_3/docs/12_OPERATOR_CARD_MODEL.md` (40 lines, 1091B)*
## Zrodlo

- `scripts/build_word_cards_registry.py`
- `scripts/ciel_repo_cards_throttle.py`
- `scripts/generate_object_cards_py.py`


---

## 6. lns-operator-composition-rules

*Źródło: [`.opencode/skills/lns-operator-composition-rules/SKILL.md`](.opencode/skills/lns-operator-composition-rules/SKILL.md)*

---
name: operator-composition-rules
priority: 4
description: >
  >
---

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

---

## 7. lns-operator-disambiguation-and-argument-typing

*Źródło: [`.opencode/skills/lns-operator-disambiguation-and-argument-typing/SKILL.md`](.opencode/skills/lns-operator-disambiguation-and-argument-typing/SKILL.md)*

---
name: operator-disambiguation-and-argument-typing
priority: 4
description: >
  >
---

## Contents

- **Example: `have / mieć`**: ```text Jan ma psa.           -> Own/AlienablePossession(John,dog) Jan ma oczy.          -> HasPart(John,eyes) Woda ma t
- **Example: `jak / how / as / like`**: ```text Jak to działa?             -> How(T) -> Ask(Manner(T)) Działa jak silnik.         -> Like(x,y) -> Sim(x,y) Pracu
- **Required disambiguation dimensions**: - surface form, - language, - part of speech, - argument types, - local syntax, - context window, - semantic axis, - kno
- **Minimum implementation**: The initial implementation is intentionally rule-based. Statistical disambiguation can be added late

## Formulas

- `Mode(Have,x,y)=\arg\max_m Score(m|type(x),type(y),context)`

## Key Points

- known dual/inverse operators,
- operator family.

## Code

```
Formal selection:

\[
Mode(Have,x,y)=\arg\max_m Score(m|type(x),type(y),context)
\]

## Example: `jak / how / as / like`
```

---
*Extracted from: `src/ciel_lingophysics_lns_repo_v2_3/docs/17_OPERATOR_DISAMBIGUATION_AND_ARGUMENT_TYPING.md` (45 lines, 1181B)*

---

## 8. lns-operator-taxonomy

*Źródło: [`.opencode/skills/lns-operator-taxonomy/SKILL.md`](.opencode/skills/lns-operator-taxonomy/SKILL.md)*

---
name: operator-taxonomy
priority: 4
description: >
  >
---

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

---
