# CIELingo Lexical Holonomy

This layer establishes relations between words, not only vectors for cards.

It treats the local NOEMA/LNS card tree as the primary source surface and adds:

- synonym / near-synonym / bliskoznaczne edges from card seed fields;
- antonym / opposition edges from card seed fields and relation CSV files;
- convergent / divergent derived edges from shared axes, phase deltas and vector distance;
- guarded access to the model's own language-card files for supervised grammar repair;
- one `word_knowledge_note` per lexical unit, with confidence, evidence counts, review state and external-source verification plan.

The module does not auto-promote any word to canon.  Open-source lexical sources are descriptors until imported with concrete dump/API provenance and license evidence.

Supervision rule: grammar correction proposals may read card files and emit patch candidates, but must not overwrite card files without human/CIEL review.
