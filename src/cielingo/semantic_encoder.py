"""CIELingo Semantic Encoder — twój TRANSFORMEM, wektoryzowany.

Używa transformer_features.FeatureToken + encode_feature_token() jako
warstwy ekstrakcji cech. Żadnych zewnętrznych zależności — tylko numpy.
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from .htri_brain_map import BRAIN_BY_ID

# ── TRANSFORMEM — transformer_features jako silnik cech ────────────────────

_FEATURE_SPEC_PATH = (
    Path(__file__).resolve().parents[2]
    / "src/ciel_lingophysics_lns_repo_v2_3"
    / "data" / "transformer_features" / "feature_spec.json"
)

try:
    from ciel_lingophysics_lns_repo_v2_3.src.lingophysics.transformer_features import (
        FeatureToken,
        encode_feature_token,
        load_feature_spec,
        load_feature_tensor,
        tokens_from_tensor,
        card_type_vector,
        role_vector,
    )
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/cielingo/semantic_encoder.py:36 quiet except scope=<module> reason=no_log_no_raise")
    # fallback: import względem repozytorium lingophysics
    import importlib.util as _ilu
    _TF_PATH = (
        Path(__file__).resolve().parents[2]
        / "src/ciel_lingophysics_lns_repo_v2_3"
        / "src" / "lingophysics" / "transformer_features.py"
    )
    if _TF_PATH.exists():
        _spec = _ilu.spec_from_file_location("transformer_features_runtime", _TF_PATH)
        _mod = _ilu.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
        FeatureToken = _mod.FeatureToken
        encode_feature_token = _mod.encode_feature_token
        load_feature_spec = _mod.load_feature_spec
        load_feature_tensor = _mod.load_feature_tensor
        tokens_from_tensor = _mod.tokens_from_tensor
        card_type_vector = _mod.card_type_vector
        role_vector = _mod.role_vector
    else:
        FeatureToken = None
        encode_feature_token = None

_SPEC = load_feature_spec(str(_FEATURE_SPEC_PATH)) if _FEATURE_SPEC_PATH.exists() else {}

SECTOR_NAMES: tuple[str, ...] = (
    "CONCEPT_CARD", "OPERATOR_CARD", "GRAMMAR_CARD", "CASE_GAUGE_CARD",
    "TAME_CARD", "DEICTIC_CARD", "SCOPE_CARD", "EVENT_FRAME",
    "ONTOLOGICAL_ASPECT", "UNKNOWN",
)

# ── Wektoryzacja — budowa osi projekcji z feature_spec ─────────────────────

def _spec_dim() -> dict[str, int]:
    dims = {}
    for group_name, group in _SPEC.get("feature_groups", {}).items():
        if isinstance(group, dict):
            dims[group_name] = int(group.get("dim", 0))
    return dims

def _total_spec_dim() -> int:
    return sum(_spec_dim().values())

# + aux: concept_mass, operator_incidence, vowel_ratio, word_length_norm, affect_bias = 5
_AUX_DIM = 5

def _feature_dim() -> int:
    return _total_spec_dim() + _AUX_DIM


# ── Budowa osi projekcji w przestrzeni spec ────────────────────────────────

def _build_axes() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """W1, W2 (faza), WO (sektory) — pełne 60-wymiarowe osie projekcji.

    W1: Concept/Concrete (+) vs Operator/Abstract (-) — rozłożone na wszystkie grupy.
    W2: Affective/Experiential (+) vs Formal/Structural (-).
    WO: 10 centroidów sektorowych w pełnej przestrzeni 60D.
    """
    dims = _spec_dim()
    spec_total = sum(dims.values())
    n_feat = spec_total + _AUX_DIM

    off: dict[str, int] = {}
    pos = 0
    for name, d in dims.items():
        off[name] = pos
        pos += d
    a = spec_total

    w1 = np.zeros(n_feat, dtype=np.float64)
    w2 = np.zeros(n_feat, dtype=np.float64)

    # ── helper ──
    def _set(grid: str, labels: tuple[str, ...], weights: tuple[float, ...],
             target: np.ndarray, axis: int) -> None:
        g = off.get(grid)
        if g is None:
            return
        for label, w in zip(labels, weights):
            if label in _SPEC.get("feature_groups", {}).get(grid, {}).get("labels", []):
                labels_list = _SPEC["feature_groups"][grid]["labels"]
                target[g + labels_list.index(label)] = w * axis

    # ── W1: Concept/Concrete (+) vs Operator/Abstract (-) ──
    _set("card_type", ("CONCEPT_CARD", "OPERATOR_CARD", "GRAMMAR_CARD", "EVENT_FRAME"),
         (1.5, -1.5, -0.5, 0.3), w1, 1)
    _set("operator", ("identity","possession","containment","spatial","temporal","logical","comparison","modal"),
         (-0.3, -0.3, -0.3, -0.5, -0.5, -0.7, -0.3, -0.5), w1, 1)
    _set("event_frame", ("agent","patient","theme","recipient","experiencer","stimulus","source","goal"),
         (0.5, 0.3, -0.3, 0.2, -0.3, -0.5, 0.2, -0.2), w1, 1)
    _set("case_gauge", ("nom","acc","gen","dat","ins","loc","voc"),
         (0.5, 0.3, 0.0, -0.2, -0.5, -0.3, 0.1), w1, 1)
    _set("tame", ("past","present","future","perfective","imperfective","modal","evidential"),
         (0.3, 0.2, -0.2, 0.3, 0.3, -0.5, -0.3), w1, 1)
    _set("scope", ("all","some","none","neg_outside","neg_inside","unresolved"),
         (0.3, 0.2, -0.3, -0.2, -0.2, -0.3), w1, 1)
    _set("deixis", ("place","time","manner","source","destination"),
         (0.3, 0.2, -0.2, -0.3, 0.2), w1, 1)
    _set("phase", ("synonym_phase","antonym_phase","surface_intent_phase","unresolved_phase"),
         (0.3, 0.3, -0.2, -0.5), w1, 1)
    w1[a] = 0.5      # concept_mass
    w1[a+1] = -0.8   # operator_incidence
    w1[a+4] = 0.3    # affect_bias (concept carries more affect)

    # ── W2: Affective/Experiential (+) vs Formal/Structural (-) ──
    _set("card_type", ("CONCEPT_CARD","EVENT_FRAME","OPERATOR_CARD","GRAMMAR_CARD","CASE_GAUGE_CARD"),
         (0.5, 0.5, -0.5, -0.5, -0.5), w2, 1)
    _set("operator", ("identity","possession","containment","spatial","temporal","logical","comparison","modal"),
         (-0.5, -0.3, -0.3, -0.2, 0.3, -0.3, 0.0, 0.5), w2, 1)
    _set("event_frame", ("agent","patient","theme","recipient","experiencer","stimulus","source","goal"),
         (-0.5, -0.3, 0.3, 0.0, 0.7, 0.5, -0.2, 0.0), w2, 1)
    _set("case_gauge", ("nom","acc","gen","dat","ins","loc","voc"),
         (-0.3, -0.3, 0.0, 0.3, 0.3, 0.3, 0.1), w2, 1)
    _set("tame", ("past","present","future","perfective","imperfective","modal","evidential"),
         (0.2, 0.3, 0.1, -0.3, 0.3, 0.1, -0.3), w2, 1)
    _set("scope", ("all","some","none","neg_outside","neg_inside","unresolved"),
         (-0.3, 0.3, -0.3, -0.2, -0.2, 0.0), w2, 1)
    _set("deixis", ("place","time","manner","source","destination"),
         (0.3, 0.2, -0.2, -0.2, 0.2), w2, 1)
    _set("phase", ("synonym_phase","antonym_phase","surface_intent_phase","unresolved_phase"),
         (-0.3, -0.3, 0.5, 0.0), w2, 1)
    w2[a] = 0.2      # concept_mass
    w2[a+1] = -0.3   # operator_incidence
    w2[a+2] = 0.3    # vowel_ratio (sonority ~ affect)
    w2[a+4] = 1.5    # affect_bias — główny nośnik afektu

    # Gram-Schmidt: ortogonalizacja W2 względem W1
    w2 = w2 - np.dot(w2, w1) / (np.dot(w1, w1) + 1e-12) * w1

    w1 /= np.linalg.norm(w1) + 1e-12
    w2 /= np.linalg.norm(w2) + 1e-12

    # WO: centroidy sektorów — każdy sektor ma swój wektor w 60D
    n_sectors = len(SECTOR_NAMES)
    wo = np.zeros((n_sectors, n_feat), dtype=np.float64)
    for i in range(n_sectors):
        theta = 2.0 * math.pi * i / n_sectors
        # card_type one-hot jako baza
        ct_off = off.get("card_type", 0)
        wo[i, ct_off + i] = 1.0
        # afekt moduluje centroid sinusoidalnie
        wo[i, a+4] = 0.3 * math.sin(2.0 * theta)
        # koncept_mass jako promień
        wo[i, a] = 0.2 * math.cos(theta)
        # operator_incidence
        wo[i, a+1] = 0.2 * math.sin(theta)
        row_norm = np.linalg.norm(wo[i]) + 1e-12
        wo[i] /= row_norm

    return w1, w2, wo


# ── Ekstrakcja cech — wierne użycie transformer_features ──────────────────

_AFFECT_LEXICON: dict[str, float] = {
    "love": 0.9, "kocham": 0.9, "miłość": 0.9, "joy": 0.8, "radość": 0.8,
    "peace": 0.8, "spokój": 0.7, "hope": 0.7, "nadzieja": 0.7, "trust": 0.7,
    "fear": -0.8, "strach": -0.8, "pain": -0.8, "ból": -0.8,
    "death": -0.7, "śmierć": -0.7, "betrayal": -0.9, "zdrada": -0.9,
    "anger": -0.7, "gniew": -0.7, "trauma": -0.8, "despair": -0.8, "rozpacz": -0.8,
    "chaos": -0.6, "order": 0.6, "consciousness": 0.3, "soul": 0.5, "dusza": 0.5,
    "cielingo": 0.5, "noema": 0.4, "htri": 0.3, "ciel": 0.4,
    "silence": 0.3, "cisza": 0.3, "void": -0.3, "pustka": -0.3,
    "water": 0.1, "woda": 0.1, "fire": 0.3, "ogień": 0.3,
    "truth": 0.6, "prawda": 0.6, "beauty": 0.7, "piękno": 0.6,
}

def _vowel_ratio(word: str) -> float:
    vowels = set("aeiouyąęióAEIOUYĄĘIÓ")
    if not word:
        return 0.5
    v = sum(1 for ch in word if ch in vowels)
    return v / len(word)

def _word_length_bins(word: str) -> tuple[float, float, float]:
    n = len(word)
    short = max(0.0, min(1.0, (4 - n) / 3))
    long_ = max(0.0, min(1.0, (n - 7) / 4))
    medium = max(0.0, 1.0 - short - long_)
    return (short, medium, long_)

def _affect_bias(word: str) -> float:
    return _AFFECT_LEXICON.get(word.lower().strip(".,!?;:\"'()[]{}"), 0.0)

def _semantic_mass(word: str) -> float:
    n = len(word)
    if n <= 2: return 0.15
    if n <= 4: return 0.35
    if n <= 6: return 0.55
    if n <= 8: return 0.75
    if n <= 12: return 0.90
    return 0.98

def _operator_incidence(word: str) -> float:
    fw = {
        "the","a","an","is","are","was","were","be","been","have","has","had",
        "do","does","did","will","would","shall","should","may","might","must",
        "can","could","to","of","in","on","at","by","for","with","from",
        "and","or","but","nor","yet","so","if","then","else","when","while",
        "that","this","these","those","i","you","he","she","it","we","they",
        # Polish
        "nie","się","na","w","z","do","od","po","przy","nad","pod","przed","za",
        "i","a","oraz","ale","lub","albo","więc","zatem","że","żeby","aby",
        "gdy","jeśli","jak","tak","tu","tam","co","kto","czy","to","ten","ta",
        "jest","są","był","była","ma","mam","masz",
        # expanded Polish operators
        "bez","dla","między","ponad","przeciw","według","obok","koło","wśród",
        "przez","podczas","wzdłuż","wokół","wewnątrz","zewnątrz","dzięki",
        "mimo","pomimo","zamiast","poprzez","wobec","względem","odnośnie",
        "być","byłem","byłeś","byli","były","będzie","będą","został","została",
        "zostać","staje","stał","stała","móc","może","mogą","mógł","mogła",
        "musieć","musi","muszą","musiał","musiała","chcieć","chce","chcą",
        "chciał","chciała","wiedzieć","wie","wiedzą","wiedział","wiedziała",
        "ten","ta","to","te","ci","tamte","tamta","tamto","tamci",
        "mój","moja","moje","twój","twoja","twoje","jego","jej","ich",
        "nasz","nasza","nasze","wasz","wasza","wasze",
        "kiedy","gdzie","skąd","dokąd","dlaczego","czemu","jak","jaki","jaka",
        "który","która","które","którzy","ile","któż","cóż","kogóż",
        "bardzo","także","również","jednak","natomiast","ponadto",
        "niestety","oczywiście","może","możliwe","raczej","chyba","pewnie",
        "zawsze","nigdy","często","rzadko","już","jeszcze","dopiero",
        "właśnie","nawet","aż","tylko","jedynie","choć","chociaż",
    }
    return 0.8 if word.lower().strip(".,!?;:\"'()[]{}") in fw else 0.05


def _build_feature_vector(
    card_type: str,
    roles: tuple[str, ...],
    concept_mass: float,
    operator_incidence: float,
    *,
    word: str = "",
) -> np.ndarray:
    """Wektoryzacja wg feature_spec: [spec_groups (55) | aux (5)] = 60."""
    dims = _spec_dim()
    spec_total = sum(dims.values())
    n_feat = spec_total + _AUX_DIM
    vec = np.zeros(n_feat, dtype=np.float64)

    off = {}
    pos = 0
    for name, d in dims.items():
        off[name] = pos
        pos += d

    if "card_type" in off:
        ct_off = off["card_type"]
        if card_type in SECTOR_NAMES:
            vec[ct_off + SECTOR_NAMES.index(card_type)] = 1.0
        else:
            vec[ct_off + SECTOR_NAMES.index("UNKNOWN")] = 1.0

    if "event_frame" in off:
        ef_off = off["event_frame"]
        labels = _SPEC.get("feature_groups", {}).get("event_frame", {}).get("labels", [])
        for label in roles:
            if label in labels:
                vec[ef_off + labels.index(label)] = 1.0

    a = spec_total
    vec[a] = concept_mass
    vec[a + 1] = operator_incidence
    vec[a + 2] = _vowel_ratio(word)
    vec[a + 3] = min(1.0, len(word) / 20.0)  # word_length_norm
    vec[a + 4] = _affect_bias(word)           # affect_bias

    return vec


# ── Parsowanie tekstu przez lingo bridge ───────────────────────────────────

def _tokenize(text: str) -> list[dict[str, Any]]:
    try:
        from ciel_sot_agent.cielingo_bridge import build_lingo_frame
        frame = build_lingo_frame(text)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/cielingo/semantic_encoder.py:313 quiet except scope=_tokenize reason=return _fallback(text)")
        return _fallback(text)

    tokens: list[dict[str, Any]] = []
    seen: set[str] = set()

    for ct in frame.get("concept_tokens", []):
        s = ct.lower()
        if s not in seen:
            seen.add(s)
            tokens.append({"surface": s, "card_type": "CONCEPT_CARD", "roles": ("theme",)})

    for ot in frame.get("operator_tokens", []):
        s = ot.lower()
        if s not in seen:
            seen.add(s)
            tokens.append({"surface": s, "card_type": "OPERATOR_CARD", "roles": ()})

    for ur in frame.get("unresolved", []):
        s = ur.lower()
        if s not in seen:
            seen.add(s)
            tokens.append({"surface": s, "card_type": "UNKNOWN", "roles": ()})

    return tokens if tokens else _fallback(text)

def _fallback(text: str) -> list[dict[str, Any]]:
    seen: set[str] = set()
    tokens = []
    for word in text.split():
        s = word.strip(".,!?;:\"'()[]{}").lower()
        if s and s not in seen:
            seen.add(s)
            if _operator_incidence(s) >= 0.5:
                tokens.append({"surface": s, "card_type": "OPERATOR_CARD", "roles": ()})
            else:
                tokens.append({"surface": s, "card_type": "CONCEPT_CARD", "roles": ("theme",)})
    return tokens


def _normalize_pl(word: str) -> str:
    """Strip Polish diacritics for lookup."""
    trans = str.maketrans("ąćęłńóśźżĄĆĘŁŃÓŚŹŻ", "acelnoszzACELNOSZZ")
    return word.translate(trans)

def _resolve_oscillator(tokens: list[dict[str, Any]], sector_fallback: int) -> int:
    """Głosowanie wszystkich tokenów na oscylator. Najsilniejszy wygrywa."""
    votes: dict[int, float] = {}
    for t in tokens:
        s = _normalize_pl(t["surface"])
        # try direct match, then normalized
        osc = _NAMED_OSC.get(s) or _NAMED_OSC.get(t["surface"])
        if osc is not None:
            mass = len(s) / 20.0
            votes[osc] = votes.get(osc, 0.0) + mass
    if votes:
        return max(votes, key=votes.get)
    return _SECTOR2OSC.get(sector_fallback, 13)


# ── Mapa nazwanych jednostek → oscylator mózgu ────────────────────────────

_NAMED_OSC: dict[str, int] = {
    # ── English ──
    "adrian": 0, "ciel": 1, "apocalyptos": 2, "noema": 21,
    "htri": 16, "omega": 20, "cielingo": 8, "orchorbital": 6,
    "sot": 22, "cqcl": 10, "sapiens": 18, "brain": 20,
    "semantic": 21, "affect": 2, "memory": 10, "ethics": 1,
    "chaos": 11, "order": 0, "consciousness": 13,
    "truth": 1, "love": 2, "fear": 11, "time": 10,
    "dream": 20, "soul": 5, "god": 1, "death": 11,
    "pain": 11, "light": 2, "dark": 11, "peace": 18,
    "hope": 1, "void": 20, "silence": 20, "water": 5,
    "fire": 19, "storm": 11, "beauty": 2, "mind": 0,
    "wisdom": 1, "knowledge": 1,
    "space": 6, "time": 10, "logic": 0, "poem": 8,
    "word": 8, "star": 20, "wind": 19,
    # ── Polish ──
    "strach": 11, "ból": 11, "śmierć": 11, "zdrada": 11,
    "miłość": 2, "pokój": 18, "radość": 2, "gniew": 11,
    "spokój": 18, "nadzieja": 1, "cisza": 20,
    "prawda": 1, "piękno": 2, "chaos": 11, "porządek": 0,
    "dusza": 5, "woda": 5, "ogień": 19, "wiatr": 19,
    "gwiazda": 20, "gwiazdy": 20, "nieskończoność": 20,
    "świadomość": 13, "pamięć": 10, "czas": 10,
    "etyka": 1, "wolność": 0, "samotność": 13,
    "przestrzeń": 6, "logika": 0, "wiersz": 8,
    "słowo": 8, "słowa": 8, "sen": 20,
    "pustka": 20, "noc": 11, "dzień": 2,
    "światło": 2, "ciemność": 11, "dobro": 1, "zło": 11,
    "początek": 0, "koniec": 20, "życie": 18, "śmierć": 11,
    "matematyka": 6, "symetria": 6, "liczba": 6,
    "zero": 20, "jeden": 0, "dwa": 6, "trzy": 20,
    "rzeka": 5, "morze": 5, "las": 5, "góra": 5,
    "słońce": 2, "księżyc": 2, "ziemia": 5,
    "ptak": 5, "liść": 5, "drzewo": 5,
    "twórczość": 2, "tworzenia": 2, "harmonia": 18,
    "przemoc": 11, "wojna": 11, "pokój": 18,
    "myśl": 8, "myślenie": 0, "rozum": 0,
    "uczucie": 2, "emocja": 2, "emocje": 2,
    # ── Polish ASCII (bez polskich znaków) ──
    "milosc": 2, "piekno": 2, "swiatlo": 2, "ciemnosc": 11,
    "swiadomosc": 13, "nieskonczonosc": 20, "smierc": 11,
    "przestrzen": 6, "zlo": 11, "zycie": 18, "tworczosc": 2,
    "gwiazdy": 20, "slonce": 2, "ksiezyc": 2, "drzewo": 5,
    "słonce": 2, "księżyc": 2,
}

_SECTOR2OSC: dict[int, int] = {
    0: 8, 1: 0, 2: 6, 3: 13, 4: 10,
    5: 7, 6: 16, 7: 21, 8: 20, 9: 13,
}


# ── Public API ─────────────────────────────────────────────────────────────

@dataclass
class EncoderResult:
    text: str
    embedding: np.ndarray
    phase: float
    sector_dist: np.ndarray
    dominant_sector: str
    coherence: float
    brain_region: str
    brain_oscillator_id: int
    token_count: int
    per_token: list[dict[str, Any]]


class CIELingoSemanticEncoder:
    def __init__(self) -> None:
        self._W1, self._W2, self._WO = _build_axes()
        self._spec = _SPEC
        # Centrum projekcji: punkt neutralny między CONCEPT_CARD a OPERATOR_CARD
        v_con = _build_feature_vector("CONCEPT_CARD", ("theme",), 0.55, 0.05, word="the")
        v_op = _build_feature_vector("OPERATOR_CARD", (), 0.15, 0.80, word="the")
        self._CENTER = (v_con + v_op) / 2.0

    def encode(self, text: str) -> EncoderResult:
        tokens = _tokenize(text)
        if not tokens:
            return self._empty(text)

        feat_vecs: list[np.ndarray] = []
        per_token_out: list[dict[str, Any]] = []

        for t in tokens:
            mass = _semantic_mass(t["surface"])
            inc = _operator_incidence(t["surface"])
            fv = _build_feature_vector(
                card_type=t["card_type"],
                roles=t.get("roles", ()),
                concept_mass=mass,
                operator_incidence=inc,
                word=t["surface"],
            )
            feat_vecs.append(fv)
            phi_t = self._phase(fv - self._CENTER)
            per_token_out.append({
                "surface": t["surface"],
                "card_type": t["card_type"],
                "phase": round(phi_t, 6),
                "concept_mass": mass,
                "operator_incidence": inc,
            })

        embedding = np.mean(feat_vecs, axis=0)
        centered = embedding - self._CENTER
        phase = self._phase(centered)

        sector_dist = self._sectors(embedding)
        dom_idx = int(np.argmax(sector_dist))
        dominant_sector = SECTOR_NAMES[dom_idx]

        coherence = self._coherence([self._phase(fv - self._CENTER) for fv in feat_vecs])

        osc_id = _resolve_oscillator(tokens, dom_idx)
        brain_region = BRAIN_BY_ID.get(osc_id, BRAIN_BY_ID[0]).brain_region

        return EncoderResult(
            text=text, embedding=embedding, phase=phase,
            sector_dist=sector_dist, dominant_sector=dominant_sector,
            coherence=coherence, brain_region=brain_region,
            brain_oscillator_id=osc_id, token_count=len(tokens),
            per_token=per_token_out,
        )

    def _phase(self, v: np.ndarray) -> float:
        y = float(np.dot(self._W1, v))
        x = float(np.dot(self._W2, v))
        return float(math.atan2(y, x)) % (2.0 * math.pi)

    def _sectors(self, v: np.ndarray) -> np.ndarray:
        sims = self._WO @ v
        logits = sims / 0.5
        logits -= logits.max()
        probs = np.exp(logits)
        return probs / probs.sum()

    @staticmethod
    def _coherence(phases: list[float]) -> float:
        if not phases:
            return 0.5
        sin_s = sum(math.sin(p) for p in phases)
        cos_s = sum(math.cos(p) for p in phases)
        r = math.sqrt(sin_s**2 + cos_s**2) / len(phases)
        return float(np.clip(r, 0.0, 1.0))

    @staticmethod
    def _empty(text: str) -> EncoderResult:
        dist = np.full(len(SECTOR_NAMES), 1.0 / len(SECTOR_NAMES))
        return EncoderResult(
            text=text, embedding=np.zeros(_feature_dim(), dtype=np.float64),
            phase=0.0, sector_dist=dist, dominant_sector="UNKNOWN",
            coherence=0.5, brain_region="insula", brain_oscillator_id=13,
            token_count=0, per_token=[],
        )


_encoder: CIELingoSemanticEncoder | None = None

def get_encoder() -> CIELingoSemanticEncoder:
    global _encoder
    if _encoder is None:
        _encoder = CIELingoSemanticEncoder()
    return _encoder

def encode(text: str) -> EncoderResult:
    return get_encoder().encode(text)

__all__ = [
    "CIELingoSemanticEncoder", "EncoderResult",
    "SECTOR_NAMES", "encode", "get_encoder",
]
