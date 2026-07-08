# Merge: lns-batches

Wszystkie skille z grupy lns-batches

---

## Importy

Ten skill agreguje poniższe skille źródłowe:

- `lns-batch-library-build-protocol` → [`.opencode/skills/lns-batch-library-build-protocol/SKILL.md`](.opencode/skills/lns-batch-library-build-protocol/SKILL.md) (36 linii)
- `lns-batch01-foundational-36x5` → [`.opencode/skills/lns-batch01-foundational-36x5/SKILL.md`](.opencode/skills/lns-batch01-foundational-36x5/SKILL.md) (31 linii)
- `lns-batch02-dependency-growth-and-martini-effect` → [`.opencode/skills/lns-batch02-dependency-growth-and-martini-effect/SKILL.md`](.opencode/skills/lns-batch02-dependency-growth-and-martini-effect/SKILL.md) (15 linii)
- `lns-batch02-expansion-36x5` → [`.opencode/skills/lns-batch02-expansion-36x5/SKILL.md`](.opencode/skills/lns-batch02-expansion-36x5/SKILL.md) (23 linii)

---

## 1. lns-batch-library-build-protocol

*Źródło: [`.opencode/skills/lns-batch-library-build-protocol/SKILL.md`](.opencode/skills/lns-batch-library-build-protocol/SKILL.md)*

---
name: batch-library-build-protocol
priority: 3
description: >
  >
---

## Contents

- **Principle**: A batch is not a word list. A batch is a controlled update to a growing semantic graph. ```text NewCards -> CompareAgain
- **Batch sizing**: - Rounds 1-3: 36 concept cards × 5 languages. - Rounds 4-7: 20 concept cards × 5 languages. - Later rounds: 15 concept c
- **Separation rule**: ```text Concept cards are semantic masses. Operator cards are forces/functions. Grammar is geometry. A sentence is a tra

## Key Points

- Rounds 1-3: 36 concept cards × 5 languages.
- Rounds 4-7: 20 concept cards × 5 languages.
- Later rounds: 15 concept cards × 5 languages.

## Code

```
## Batch sizing

- Rounds 1-3: 36 concept cards × 5 languages.
- Rounds 4-7: 20 concept cards × 5 languages.
- Later rounds: 15 concept cards × 5 languages.

The batch size shrinks because graph density increases. Each new card must be checked against all existing cards for synonymy, antonymy, dual operators, false friends, phase conflicts, and attractor membership.

## Separation rule
```

---
*Extracted from: `src/ciel_lingophysics_lns_repo_v2_3/docs/18_BATCH_LIBRARY_BUILD_PROTOCOL.md` (30 lines, 1039B)*

---

## 2. lns-batch01-foundational-36x5

*Źródło: [`.opencode/skills/lns-batch01-foundational-36x5/SKILL.md`](.opencode/skills/lns-batch01-foundational-36x5/SKILL.md)*

---
name: batch01-foundational-36x5
priority: 3
description: >
  >
---

## Contents

- **Counts**: - Concept cards: 36 - Language panels: 180 - Relation rows: 454 - Operator links: 115
- **Data artifacts**: - `data/concept_cards/batch01_foundational_36x5/*.yaml` - `data/concept_cards/batch01_foundational_36x5/*.json` - `data/
- **Validation status**: The test suite verifies basic counts, language coverage, concept/operator separation, SQLite presenc

## Key Points

- Concept cards: 36
- Language panels: 180
- Relation rows: 454
- Operator links: 115
- `data/concept_cards/batch01_foundational_36x5/*.yaml`
- `data/concept_cards/batch01_foundational_36x5/*.json`
- `data/concept_cards/batch01_foundational_36x5/batch01_multilingual_concept_cards.xlsx`
- `data/sqlite/cielingo_batch01_v1_0.sqlite`
- `data/hdf5/cielingo_batch01_v1_0.h5`
- `data/graphs/batch01_concept_operator_graph.graphml`
- `outputs/heatmaps/batch01_grammar_gauge_distance.png`
- `outputs/heatmaps/batch01_concept_operator_incidence.png`

---
*Extracted from: `src/ciel_lingophysics_lns_repo_v2_3/docs/19_BATCH01_FOUNDATIONAL_36X5.md` (29 lines, 1053B)*

---

## 3. lns-batch02-dependency-growth-and-martini-effect

*Źródło: [`.opencode/skills/lns-batch02-dependency-growth-and-martini-effect/SKILL.md`](.opencode/skills/lns-batch02-dependency-growth-and-martini-effect/SKILL.md)*

---
name: batch02-dependency-growth-and-martini-effect
priority: 3
description: >
  >
---

## Contents

- **Required pipeline**: ```text new card → classify card type → attach language panels → attach operator hooks → compare against existing cards 
- **Batch-size rule**: ```text 0–100 cards      batch 36 100–200 cards    batch 20 200+ cards       batch 15 400+ cards       batch 10 or curat

---
*Extracted from: `src/ciel_lingophysics_lns_repo_v2_3/docs/35_BATCH02_DEPENDENCY_GROWTH_AND_MARTINI_EFFECT.md` (28 lines, 837B)*

---

## 4. lns-batch02-expansion-36x5

*Źródło: [`.opencode/skills/lns-batch02-expansion-36x5/SKILL.md`](.opencode/skills/lns-batch02-expansion-36x5/SKILL.md)*

---
name: batch02-expansion-36x5
priority: 3
description: >
  >
---

## Contents

- **Principle**: Batch02 is not a dictionary import. It is a hand-curated seed layer. Each concept card is a semantic ```text Concept car
- **Counts**: - 36 concept cards - 5 languages - 180 language panels - SQLite, HDF5, JSON/YAML, CSV, GraphML, graph JSON - XLSX workbo
- **Status**: All data are `draft_seed` and `needs_human_validation`.

## Key Points

- 36 concept cards
- 180 language panels
- SQLite, HDF5, JSON/YAML, CSV, GraphML, graph JSON
- XLSX workbook generated as a human-facing card table

---
*Extracted from: `src/ciel_lingophysics_lns_repo_v2_3/docs/34_BATCH02_EXPANSION_36X5.md` (28 lines, 809B)*

---
