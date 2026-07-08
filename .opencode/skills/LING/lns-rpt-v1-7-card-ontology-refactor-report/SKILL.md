---
name: v1-7-card-ontology-refactor-report
priority: 5
description: >
  >
---
# v1.7 Card Ontology Refactor Patch Report

## Contents

- **What changed**: This patch turns the v1.6 repository into a typed card system. It adds explicit ontology files, cons
- **Core correction**: ```text Not every word is a concept. Concept cards are masses. Operator cards are forces. Grammar is geometry. Sentences
- **New validation**: - concept cards cannot silently become primary operator definitions; - operator cards missing arity/formal modes are war
- **Result**: The repo is now ready for a cleaner Batch02 expansion because every new object must first declare or

## Key Points

- concept cards cannot silently become primary operator definitions;
- operator cards missing arity/formal modes are warned;
- deictic cards may remain unresolved but must identify their anchor domain;
- scope cards preserve unresolved scope rather than guessing;
- repository files are classified into explicit ontology layers.

---
*Extracted from: `src/ciel_lingophysics_lns_repo_v2_3/reports/v1_7_card_ontology_refactor_report.md` (29 lines, 909B)*