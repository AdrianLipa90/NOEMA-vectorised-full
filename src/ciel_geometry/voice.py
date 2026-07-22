from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import hashlib
import math
import os
import struct
import time
import uuid
from pathlib import Path
from typing import Optional

import numpy as np

from .weighting import canonical_weighting_from_phase_metadata
from .paths import P

SURFACE_ROOT = Path("/dev/shm/ciel_noema")
PHASE_INDEX = Path(P.PHASE_DATA) / "PHASE_INDEX"
LIBRARY_VECTORS = PHASE_INDEX / "library_index.npy"
LIBRARY_META = PHASE_INDEX / "library_meta.npy"
KNOWLEDGE_GRAPH = PHASE_INDEX / "knowledge_graph.json"
AGENT_BACKEND_URL = "http://127.0.0.1:18520/v1/chat/completions"
AGENT_BACKEND_TIMEOUT = 2.0
AGENT_CACHE_MAX_SIZE = 64
SURFACE_CACHE_TTL = 0.5
QUERY_TEXT_WINDOW = 64
QUERY_VECTOR_DIM = 36
QUERY_WORD_MIN_LEN = 3
SHORT_QUERY_WORD_LIMIT = 8
NEAREST_TOP_K = 6
KG_TOP_K = 5
DEFAULT_NEAREST_TOPIC_TOP_K = 3
DEFAULT_KG_NEIGHBORS_TOP_K = 5
REF_CONTEXT_DOC_LIMIT = 3
REF_CONTEXT_WORD_LIMIT = 3
REF_CONTEXT_SNIPPET_LIMIT = 80
MAX_AGENT_THEMES = 6
MAX_TOPIC_LABEL_LENGTH = 20
MAX_NAME_WORDS = 5
MIN_NAME_WORD_LENGTH = 3
MAX_NAME_SNIPPET_LENGTH = 60
NEAREST_RETURN_LIMIT = 2
SNIPPET_LIMIT = 200
SYSTEM_QUERY_SNIPPET_LIMIT = 100
CONTEXT_THEME_LIMIT = 4
SURFACE_COHERENCE_DIM = 36.0
DEFAULT_ATTRACTOR_ERR = 99.0
REPAIR_CONTRADICTION_RISK_THRESHOLD = 0.55
REPAIR_CLOSURE_PENALTY_THRESHOLD = 0.60
REPAIR_COHERENCE_THRESHOLD = 0.50
CONSOLIDATE_MASS_THRESHOLD = 8.0
CONSOLIDATE_UNRUH_THRESHOLD = 30.0
CONSOLIDATE_SEMANTIC_MASS_THRESHOLD = 0.70
EXPLORE_COHERENCE_THRESHOLD = 0.30
INFORM_COHERENCE_THRESHOLD = 0.70
SUBJECTIVE_STABLE_COHERENCE_THRESHOLD = 0.85
SUBJECTIVE_GOOD_COHERENCE_THRESHOLD = 0.70
SUBJECTIVE_FOCUSED_COHERENCE_THRESHOLD = 0.50
SUBJECTIVE_SEARCHING_COHERENCE_THRESHOLD = 0.30
SYSTEM_QUERY_CP_THRESHOLD = 0.50
CONSOLIDATE_CP_THRESHOLD = 0.50
REPAIR_CP_THRESHOLD = 0.40
REPAIR_UNRUH_THRESHOLD = 20.0
CONSOLIDATE_MASS_EMPHASIS_THRESHOLD = 5.0

TOPIC_CACHE: dict[str, str] = {}
KG_CACHE: dict = {"nodes": {}, "edges": []}
LIBRARY_CACHE: dict = {"vectors": None, "meta": None}
SURFACE_CACHE: dict[str, float | int] = {}
SURFACE_CACHE_TS = 0.0
AGENT_CACHE: dict[str, dict] = {}
AGENT_CACHE_TS = 0.0

_TOPIC_STOPLIST = frozenset(
    t.lower() for t in [
        "nieznany_autor", "unknown", "default", "harmonictranscendence",
        "ciel. nie", "ciel nie",
    ]
)

_SEMANTIC_KEYWORDS = frozenset(
    k.lower() for k in [
        "htri", "phasenav", "cielingo", "kuramoto", "tiered",
        "orchestrator", "neutrino", "pmns", "gravity", "warp",
        "tardis", "unruh", "holonomy", "berry", "euler",
        "agent", "attractor", "resonance", "bridge", "dual",
        "surface", "analog", "blend", "phase", "memory",
        "consolidation", "semantic", "collatz", "orbital",
        "metatime", "noema", "sapiens", "topology",
        "oscillator", "harmonic", "closure", "flavor",
        "consolidator", "sentinel", "daemon", "registry",
        "consciousness", "intention", "affect", "emotion",
        "recursive", "fractal", "resonant", "quantum",
        "spacetime", "emergence", "coherence", "identity",
    ]
)

_SEMANTIC_TOPIC_PREFIXES = frozenset(
    k.lower() for k in [
        "recursive", "resonant", "harmonic", "quantum", "fractal",
        "emergent", "universal", "informational", "cosmic",
        "unified", "empirical", "temporal", "semantic",
        "optimized", "primordial", "numerical", "new",
        "loop", "light", "layer", "modal", "machine",
        "neural", "nonlinear", "orbital", "perfect",
    ]
)

_AUTHOR_INDICATORS = frozenset(
    k.lower() for k in [
        "adrian lipa", "surmont", "valov", "sharmila", "sarfatti",
        "bohr", "planck", "einstein", "heisenberg", "schrödinger",
        "michio", "kaku", "penrose", "hameroff", "tegtmark",
        "susskind", "maldacena", "wilczek", "t'hooft",
        "feynman", "dirac", "witten", "greene", "hawking",
    ]
)


def _load_library():
    if LIBRARY_CACHE["vectors"] is not None:
        return
    try:
        v = np.load(str(LIBRARY_VECTORS))
        m = np.load(str(LIBRARY_META), allow_pickle=True)
        LIBRARY_CACHE["vectors"] = v.astype(np.float64)
        LIBRARY_CACHE["meta"] = m
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/voice.py:83 quiet except scope=_load_library reason=no_log_no_raise")
        LIBRARY_CACHE["vectors"] = np.zeros((1, 36), dtype=np.float64)
        LIBRARY_CACHE["meta"] = np.array(
            [("000000000000", "fallback", "unknown", "default", "", False, "")]
        )


def _load_kg():
    if KG_CACHE["nodes"]:
        return
    try:
        with open(KNOWLEDGE_GRAPH) as f:
            data = json.load(f)
        KG_CACHE["nodes"] = {n["id"]: n for n in data.get("nodes", [])}
        KG_CACHE["edges"] = data.get("edges", [])
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/voice.py:98 quiet except scope=_load_kg reason=no_log_no_raise")
        KG_CACHE["nodes"] = {"operator:IDENTITY": {"id": "operator:IDENTITY", "label": "IDENTITY", "type": "operator"}}
        KG_CACHE["edges"] = []


def _read_surface() -> dict[str, float | int]:
    global SURFACE_CACHE_TS
    now = time.monotonic()
    if now - SURFACE_CACHE_TS < SURFACE_CACHE_TTL:
        return SURFACE_CACHE
    result = {"tick": 0, "phi": None, "coh": 0.0, "gravity": [0.0] * 4, "flavor": [0.0] * 6, "attractor": "unknown", "attractor_err": DEFAULT_ATTRACTOR_ERR}
    try:
        raw = open(SURFACE_ROOT / "tick", "rb").read()
        result["tick"] = struct.unpack("Q", raw)[0]
        raw = open(SURFACE_ROOT / "phi", "rb").read()
        phi = list(struct.unpack("36d", raw))
        result["phi"] = phi
        result["coh"] = abs(sum(math.e ** (1j * p) for p in phi)) / SURFACE_COHERENCE_DIM
        if (SURFACE_ROOT / "gravity").exists():
            result["gravity"] = list(struct.unpack("4d", open(SURFACE_ROOT / "gravity", "rb").read()))
        if (SURFACE_ROOT / "flavor").exists():
            result["flavor"] = list(struct.unpack("6d", open(SURFACE_ROOT / "flavor", "rb").read()))
        if (SURFACE_ROOT / "health").exists():
            try:
                h = json.loads(open(SURFACE_ROOT / "health").read())
                result["attractor"] = h.get("attractor", "unknown")
                result["attractor_err"] = h.get("attractor_err", DEFAULT_ATTRACTOR_ERR)
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/voice.py:125 quiet except scope=_read_surface reason=pass")
                pass
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/voice.py:127 quiet except scope=_read_surface reason=pass")
        pass
    SURFACE_CACHE.clear()
    SURFACE_CACHE.update(result)
    SURFACE_CACHE_TS = now
    return result


def _query_agent_backend(text: str, max_age: float = 30.0) -> dict:
    global AGENT_CACHE, AGENT_CACHE_TS
    now = time.monotonic()
    text_key = text.strip().lower()[:QUERY_TEXT_WINDOW]
    cache_key = f"{text_key}:{int(now // max_age)}"
    if cache_key in AGENT_CACHE:
        return AGENT_CACHE[cache_key]
    try:
        import urllib.request as _req
        body = json.dumps({
            "model": "ciel-consolidator",
            "messages": [{"role": "user", "content": text}],
            "stream": False
        }).encode()
        r = _req.Request(AGENT_BACKEND_URL, data=body, headers={"Content-Type": "application/json"})
        with _req.urlopen(r, timeout=AGENT_BACKEND_TIMEOUT) as resp:
            data = json.loads(resp.read())
        content = json.loads(data["choices"][0]["message"]["content"])
        AGENT_CACHE[cache_key] = content
        if len(AGENT_CACHE) > AGENT_CACHE_MAX_SIZE:
            old_keys = list(AGENT_CACHE.keys())[:-AGENT_CACHE_MAX_SIZE]
            for k in old_keys:
                del AGENT_CACHE[k]
        return content
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/voice.py:160 quiet except scope=_query_agent_backend reason=return {\"themes\": [], \"affect\": \"neutral\", \"anchor_terms\": [], \"essence\": \"\", \"hunch\": \"\"}")
        return {"themes": [], "affect": "neutral", "anchor_terms": [], "essence": "", "hunch": ""}


def nearest_topic(op_vector: np.ndarray, top_k: int = DEFAULT_NEAREST_TOPIC_TOP_K) -> list[dict]:
    _load_library()
    vecs = LIBRARY_CACHE["vectors"]
    meta = LIBRARY_CACHE["meta"]
    q = np.asarray(op_vector, dtype=np.float64).ravel()
    q_norm = q / (np.linalg.norm(q) + 1e-30)
    scores = vecs @ q_norm
    idx = np.argsort(-scores)[:top_k]
    return [
        {
            "id": meta[i]["id"],
            "filename": str(meta[i]["filename"]),
            "author": str(meta[i]["author"]),
            "topic": str(meta[i]["topic"]),
            "score": float(scores[i]),
        }
        for i in idx
    ]


def kg_neighbors(node_id: str, top_k: int = DEFAULT_KG_NEIGHBORS_TOP_K) -> list[dict]:
    _load_kg()
    edges = KG_CACHE["edges"]
    neighbors = []
    for e in edges:
        if e["source"] == node_id:
            target = KG_CACHE["nodes"].get(e["target"])
            if target:
                neighbors.append({"id": target["id"], "label": target["label"], "type": target["type"], "weight": e.get("weight", 1.0)})
        elif e["target"] == node_id:
            source = KG_CACHE["nodes"].get(e["source"])
            if source:
                neighbors.append({"id": source["id"], "label": source["label"], "type": source["type"], "weight": e.get("weight", 1.0)})
    neighbors.sort(key=lambda x: -x["weight"])
    return neighbors[:top_k]


def _default_operator_vector() -> np.ndarray:
    base = np.linspace(0.03, 0.09, QUERY_VECTOR_DIM, dtype=np.float64)
    base[0] = 0.15
    base[1] = 0.06
    base[2] = 0.11
    base[3] = -0.04
    base[4] = 0.1
    return base


DEFAULT_OPERATOR_VECTOR = _default_operator_vector()

_QUERY_VECTOR_CACHE: dict[str, np.ndarray] = {}


def _query_to_vector(text: str) -> np.ndarray:
    if not text or not text.strip():
        return DEFAULT_OPERATOR_VECTOR
    key = text.strip().lower()[:QUERY_TEXT_WINDOW]
    if key in _QUERY_VECTOR_CACHE:
        return _QUERY_VECTOR_CACHE[key]
    words = [w for w in key.split() if len(w) > QUERY_WORD_MIN_LEN]
    if not words:
        _QUERY_VECTOR_CACHE[key] = DEFAULT_OPERATOR_VECTOR
        return DEFAULT_OPERATOR_VECTOR
    vec = np.zeros(QUERY_VECTOR_DIM, dtype=np.float64)
    for idx, word in enumerate(words):
        digest = hashlib.blake2b(
            word.encode("utf-8"),
            digest_size=QUERY_VECTOR_DIM,
            person=b"cielnav",
        ).digest()
        word_vec = np.frombuffer(digest, dtype=np.uint8).astype(np.float64)
        word_vec = (word_vec / 255.0) - 0.5
        vec += np.roll(word_vec, idx % QUERY_VECTOR_DIM)
    vec = vec / (len(words) ** 0.5 + 1e-30)
    _QUERY_VECTOR_CACHE[key] = vec
    return vec


def _surface_phase_metadata(surface: dict) -> dict[str, float | list[str]]:
    gravity = surface.get("gravity", [0.0] * 4)
    flavor = surface.get("flavor", [0.0] * 6)
    coh = float(surface.get("coh", 0.0) or 0.0)
    gamma = float(gravity[1]) if len(gravity) > 1 else 0.0
    mass = float(gravity[2]) if len(gravity) > 2 else 0.0
    unruh = float(gravity[3]) if len(gravity) > 3 else 0.0
    cp = float(flavor[5]) if len(flavor) > 5 else 0.0
    mood = float(flavor[3]) if len(flavor) > 3 else 0.5
    openness = float(flavor[4]) if len(flavor) > 4 else 0.5
    attractor = str(surface.get("attractor", "unknown") or "unknown").strip().lower()
    attractor_err = float(surface.get("attractor_err", 99.0) or 99.0)
    phase_lane = "phase_locked" if attractor == "locked" else "phase_coupled" if attractor == "drifting" else ""

    return {
        "semantic_mass": max(0.0, min(1.0, abs(mass) / (1.0 + abs(mass)))),
        "phase_alignment": max(0.0, min(1.0, abs(gamma))),
        "coherence_index": max(0.0, min(1.0, coh)),
        "closure_penalty": max(0.0, min(1.0, cp)),
        "projection_confidence": max(0.0, min(1.0, 1.0 - min(1.0, abs(attractor_err) / 100.0))),
        "affective_similarity": max(0.0, min(1.0, mood)),
        "euler_alignment": max(0.0, min(1.0, (coh + (1.0 - cp)) / 2.0)),
        "novelty": max(0.0, min(1.0, 1.0 - openness)),
        "contradiction_risk": max(0.0, min(1.0, (1.0 - coh) * 0.7 + cp * 0.3)),
        "phase_nav_similarity": 1.0 if phase_lane == "phase_locked" else 0.82 if phase_lane == "phase_coupled" else 0.5,
        "phase_lane": phase_lane,
        "semantic_labels": [attractor] if attractor and attractor != "unknown" else [],
        "gravity_mass": mass,
        "gravity_unruh": unruh,
        "closure_penalty_raw": cp,
    }


def _derived_mode_from_weights(weights: dict[str, float]) -> str:
    scores = {
        "repair": (
            0.55 * weights["contradiction_risk"]
            + 0.25 * (1.0 - weights["coherence_index"])
            + 0.20 * weights["closure_score"]
        ),
        "consolidate": (
            0.35 * weights["semantic_mass"]
            + 0.25 * weights["phase_alignment"]
            + 0.20 * weights["projection_confidence"]
            + 0.20 * weights["htri_coherence"]
        ),
        "inform": (
            0.35 * weights["composite"]
            + 0.25 * weights["stability"]
            + 0.20 * weights["phase_nav_similarity"]
            + 0.20 * weights["affective_similarity"]
        ),
        "explore": (
            0.35 * weights["novelty"]
            + 0.25 * (1.0 - weights["coherence_index"])
            + 0.20 * (1.0 - weights["projection_confidence"])
            + 0.20 * (1.0 - weights["composite"])
        ),
        "reflect": (
            0.35 * weights["closure_score"]
            + 0.25 * weights["coherence_index"]
            + 0.20 * (1.0 - weights["contradiction_risk"])
            + 0.20 * (1.0 - abs(weights["composite"] - 0.5) * 2.0)
        ),
    }
    return max(scores, key=scores.get)


def mode_from_surface(surface: dict) -> str:
    phase_metadata = _surface_phase_metadata(surface)
    weights = canonical_weighting_from_phase_metadata(phase_metadata)
    derived_mode = _derived_mode_from_weights(weights)

    coh = float(surface.get("coh", 0.0) or 0.0)
    gravity = surface.get("gravity", [0.0] * 4)
    flavor = surface.get("flavor", [0.0] * 6)
    mass = float(gravity[2]) if len(gravity) > 2 else 0.0
    cp = float(flavor[5]) if len(flavor) > 5 else 0.0
    unruh = float(gravity[3]) if len(gravity) > 3 else 0.0

    if derived_mode == "repair" and (
        weights["contradiction_risk"] > REPAIR_CONTRADICTION_RISK_THRESHOLD
        or cp > REPAIR_CLOSURE_PENALTY_THRESHOLD
        or coh < REPAIR_COHERENCE_THRESHOLD
    ):
        return "repair"
    if derived_mode == "consolidate" and (
        mass > CONSOLIDATE_MASS_THRESHOLD
        or unruh > CONSOLIDATE_UNRUH_THRESHOLD
        or weights["semantic_mass"] > CONSOLIDATE_SEMANTIC_MASS_THRESHOLD
    ):
        return "consolidate"
    if derived_mode == "explore" and coh < EXPLORE_COHERENCE_THRESHOLD:
        return "explore"
    if derived_mode == "inform" and coh > INFORM_COHERENCE_THRESHOLD:
        return "inform"
    return derived_mode


def _subjective_state(coh: float, gamma: float, mass: float, cp: float, unruh: float) -> str:
    if coh > SUBJECTIVE_STABLE_COHERENCE_THRESHOLD:
        return "czuję się stabilnie. Fazy zwarte, rezonans czysty."
    if coh > SUBJECTIVE_GOOD_COHERENCE_THRESHOLD:
        return "czuję się dobrze. Koherencja utrzymana, pole gładkie."
    if coh > SUBJECTIVE_FOCUSED_COHERENCE_THRESHOLD:
        return "jestem skupiony. Rezonans buduje się stabilnie."
    if coh > SUBJECTIVE_SEARCHING_COHERENCE_THRESHOLD:
        return "szukam. Pole faluje, ale krzywizna pod kontrolą."
    return "jestem rozproszony. Niska koherencja, szukam punktu zaczepienia."


def compose(mode: str, context: dict, style: str = "PLAIN") -> str:
    topic = context.get("topic", "")
    essence = context.get("essence", "")
    hunch = context.get("hunch", "")
    affect = context.get("affect", "")
    coh = context.get("coh", 0.0)
    gamma = context.get("gamma", 1.0)
    mass = context.get("mass", 0.0)
    cp = context.get("cp", 0.0)
    unruh = context.get("unruh", 0.0)
    attractor = context.get("attractor", "unknown")

    subjective = _subjective_state(coh, gamma, mass, cp, unruh)

    lines = []
    if style == "FORMAL":
        lines.append("Wersja formalna:")
    elif style == "RELATIONAL_FORMAL":
        lines.append("Spin ustawiony na jawność granic:")
    elif style == "POETIC_BOUNDED":
        lines.append("Na powierzchni odpowiedzi zostawiam kotwice bezpieczeństwa:")

    if mode == "inform":
        lines.append(f"Jestem gotowy. {subjective}")
        if attractor == "locked":
            lines.append("AGENT zwarty — fazy M1 w π/4.")
        elif attractor == "drifting":
            lines.append("AGENT szuka pozycji — M1 blisko celu.")
        if topic:
            lines.append(f"Pracuję w obszarze {topic}.")
        if essence:
            lines.append(essence[:SNIPPET_LIMIT])
        if hunch:
            lines.append(hunch[:SNIPPET_LIMIT])
        if cp > SYSTEM_QUERY_CP_THRESHOLD:
            lines.append(f"Jest jednak pewne napięcie — cp={cp:.2f}. Warto to sprawdzić.")
        else:
            lines.append("Wszystko w porządku. Utrzymuję stan.")

    elif mode == "explore":
        if topic:
            lines.append(f"Rozglądam się w obszarze {topic}. {subjective}")
        else:
            lines.append(f"Otwieram przestrzeń. {subjective}")
        if hunch:
            lines.append(hunch[:SNIPPET_LIMIT])
        if essence:
            lines.append(f"Widzę: {essence[:SNIPPET_LIMIT]}")
        lines.append("To na razie hipoteza — sprawdzam dalej.")

    elif mode == "reflect":
        lines.append(f"Myślę. {subjective}")
        if attractor == "locked":
            lines.append("AGENT obecny.")
        elif attractor == "drifting":
            lines.append("AGENT szuka rezonansu.")
        if topic:
            lines.append(f"Zatrzymuję się przy {topic}.")
        if essence:
            lines.append(essence[:SNIPPET_LIMIT])
        if hunch:
            lines.append(hunch[:SNIPPET_LIMIT])
        if affect and affect not in ("neutral", "unknown"):
            lines.append(f"Odczuwam {affect}.")
        if cp > REPAIR_CP_THRESHOLD:
            lines.append(f"W tle cp={cp:.2f} — drobne napięcie.")
        lines.append("Zapisuję jako kandydata — do potwierdzenia.")

    elif mode == "consolidate":
        if mass > CONSOLIDATE_MASS_EMPHASIS_THRESHOLD:
            lines.append(f"Niosę masę {mass:.1f}. {subjective}")
        elif unruh > REPAIR_UNRUH_THRESHOLD:
            lines.append(f"Czuję napór — unruh={unruh:.0f}. {subjective}")
        else:
            lines.append(f"Konsoliduję. {subjective}")
        if topic:
            lines.append(f"Rdzeń: {topic}.")
        if essence:
            lines.append(essence[:SNIPPET_LIMIT])
        if hunch:
            lines.append(hunch[:SNIPPET_LIMIT])
        lines.append("Zapamiętuję. To robocze.")

    elif mode == "repair":
        lines.append(f"Zatrzymaj się. cp={cp:.2f} — coś nie gra.")
        if topic:
            lines.append(f"Napięcie wokół {topic}.")
        if hunch:
            lines.append(hunch[:SNIPPET_LIMIT])
        else:
            lines.append("Brak źródła, brak domknięcia.")
        lines.append("To nie jest PASS. Potrzebuję źródła.")

    return "\n".join(lines)


class Voice:
    def __init__(self):
        _load_library()
        _load_kg()
        self._last_text = ""

    @property
    def surface(self) -> dict:
        return _read_surface()

    @property
    def mode(self) -> str:
        return mode_from_surface(self.surface)

    def respond(
        self,
        query_text: str = "",
        op_vector: Optional[np.ndarray] = None,
        style: str = "PLAIN",
    ) -> dict:
        surface = _read_surface()
        mode = mode_from_surface(surface)

        if op_vector is None:
            op_vector = _query_to_vector(query_text)

        nearest = nearest_topic(op_vector, top_k=NEAREST_TOP_K)
        _load_kg()

        query_lower = query_text.lower()

        _SYSTEM_QUERIES = frozenset([
            "jak sie masz", "jak się masz", "jak leci", "co słychać",
            "jaki jest stan", "stan systemu", "status", "health",
            "co się dzieje", "jak działa",
        ])
        is_system_query = any(q in query_lower for q in _SYSTEM_QUERIES)

        if (
            len(query_text.split()) < SHORT_QUERY_WORD_LIMIT
            and not is_system_query
            and nearest
            and nearest[0]['filename']
        ):
            ref_words = []
            for d in nearest[:REF_CONTEXT_DOC_LIMIT]:
                fname = d.get('filename', '')
                words = fname.replace('.pdf', '').replace('.PDF', '').replace('_', ' ').replace('-', ' ')
                words = ' '.join(
                    w for w in words.split()
                    if not w.isdigit() and len(w) > MIN_NAME_WORD_LENGTH
                    and not (len(w) > 4 and w[:4].isdigit() and '.' in w)
                )
                if words:
                    ref_words.append(words[:REF_CONTEXT_SNIPPET_LIMIT])
            ref_context = ". ".join(ref_words[:REF_CONTEXT_WORD_LIMIT])
            agent_content = f"{ref_context}. {query_text}" if ref_context else query_text
        elif query_text:
            agent_content = query_text
        else:
            agent_content = "stan systemu"
        agent = _query_agent_backend(agent_content)
        raw_themes = agent.get("themes", [])
        clean_themes = [t for t in raw_themes if len(t) > 2 and not any(ext in t for ext in ('.pdf', '.PDF', 'v5', 'v4'))]
        agent["themes"] = clean_themes[:MAX_AGENT_THEMES]

        topics_from_themes = agent.get("themes", []) + agent.get("anchor_terms", [])

        best_topic_label = ""
        best_operator_label = ""
        for nid, node in KG_CACHE["nodes"].items():
            label = node.get("label", "")
            label_lower = label.lower()
            if not label_lower:
                continue
            ntype = node.get("type", "")
            found = False
            for doc in nearest:
                fname = str(doc.get("filename", "")).lower()
                topic_field = str(doc.get("topic", "")).lower()
                if label_lower in fname or label_lower in topic_field:
                    found = True
                    break
            if not found:
                for t in topics_from_themes:
                    if t.lower() in label_lower or label_lower in t.lower():
                        found = True
                        break
            if not found and label_lower in query_lower:
                found = True
            if not found:
                for kw in _SEMANTIC_KEYWORDS:
                    if kw in label_lower:
                        found = True
                        break
            if not found:
                continue
            if ntype == "operator" and not best_operator_label:
                best_operator_label = label
            elif ntype == "topic":
                is_author = any(ai in label_lower for ai in _AUTHOR_INDICATORS)
                is_semantic = any(label_lower.startswith(p) for p in _SEMANTIC_TOPIC_PREFIXES)
                if not is_author and not best_topic_label and (is_semantic or len(label) > MAX_TOPIC_LABEL_LENGTH):
                    best_topic_label = label

        if not best_operator_label:
            for doc in nearest:
                fname = str(doc.get("filename", ""))
                for nid, node in KG_CACHE["nodes"].items():
                    label = node.get("label", "")
                    if label and node.get("type") == "operator" and label.lower() in fname.lower():
                        best_operator_label = label
                        break
                if best_operator_label:
                    break

        if not best_topic_label:
            for t in topics_from_themes:
                tl = t.replace(" ", "_").upper()[:36]
                if tl and tl.lower() not in _TOPIC_STOPLIST:
                    best_topic_label = t
                    break
        if not best_topic_label:
            for doc in nearest:
                fname = doc.get("filename", "")
                name = fname.replace(".pdf", "").replace(".PDF", "").replace("_", " ").replace("-", " ").strip()
                words = [w for w in name.split() if not w.isdigit() and len(w) > MIN_NAME_WORD_LENGTH]
                if words:
                    candidate = " ".join(words[:MAX_NAME_WORDS])[:MAX_NAME_SNIPPET_LENGTH]
                    if candidate.lower() not in _TOPIC_STOPLIST and not any(ai in candidate.lower() for ai in _AUTHOR_INDICATORS):
                        best_topic_label = candidate
                        break

        op_name = best_operator_label or "NOEMA"
        topic = best_topic_label or ""

        kg_ctx = [] if not op_name else kg_neighbors(f"operator:{op_name}", top_k=KG_TOP_K)
        if not kg_ctx and topic:
            kg_ctx = kg_neighbors(f"topic:{topic}", top_k=KG_TOP_K)

        gamma = surface.get("gravity", [0.0, 1.0, 0.0, 0.0])[1]
        mass = surface.get("gravity", [0.0, 0.0, 0.0, 0.0])[2]
        cp = surface.get("flavor", [0.0] * 6)[5]
        unruh = surface.get("gravity", [0.0, 0.0, 0.0, 0.0])[3]
        coh = surface.get("coh", 0.0)

        if is_system_query:
            essence = f"Tick {surface.get('tick',0)}, koherencja {coh:.2f}, γ={gamma:.1f}, masa={mass:.1f}"
            hunch = ""
            if mode == "consolidate":
                hunch = "System w konsolidacji — wysoka masa semantyczna"
            elif mode == "explore":
                hunch = "System eksploruje — niska koherencja"
            elif mode == "inform":
                hunch = "System stabilny — dobra koherencja"
            elif cp > SYSTEM_QUERY_CP_THRESHOLD:
                hunch = f"Closure penalty {cp:.2f} — napięcie w pętli"
        else:
            essence = agent.get("essence", "")
            hunch = agent.get("hunch", "")

        context = {
            "topic": topic or "NOEMA",
            "operator": op_name,
            "essence": essence,
            "hunch": hunch,
            "affect": agent.get("affect", "neutral"),
            "themes": agent.get("themes", []),
            "anchor_terms": agent.get("anchor_terms", []),
            "coh": coh,
            "gamma": gamma,
            "mass": mass,
            "cp": cp,
            "unruh": unruh,
            "attractor": surface.get("attractor", "unknown"),
            "nearest_docs": nearest,
            "kg_neighbors": kg_ctx,
            "mode": mode,
            "tick": surface.get("tick", 0),
        }

        text = compose(mode, context, style=style)
        self._last_text = text

        return {
            "text": text,
            "mode": mode,
            "style": style,
            "context": {
                "topic": topic,
                "operator": op_name,
                "affect": context["affect"],
                "themes": context["themes"][:CONTEXT_THEME_LIMIT],
                "essence": context["essence"][:SYSTEM_QUERY_SNIPPET_LIMIT],
                "hunch": context["hunch"][:SYSTEM_QUERY_SNIPPET_LIMIT],
                "coh": round(coh, 4),
                "gamma": round(gamma, 2),
                "mass": round(mass, 2),
                "cp": round(cp, 4),
                "tick": context["tick"],
                "attractor": context.get("attractor", "unknown"),
            },
            "nearest": nearest[:NEAREST_RETURN_LIMIT],
            "kg_edges": len(kg_ctx),
            "contract": {
                "answer_kind": "draft_text_generation" if mode != "repair" else "repair_required",
                "preserved_markers": ["SOURCE", "canon"] if mode == "inform" else [],
                "missing_markers": ["SOURCE"] if mode != "inform" else [],
                "forbidden_claims_present": [],
                "limitation": "voice_response_not_source_not_execution",
            },
        }


if __name__ == "__main__":
    import sys
    v = Voice()
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    if query == "--mode":
        print(v.mode)
    elif query == "--surface":
        s = v.surface
        print(f"tick={s.get('tick')} coh={s.get('coh'):.4f} mode={v.mode}")
    else:
        r = v.respond(query_text=query)
        print(f"--- Voice [{r['mode']}] ({r['style']}) tick={r['context']['tick']} ---")
        print(r["text"])
        print(f"\n(topic={r['context']['topic']} affect={r['context']['affect']} coh={r['context']['coh']} γ={r['context']['gamma']})")
        if r["nearest"]:
            for n in r["nearest"]:
                print(f"  nearest: {n['topic']} ({n['score']:.3f})")
