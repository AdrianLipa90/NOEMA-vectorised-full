---
name: case-gauge-layer-slavic-to-weak-case-languages
priority: 3
description: >
  >
---
# 20. Case Gauge Layer: Mapping Slavic Cases to Weak-Case Languages

## Contents

- **Core claim**: Slavic case morphology is not just “word form decoration”. In CIEL-LNS it is a **local gauge of sema Universal Dependenc
- **Formal model**: For a Slavic language `l_s`: ```text Surface_l_s(token_with_case) -> CaseRole(token, role) ``` For a weak-case language 
- **Polish case operators**: | Case | Polish | CIEL operator | Weak-case realization | |---|---|---|---| | Nom | mianownik | `SubjectOrIdentity(x)` |
- **Important warning**: A case is often polyfunctional and governed by lexical valency. Therefore each mapping needs: ```text case + governing o
- **CIEL rule**: ```text Slavic case endings are compressed role operators. Weak-case languages reconstruct those operators with syntax, 

## Tables

| Nom | mianownik | `SubjectOrIdentity(x)` | subject position, nominative pronoun residue |
| Acc | biernik | `DirectPatient(x)` | direct object position, object pronoun/clitic |
| Gen | dopełniacz | `OfPossessionSourcePartitive(x,y)` | `of`, possessive, `de`, partitive, negation/absence constructions |
| Dat | celownik | `RecipientBeneficiaryTarget(x)` | `to/for`, `à`, `a/para`, indirect object clitics |
| Ins | narzędnik | `InstrumentMeansComitativeRole(x)` | `with/by/using/as`, `mit/durch/von/als`, etc. |
| Loc | miejscownik | `LocationTopicFrame(x)` | `in/on/at/about`, `dans/sur/à`, `en/sobre`, selected by operator |
| Voc | wołacz | `Address(x)` | comma, intonation, address particles |

## Code

```
For a weak-case language `l_w`:
```

```
## Polish case operators

| Case | Polish | CIEL operator | Weak-case realization |
|---|---|---|---|
| Nom | mianownik | `SubjectOrIdentity(x)` | subject position, nominative pronoun residue |
| Acc | biernik | `DirectPatient(x)` | direct object position, object pronoun/clitic |
| Gen | dopełniacz | `OfPossessionSourcePartitive(x,y)` | `of`, possessive, `de`, partitive, negation/absence constructions |
| Dat | celownik | `RecipientBeneficiaryTarget(x)` | `to/for`, `à`, `a/para`, indirect object
```

```
Without valency, mapping is noisy. For example Polish genitive may encode possession, absence under negation, source, measure, or partitive structure. A single English preposition cannot cover all of it.

## CIEL rule
```

---
*Extracted from: `src/ciel_lingophysics_lns_repo_v2_3/docs/20_CASE_GAUGE_LAYER_SLAVIC_TO_WEAK_CASE_LANGUAGES.md` (65 lines, 2567B)*