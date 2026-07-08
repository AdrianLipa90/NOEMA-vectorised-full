# CIELingo Real-Time Unresolved Protocol

Status: local diagnostic/runtime layer. It is not NOEMA SoT writeback and it is not a canonical dictionary import.

The protocol handles words that the phase-sense parser cannot bind to an existing CIELingo language card.

Pipeline:

1. `parse_text_to_phase_sense(text)` marks unknown tokens.
2. `record_realtime_unresolved(text)` appends unknown tokens to:
   - `runtime/cielingo/unresolved/unresolved.jsonl`
   - `runtime/cielingo/unresolved/daily/YYYY-MM-DD.unresolved.jsonl`
3. The checker looks for local source evidence in `data/cielingo/source_evidence/*.jsonl`.
4. If evidence exists, it creates a candidate word card with initial `confidence = 0.5`.
5. Candidate cards remain non-canonical and require supervised review.
6. `daily_unresolved_rollup()` creates the daily summary without deleting raw events.

Semantic field policy:

- card order/filename number is technical only;
- word potential is semantic rest-mass proxy times `ln(2)/(24π)`;
- relation energy is a candidate N-body proxy;
- colour expresses emotional tone;
- intensity expresses emotional force;
- density expresses priority/weight;
- viscosity expresses subjective solo/group drag;
- no candidate is promoted to canon without evidence and review.

Source policy:

The module never fetches the network. External/open-source lexical resources must be supplied as local evidence extracts, with source name, license hint, retrieval mode and evidence digest. This preserves auditability and avoids hallucinated dictionary claims.
