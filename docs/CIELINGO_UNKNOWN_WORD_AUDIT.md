# CIELingo Unknown Word Audit

Schema version: `cielingo/unknown-word-audit/v0.2`

`CIELINGO_UNKNOWN_WORD_AUDIT` treats unknown words as productive failure, not as a terminal error.

The audit reads `unknown_word_candidate` cards generated from meaning-debt scaffolds and writes a supervised learning queue:

- `unknown_words.audit.jsonl` — every unknown with a debt type, missing axis, confidence and next action.
- `unknown_clusters.jsonl` — suffix/debt clusters for morphology and source planning.
- `missing_axes_report.json` — aggregate map of what the grammar omitted.
- `source_lookup_queue.jsonl` — Wiktionary/SGJP/Morfeusz/plWordNet/human-review lookup queue.
- `promotion_candidates_0_5.jsonl` — candidate material only; not canon and not `WORD_CARD_PASS`.
- `review_batches/batch_*.jsonl` — batches for supervised correction.

Protocol:

```text
unknown -> debt_type -> missing_axis -> source_lookup -> candidate_0_5 -> supervised_review -> revaluation -> possible_promotion
```

No sequence number, filename prefix, card ordinal or source-card number is semantic rank. It is provenance only.

Core classifications:

- `closed_class_missed`
- `quantifier_pronoun_axis_missing`
- `unknown_inflected_form_candidate`
- `verbal_noun_or_participle_candidate`
- `adverb_or_manner_axis_missing`
- `project_or_runtime_term_candidate`
- `foreign_or_technical_candidate`
- `unknown_real_polish_word_candidate`
- `source_required_before_classification`

Every word receives a status. Unknown is allowed; unmarked is not.


## Collatz learning cycle

Unknown word handling uses the project Collatz rhythm:

```text
unknown odd state -> ×3+1 expansion -> explicit hypotheses + no-canon boundary -> /2 reduction -> source evidence + supervised review
```

The expansion is not hallucination. It is a controlled generation of candidate axes: POS/function, morphology/source, affect/register and boundary. Reduction is allowed only through evidence and review. In this sense `×3+1` exists so `/2` has something structured to reduce.
