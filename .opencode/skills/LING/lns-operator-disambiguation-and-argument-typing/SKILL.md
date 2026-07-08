---
name: operator-disambiguation-and-argument-typing
priority: 4
description: >
  >
---
# Operator Disambiguation and Argument Typing

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