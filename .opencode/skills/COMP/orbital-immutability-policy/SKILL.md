---
name: immutability-policy
priority: 4
description: >
  >
---
# Immutability Policy

## Contents

- **Purpose**: This file defines how the CIEL Ethics and Semantic Action Algorithm is governed across repositories.
- **Immutable core**: The following files are treated as immutable core contract files: - `contracts/CIEL_ETHICS_AND_SEMANTIC_ACTION_ALGORITHM
- **Allowed change modes**: Changes to the immutable core are allowed only through one of the following: 1. explicit version bump, 2. signed archite
- **Forbidden change modes**: The following are forbidden: - ad hoc local weakening of truth rules, - changing penalties without explicit declaration,
- **Extension rule**: Repository-local specialization must be written in: - `contracts/appendices/AUDIT_APPENDIX_<repo>.md` Such appendices ma
- **Interpretation hierarchy**: When documents disagree, the preferred order is: 1. immutable core contract, 2. machine-readable parameter file, 3. expl

## Key Points

- `contracts/CIEL_ETHICS_AND_SEMANTIC_ACTION_ALGORITHM.md`
- `contracts/relational_contract.yaml`
- ad hoc local weakening of truth rules,
- changing penalties without explicit declaration,
- removing audit channels silently,
- altering the output discipline silently,
- repository-local edits that invert the ethical ordering.
- `contracts/appendices/AUDIT_APPENDIX_<repo>.md`
- add local metrics,
- add repo-specific test surfaces,
- add domain-specific observables,
- refine thresholds.

---
*Extracted from: `src/CIEL_Orbital_Foundation_Packk/IMMUTABILITY_POLICY.md` (59 lines, 1643B)*