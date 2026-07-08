# CIELingo Meaning-Debt Word Cards

This layer converts the CIEL-POL meaning-debt registry into supervised candidate word cards. It does not canonize the old scaffolds.

Rules:

- sequence numbers, file names, and legacy `MISSING-POL-*` ids are technical provenance only;
- every word receives a grammatical designation, even if the designation is a low-confidence candidate;
- infinitives are separated first because they seed action/predicate dynamics and modal mappings;
- other parts of speech and sentence roles are marked by a deterministic local heuristic;
- all candidates begin at confidence `0.5` and remain behind `WORD_CARD_PASS_FALSE_UNTIL_RESOLVED`;
- no candidate becomes canon without open-source evidence and supervised grammar review.

Field interpretation:

- word potential is computed from semantic rest mass and `κ_info = ln(2)/(24π)`;
- relation energy is a proxy for the word-in-relation load;
- colour is the emotional/register channel;
- intensity is the strength of that colour;
- density is priority/weight;
- solo/group viscosity expresses subjective friction for one person and for a group.

Outputs:

- `data/cielingo/debt_word_cards/word_candidate_cards.jsonl`
- `data/cielingo/debt_word_cards/infinitive_candidate_cards.jsonl`
- `data/cielingo/debt_word_cards/other_pos_candidate_cards.jsonl`
- `data/cielingo/debt_word_cards/by_part_of_speech/*.jsonl`
- `data/cielingo/debt_word_cards/meaning_debt_word_cards_report.json`

This is a debt surface, not a dictionary.
