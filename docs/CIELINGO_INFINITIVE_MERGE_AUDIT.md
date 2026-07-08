# CIELingo infinitive merge audit

This stage follows `CIELINGO_UNKNOWN_WORD_AUDIT`.

It performs three operations:

1. `bezokolicznikujemy co się da`: safe local heuristic conversion of unknown surfaces to infinitive/action candidates.
2. `bezokoliczniki zestawiamy ze stanem`: each candidate is merged with the existing unknown-state record: semantic mass, density, relation energy, source card id and next action.
3. `resztę grupujemy na zbiory własne`: all non-infinitivized words receive exactly one residual-set assignment.

No mapping is canonical.  The outputs are candidate surfaces for SGJP/Morfeusz/Wiktionary/plWordNet or supervised review.
