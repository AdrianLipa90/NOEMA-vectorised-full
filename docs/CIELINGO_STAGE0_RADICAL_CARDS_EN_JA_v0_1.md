# CIELingo Stage 0 — Radical Cards and EN/JA Test Words v0.1

**Status:** `stage0_seed_patch`  
**Epistemic mode:** `ARTIFACT_GROUNDED + HYPOTHESIS`  
**NOEMA SoT:** not written  
**Canon:** not allowed by default  
**Japanese status:** technical draft; `needs_native_review=true`

## Purpose

This seed patch creates the first careful data layer for the Stage 0 linguistic architecture:

1. global radical cards / lexical slots,
2. separate English and Japanese language-slot entries,
3. non-identity cross-language alignment records,
4. validation tests for the Stage 0 contract.

This is not a translation table. A shared `slot_id` is a comparison axis, not semantic identity.

## Principles encoded

### Lexical Slot Principle

Each radical has a global `slot_id`. Example:

```text
slot[15] = FILE
en[15] = file
ja[15] = ファイル
```

### Separate Language Space Principle

English and Japanese entries live in separate language spaces. Their local J-functionals differ.

### Local Holonomy Principle

Each language entry carries its own `j_functionals`. Japanese entries deliberately include higher `J_particle_load`, `J_politeness_load`, and `J_native_review_required`.

### In Blanco readiness

This patch does not yet include blank entries, but the schema supports:

```text
in_blanco_open
in_blanco_stable
in_blanco_validated
```

A missing equivalent must remain blank rather than being hallucinated.

### No SOURCE by default

Radicals, language entries, and alignment records are `ARTIFACT_GROUNDED`, not `SOURCE`.

## Files

```text
src/cielingo/stage0_radical_cards.py
cards/cielingo_radicals/radical_cards_seed_v0_1.jsonl
cards/cielingo_languages/en/slot_entries_test_v0_1.jsonl
cards/cielingo_languages/ja/slot_entries_test_v0_1.jsonl
cards/cielingo_alignments/alignment_seed_en_ja_v0_1.jsonl
tests/test_cielingo_stage0_radical_cards.py
reports/cielingo_stage0_radical_cards_en_ja_v0_1_report.json
```

## Seed contents

The patch contains:

- 24 radical cards,
- 24 English language-slot entries,
- 24 Japanese language-slot entries,
- 24 alignment records.

The seed is intentionally small and designed for ad hoc testing of the universal sentence-equation architecture.

## Caveat on Japanese

Japanese entries are technically curated but not native-validated. The patch marks every Japanese entry with:

```yaml
needs_native_review: true
J_native_review_required: 1.0
```

This prevents false linguistic certainty.

## Validation

Run:

```bash
PYTHONPATH=. pytest -q tests/test_cielingo_stage0_radical_cards.py
```

Expected result:

```text
8 passed
```
