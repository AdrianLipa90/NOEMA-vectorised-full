"""PhaseNav concept classifier — lexical, not hash-based.

This is the single lexical classification surface.  Text without a matching
anchor is classified as ``UNCERTAINTY`` (the explicit epistemic state for
insufficient evidence), never assigned a synthetic hash-derived operator.

This module instead scores a document against each of the 36 canonical
operators (`operator_algebra.ALL_OPERATOR_IDS`) using a human-curated
keyword anchor set matched against the document's TF-IDF term weights
(`term_index` table, already computed by the ingestion pipeline). The
anchor lists are a first-pass lexicon, not a formal ontology — expect to
refine them once real tagging output is reviewed.
"""
from __future__ import annotations

from .operator_algebra import ALL_OPERATOR_IDS

# Human-curated keyword anchors per operator. Each anchor is matched as a
# case-insensitive substring against term_index terms (already stemmed/
# tokenized by the ingestion pipeline), not an exact token match — this
# tolerates minor stemming variance without a full NLP stack.
OPERATOR_ANCHORS: dict[str, list[str]] = {
    # Bilingual (English + Polish) — CIEL's actual conversational language is
    # Polish, so an English-only anchor set never matches ordinary Polish
    # input and silently falls back to UNCERTAINTY for everything. Added
    # 2026-07-18 after exactly that was observed live: "pamiętasz co
    # mówiliśmy wcześniej?" (an obvious memory-domain question) classified
    # as UNCERTAINTY because none of its words were English.
    "IDENTITY": ["identity", "self-same", "sameness", "invariant", "unchanged", "equal to itself",
                 "tożsamość", "identyczny", "taki sam", "niezmienny", "ten sam"],
    "DIFFERENCE": ["difference", "distinct", "contrast", "unlike", "disparity", "deviation",
                   "różnica", "różny", "odmienny", "kontrast", "rozbieżność"],
    "ORDER": ["order", "sequence", "rank", "sort", "hierarchy", "priority",
              "kolejność", "sekwencja", "hierarchia", "priorytet", "sortowanie"],
    "COMPOSITION": ["composition", "compose", "combine", "assemble", "synthesis", "structure",
                    "holonomy", "holonomia", "holonomię", "geometric phase", "berry phase",
                    "faza geometryczna", "faza berry", "parallel transport", "transport równoległy",
                    "kompozycja", "złożenie", "połączenie", "synteza", "struktura"],
    "ADDITION": ["addition", "summation", "aggregate", "accumulate", "superposition",
                 "dodawanie", "suma", "sumowanie", "akumulacja", "superpozycja"],
    "FORCE": ["force", "power", "energy", "drive", "impact", "strength", "pressure",
              "siła", "moc", "energia", "napęd", "wpływ", "nacisk"],
    "NEGATION": ["negation", "deny", "refuse", "absence", "without", "not the case",
                 "negacja", "zaprzeczenie", "brak", "bez"],
    "QUESTION": ["question", "query", "inquiry", "ask", "interrogative",
                 "pytanie", "zapytanie", "kwestia", "pytać"],
    "TRANSFORM": ["transform", "transformation", "convert", "morph", "mapping", "conversion",
                  "phase", "faza", "fazy", "fazie", "fazę", "fazą", "fazow", "fazowy", "fazowa", "fazowe",
                  "oscylator", "oscylatorów", "oscylację", "oscylacja", "oscylacji",
                  "oscillator", "oscillation", "kuramoto", "synchronization", "synchronizacja",
                  "synchronizację", "synchronizacji", "synchronizacyjn",
                  "phasenav", "orbital", "koherencja", "koherencji", "koherencję", "coherence",
                  "resonance", "rezonans", "rezonansu", "rezonansow",
                  "transformacja", "przekształcenie", "zmiana", "konwersja", "mapowanie"],
    "RETURN": ["return", "revert", "recur", "cycle", "feedback loop",
               "powrót", "nawrót", "cykl", "sprzężenie zwrotne", "wraca"],
    "FOLD": ["fold", "collapse", "contract", "compress", "reduction",
             "złożenie", "zapadnięcie", "kompresja", "redukcja", "zwinięcie"],
    "BOUNDARY": ["boundary", "limit", "edge", "border", "threshold", "constraint",
                 "granica", "limit", "krawędź", "próg", "ograniczenie"],
    "SCOPE": ["scope", "range", "extent", "domain", "universal quantifier", "for all",
              "zakres", "obszar", "domena", "zasięg"],
    "AFFECT": ["affect", "emotion", "feeling", "mood", "sentiment", "joy", "fear", "anger", "love", "sadness",
               "afekt", "emocja", "emocji", "emocje", "emocją", "uczucie", "uczucia", "nastrój", "nastrojowy",
               "radość", "strach", "złość", "miłość", "smutek", "czujesz", "czuję", "czuć"],
    "CONSENT": ["consent", "agreement", "approval", "authorize", "opt-in", "permission granted",
                "zgoda", "przyzwolenie", "autoryzacja", "pozwolenie"],
    "SOURCE": ["source", "origin", "provenance", "citation", "attribution", "reference",
               "źródło", "pochodzenie", "proweniencja", "cytat", "przypisanie"],
    "MEMORY": ["memory", "recall", "remember", "past", "history", "episodic", "archive",
               "pamięć", "pamięci", "pamięcią", "pamiętać", "pamiętasz", "wspomnienie",
               "przeszłość", "historia", "wspominać", "mówiliśmy", "rozmawialiśmy"],
    "RISK": ["risk", "danger", "hazard", "threat", "vulnerability", "exposure",
             "ryzyko", "niebezpieczeństwo", "zagrożenie", "podatność"],
    "ASSERTION": ["assertion", "claim", "statement", "declare", "affirm",
                  "twierdzenie", "roszczenie", "oświadczenie", "deklaracja"],
    "CONDITION": ["condition", "conditional", "criterion", "prerequisite", "if then",
                  "warunek", "warunkowy", "kryterium", "jeśli"],
    "CAUSE": ["cause", "causal", "because", "reason", "consequence", "trigger", "effect of",
              "przyczyna", "powód", "ponieważ", "konsekwencja", "skutek"],
    "MODAL_POSSIBILITY": ["possible", "possibility", "might", "could", "potential", "plausible",
                          "możliwe", "możliwość", "mógłby", "potencjalny"],
    "MODAL_NECESSITY": ["necessary", "necessity", "must be", "essential", "inevitable", "required by",
                        "konieczne", "konieczność", "musi być", "niezbędny", "nieunikniony"],
    "MODAL_PERMISSION": ["permission", "may", "allowed", "permitted", "authorized to",
                         "pozwolenie", "dozwolone", "upoważniony"],
    "MODAL_OBLIGATION": ["obligation", "duty", "shall", "ought", "mandatory",
                         "obowiązek", "powinność", "musi", "powinien"],
    "UNCERTAINTY": ["uncertain", "uncertainty", "unclear", "ambiguous", "doubt", "unknown", "unverified",
                    "niepewność", "niepewny", "niejasny", "wątpliwość", "nieznany", "niezweryfikowany"],
    "SOURCE_REQUIRED": ["citation needed", "source unclear", "unverified source", "needs verification",
                        "wymaga cytowania", "źródło niejasne", "niezweryfikowane źródło"],
    "CANON_BLOCK": ["forbidden", "restricted", "off-limits", "prohibited", "blocked",
                    "zabronione", "ograniczone", "zablokowane"],
    "CONSENT_REQUIRED": ["authorization required", "consent required", "requires permission",
                         "wymaga zgody", "wymagana autoryzacja"],
    "ACTION_REQUEST": ["request", "please", "action item", "execute", "perform the following",
                       "prośba", "proszę", "wykonaj", "zrób to"],
    "REFUSAL": ["refuse", "refusal", "decline", "reject", "will not",
                "odmowa", "odmawiam", "odrzucić", "nie zrobię"],
    "PAUSE": ["pause", "halt", "suspend", "hold on", "wait for",
              "pauza", "zatrzymaj", "wstrzymaj", "poczekaj"],
    "SIMULATION_BOUNDARY": ["simulation", "hypothetical", "sandbox", "synthetic scenario", "thought experiment",
                            "symulacja", "hipotetyczny", "piaskownica", "eksperyment myślowy"],
    "UNRUH_DRIVE": ["unruh effect", "unruh radiation", "temporal friction", "acceleration horizon",
                    "efekt unruha", "tarcie temporalne"],
    "WARP_DRIFT": ["warp drive", "alcubierre", "spatial offset", "warp bubble",
                   "napęd warp", "bąbel warp"],
    "ATTRACTOR": ["attractor", "convergence", "fixpoint", "fixed point", "equilibrium", "basin of attraction",
                   "ciel", "noema", "soul", "tożsamość systemu", "system identity",
                   "atraktor", "zbieżność", "punkt stały", "równowaga"],
    "HYPOTHESIS": ["hypothesis", "suppose", "conjecture", "assume", "speculate", "working theory",
                   "hipoteza", "przypuszczenie", "domniemanie", "spekulacja", "teoria robocza"],
    "PREFERENCE": ["preference", "prefer", "favorite", "rather", "inclination", "bias toward",
                   "preferencja", "wolę", "ulubiony", "raczej", "skłonność"],
}

assert set(OPERATOR_ANCHORS.keys()) == set(ALL_OPERATOR_IDS), (
    "concept_classifier anchors must cover exactly the 36 canonical operators "
    f"(missing: {set(ALL_OPERATOR_IDS) - set(OPERATOR_ANCHORS.keys())}, "
    f"extra: {set(OPERATOR_ANCHORS.keys()) - set(ALL_OPERATOR_IDS)})"
)


def classify_text(text: str) -> tuple[str, float]:
    """Return the best evidenced operator and its lexical score.

    The score is evidence, not a generated embedding.  ``UNCERTAINTY`` is
    returned when no registered anchor matches; this keeps unknown concepts
    visible instead of inventing a deterministic-but-arbitrary operator.
    """
    import re

    words = set(re.findall(r"[a-ząćęłńóśźż0-9]+", text.casefold().replace("_", " ").replace(":", " ")))
    best_op: str | None = None
    best_score = 0.0
    for op_id, anchors in OPERATOR_ANCHORS.items():
        anchor_words: set[str] = set()
        for anchor in anchors:
            anchor_words.update(re.findall(r"[a-ząćęłńóśźż0-9]+", anchor.casefold()))
        # Prefix stem matching — obsługuje fleksję PL (synchronizację/synchronizacja,
        # emocji/emocja, pamięcią/pamięć). Porównuje pierwsze N-2 znaków obu słów
        # gdzie N = min(len). Minimalna długość prefiksu: 5 znaków.
        score = 0.0
        for w in words:
            matched = False
            for aw in anchor_words:
                if matched:
                    break
                # Exact substring match (en phrases like "geometric phase")
                if len(aw) >= 4 and (aw in w or w in aw):
                    score += 1.0 + 0.3 * len(aw)
                    matched = True
                    continue
                # Prefix match dla fleksji PL: porównaj pierwsze N-2 znaków
                _stem_len = min(len(aw), len(w)) - 2
                if _stem_len >= 4 and aw[:_stem_len] == w[:_stem_len]:
                    score += 0.8 + 0.2 * _stem_len
                    matched = True
        if score > best_score:
            best_op, best_score = op_id, score
    return (best_op or "UNCERTAINTY"), best_score


def score_document(term_weights: dict[str, float], top_k: int = 3) -> list[tuple[str, float]]:
    """Score a document's terms (term -> tfidf weight) against all 36 operators.

    Returns up to `top_k` (operator_id, score) pairs sorted descending,
    excluding operators with zero score entirely (no anchor matched).
    """
    terms_lower = {t.lower(): w for t, w in term_weights.items()}
    scores: dict[str, float] = {}
    for op_id, anchors in OPERATOR_ANCHORS.items():
        total = 0.0
        for anchor in anchors:
            for term, weight in terms_lower.items():
                if anchor in term or term in anchor:
                    total += weight
        if total > 0.0:
            scores[op_id] = total

    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    return ranked[:top_k]
