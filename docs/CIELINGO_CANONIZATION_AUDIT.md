# CIELingo Canonization Audit

This stage checks the infinitive merge and residual grouping outputs and canonizes only what can be canonized locally.

Canon levels:

- `external_canon`: requires imported Wiktionary/SGJP/Morfeusz/plWordNet evidence plus review. This patch creates zero external-canon entries.
- `local_morphology_canon_candidate`: deterministic infinitive mapping accepted as a CIELingo-local morphology map, not as dictionary truth.
- `local_residual_set_canon`: residual set membership accepted as workflow taxonomy, not POS/lemma truth.
- `deferred`: candidate remains blocked until source lookup and review.

The numeric order of source cards remains technical provenance only.
