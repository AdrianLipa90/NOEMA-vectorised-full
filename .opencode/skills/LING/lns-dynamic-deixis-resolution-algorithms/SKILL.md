---
name: dynamic-deixis-resolution-algorithms
priority: 3
description: >
  >
---
# Dynamic Deixis Resolution Algorithms

## Contents

- **Pipeline**: ```text surface form -> detect dynamic deictic operator -> determine operator family -> attach variable anchor -> inspec
- **Spatial indefinite**: ```text Somewhere(E) -> ∃x∈Place : Located(E,x) ∧ resolution(x)<1 ``` If context contains a bounded spatial frame, e.g. 
- **Temporal indefinite**: ```text Sometime(E) -> ∃t∈Time : Occurs(E,t) ∧ resolution(t)<1 ``` `kiedyś` is especially important because it may point
- **Negative dynamic anchors**: Negative deictics collapse the existential anchor under active domain: ```text Nowhere(E) -> ¬∃x∈Place : Located(E,x) Ne
- **Free-choice dynamic anchors**: ```text Anywhere(E) -> free-choice x∈Place Anytime(E)  -> free-choice t∈Time ``` These interact with modal operators suc
- **Preservation rule**: If context cannot resolve the anchor, CIEL-LNS must preserve it as unresolved rather than hallucinat ```text UnresolvedA

## Code

```
If context contains a bounded spatial frame, e.g. `in the house`, the anchor becomes constrained:
```

```python
`kiedyś` is especially important because it may point backward or forward depending on tense, aspect, memory, and intention:
```

```
## Negative dynamic anchors

Negative deictics collapse the existential anchor under active domain:
```

---
*Extracted from: `src/ciel_lingophysics_lns_repo_v2_3/docs/23_DYNAMIC_DEIXIS_RESOLUTION_ALGORITHMS.md` (69 lines, 1651B)*