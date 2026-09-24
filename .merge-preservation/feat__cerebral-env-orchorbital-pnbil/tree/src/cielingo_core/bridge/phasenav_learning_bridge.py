"""PhaseNav Learning Bridge — CIELingo uczy się przez PhaseNav + CIELingo LNS.

Łączy PhaseNav solver z CIELingo LNS pełną semantyką.
UŻYWA rzeczywistych modułów CIELingo:
  operator_algebra, grammar_math, case_gauge, tame, predicate_valency,
  concept_card, operator_card, card_ontology, diagnostic_geometry,
  noema_router, scope_quantifier, dynamic_deixis, ontological_aspect,
  + cielingo_core wrappery (lingophysics, semantic_neural, language_spaces, meaning)
"""

from __future__ import annotations

import hashlib
import json
import logging
import sqlite3
import sys
import time
from pathlib import Path
from typing import Any

_log = logging.getLogger(__name__)

import numpy as np

from cielingo_core.persistence.state_engine import CIELingoStateEngine
from ciel_geometry.phasenav.enrichment import phasenav_enrich
from ciel_geometry.phasenav.solver import PhaseNavSolver, PhaseNavTrace

# ─── Ścieżki ──────────────────────────────────────────────────────────────

NOEMA_ROOT = Path("/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA")
MEMORY_ROOT = Path("/media/adrian/New Volume/CIEL_memories")
LIBRARY_ROOT = Path("/media/adrian/New Volume/NOEMA_LIBRARY")
LNS_ROOT = Path("/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/src/ciel_lingophysics_lns_repo_v2_3")

CIELINGO_CARDS_CANON = NOEMA_ROOT / "cards" / "cielingo_cards.jsonl"
CIELINGO_CARDS_LIB = LIBRARY_ROOT / "CARDS" / "cielingo_cards.jsonl"
CIELINGO_CARDS_DIR = LIBRARY_ROOT / "data" / "cielingo" / "cards"

KNOWLEDGE_DB = MEMORY_ROOT / "state" / "noema_knowledge.db"
MEMORIES_DB = MEMORY_ROOT / "memories_index.db"

PHASENAV_INDEX = LIBRARY_ROOT / "INDEX" / "phasenav_index.npy"
PHASENAV_META = LIBRARY_ROOT / "INDEX" / "phasenav_meta.jsonl"

# ─── LNS data paths ───────────────────────────────────────────────────────

LNS_CASE_GAUGE = LNS_ROOT / "data" / "case_systems" / "slavic_case_gauge.yaml"
LNS_TAME_SYSTEM = LNS_ROOT / "data" / "tame" / "tame_operator_system.yaml"
LNS_EVENT_FRAMES = LNS_ROOT / "data" / "event_frames" / "predicate_valency_frames.yaml"
LNS_ONTOLOGICAL = LNS_ROOT / "data" / "ontological_aspect" / "koto_mono_ser_estar.yaml"
LNS_DEIXIS = LNS_ROOT / "data" / "operator_cards" / "dynamic_deictic_operators_5lang.yaml"
LNS_SCOPE = LNS_ROOT / "data" / "scope" / "scope_quantifier_negation.yaml"
LNS_OP_ALGEBRA = LNS_ROOT / "data" / "operator_algebra" / "operator_algebra_index.yaml"
LNS_CARD_ONTOLOGY = LNS_ROOT / "data" / "card_ontology" / "card_ontology_v1_7.yaml"
LNS_GRAMMAR_EN = LNS_ROOT / "data" / "grammar" / "en_grammar_math.yaml"
LNS_GRAMMAR_PL = LNS_ROOT / "data" / "grammar" / "pl_grammar_math.yaml"
LNS_RECON_COSTS = LNS_ROOT / "data" / "diagnostics" / "cross_language_reconstruction_costs.json"
LNS_CONFLICT_REG = LNS_ROOT / "data" / "diagnostics" / "conflict_ambiguity_unresolved_registry.json"
LNS_NOEMA_INDEX = LNS_ROOT / "data" / "noema" / "noema_index_seed_v2_2.yaml"
LNS_ROUTING_POLICY = LNS_ROOT / "data" / "noema" / "routing_policy_v2_2.yaml"

_LINGO_ROOT_SUBPATH = Path("src")


def _ensure_lingophysics_on_path() -> bool:
    """Dodaje katalog ze źródłami lingophysics do sys.path."""
    lingo_src = (LNS_ROOT / _LINGO_ROOT_SUBPATH).resolve()
    if lingo_src.exists():
        lingo_str = str(lingo_src)
        if lingo_str not in sys.path:
            sys.path.insert(0, lingo_str)
        return True
    return False


# ─── Pomocnicze ───────────────────────────────────────────────────────────


def _connect(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), timeout=5)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    return conn


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    data = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return data


def _append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def _now() -> float:
    return time.time()


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:12]


def _load_yaml(path: Path) -> dict:
    try:
        import yaml
        with open(str(path), encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}


def _load_json(path: Path) -> dict | list:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _detect_language(text: str) -> str:
    """Prosta heurystyka — PL vs EN vs other."""
    pl_chars = "ąćęłńóśźż"
    en_score = sum(1 for c in text if c.isascii() and c.isalpha())
    pl_score = sum(1 for c in text if c.lower() in pl_chars)
    if pl_score > 0:
        return "pl"
    pl_words = {"i", "w", "na", "z", "do", "się", "nie", "to", "jest", "że", "ma", "jak", "tak", "co", "ale", "po", "od", "przez", "dla", "czy", "ich"}
    words = set(text.lower().split())
    if words & pl_words:
        return "pl"
    return "en"


# ═══ CIELingo Subsystems ═════════════════════════════════════════════════


class CIELingoSubsystems:
    """Lazy-loaded CIELingo LNS subsystems. Każdy subsystem ładuje się przy pierwszym użyciu."""

    def __init__(self, debug: bool = False):
        self._debug = debug
        self._log: list[str] = []
        _ensure_lingophysics_on_path()

        # operator_algebra
        self._operator_algebra_loaded = False
        self._operator_algebra_index: dict = {}
        self._classify_library_item = None
        self._compose_dual = None
        self._operator_power = None
        self._euler_phase_error = None
        self._validate_composition = None

        # grammar_math
        self._grammar_math_loaded = False
        self._euclidean_distance = None
        self._grammar_curvature_seed = None
        self._cross_language_compatible = None
        self._grammar_profiles: dict[str, list[float]] = {}

        # case_gauge
        self._case_gauge_loaded = False
        self._case_gauge: dict = {}
        self._map_polish_case = None
        self._decode_case_role = None
        self._reconstruction_cost = None

        # tame
        self._tame_loaded = False
        self._tame_system: dict = {}
        self._encode_tame = None
        self._phase_distance = None
        self._compatible_tame = None

        # predicate_valency
        self._valency_loaded = False
        self._event_frames: dict = {}
        self._validate_roles = None
        self._get_frame = None
        self._required_roles = None

        # concept_card / operator_card / card_ontology
        self._card_models_loaded = False
        self._card_ontology_specs: dict = {}
        self._infer_card_type = None
        self._validate_payload_shape = None
        self._ConceptCard = None
        self._OperatorCard = None
        self._classify_word_card = None

        # diagnostic_geometry
        self._diagnostic_loaded = False
        self._recon_costs: list[dict] = []
        self._conflict_registry: dict = {}
        self._max_cost_val = 0.0

        # noema_router
        self._router_loaded = False
        self._noema_index: dict = {}
        self._routing_policy: dict = {}
        self._route_query = None
        self._detect_unresolved = None

        # scope_quantifier
        self._scope_loaded = False
        self._scope_system: dict = {}
        self._normalize_scope = None
        self._encode_quantifier = None

        # dynamic_deixis
        self._deixis_loaded = False
        self._deixis_data: dict = {}
        self._classify_dynamic_surface = None
        self._resolve_dynamic_anchor = None

        # ontological_aspect
        self._ontological_loaded = False
        self._ontological_data: dict = {}
        self._classify_ontological = None
        self._resolve_be = None

        # semantic_neural (cielingo wrapper)
        self._semantic_loaded = False
        self._semantic_encoder = None
        self._semantic_collatz = None

        # language_spaces (cielingo wrapper)
        self._lang_spaces_loaded = False
        self._LNSLanguageCard = None
        self._load_all_language_cards = None
        self._PolishLinguisticDatabase = None

    def _log_msg(self, msg: str) -> None:
        if self._debug:
            print(f"[CIELingoSubsystems] {msg}")
        self._log.append(msg)

    # ── operator_algebra ────────────────────────────────────────────────

    def load_operator_algebra(self) -> bool:
        if self._operator_algebra_loaded:
            return True
        try:
            from lingophysics.operator_algebra import (
                classify_library_item, compose_dual, operator_power,
                euler_phase_error, validate_composition,
            )
            self._classify_library_item = classify_library_item
            self._compose_dual = compose_dual
            self._operator_power = operator_power
            self._euler_phase_error = euler_phase_error
            self._validate_composition = validate_composition
            self._operator_algebra_index = _load_yaml(LNS_OP_ALGEBRA)
            self._operator_algebra_loaded = True
            self._log_msg(f"operator_algebra loaded: {len(self._operator_algebra_index.get('families', []))} families, module functions ready")
            return True
        except Exception as ex:
            self._log_msg(f"operator_algebra FAILED: {ex}")
            return False

    def classify_operator(self, text: str) -> dict[str, Any]:
        if not self.load_operator_algebra():
            return {"operator": "unknown", "domain": "unknown", "power": 1}
        words = text.lower().split()
        semantic_roles = {
            "give": "transfer", "take": "transfer", "make": "creation",
            "break": "destruction", "see": "perception", "hear": "perception",
            "think": "cognition", "feel": "affect", "say": "communication",
            "want": "desire", "know": "knowledge", "have": "possession",
            "be": "identity", "do": "action", "go": "motion", "come": "motion",
            "daj": "transfer", "dawać": "transfer", "dać": "transfer",
            "dawał": "transfer", "dali": "transfer", "daje": "transfer",
            "zrobić": "creation", "robić": "creation", "zrób": "creation",
            "stworzyć": "creation", "tworzyć": "creation",
            "złamać": "destruction", "zniszczyć": "destruction", "niszczyć": "destruction",
            "widzieć": "perception", "zobaczyć": "perception", "patrzeć": "perception",
            "słyszeć": "perception", "usłyszeć": "perception",
            "myśleć": "cognition", "pomyśleć": "cognition", "wiedzieć": "knowledge",
            "mówić": "communication", "powiedzieć": "communication",
            "chcieć": "desire", "chce": "desire", "pragnąć": "desire",
            "mieć": "possession", "ma": "possession", "mam": "possession",
            "być": "identity", "jest": "identity", "są": "identity",
            "iść": "motion", "pójść": "motion", "przyjść": "motion",
        }
        for word in words:
            if word in semantic_roles:
                return {"operator": word, "domain": semantic_roles[word],
                        "kind": "operator", "power": 1, "dual": "", "inferred": True}
        return {"operator": "unknown", "domain": "unknown", "kind": "unknown", "power": 0}

    def compose_operator(self, expr: str) -> str:
        if not self.load_operator_algebra():
            return expr
        return self._compose_dual(expr)

    def operator_power_of(self, op: str, n: int) -> Any:
        if not self.load_operator_algebra():
            return op
        return self._operator_power(op, n)

    # ── grammar_math ────────────────────────────────────────────────────

    def load_grammar_math(self) -> bool:
        if self._grammar_math_loaded:
            return True
        try:
            from lingophysics.grammar_math import (
                euclidean_distance, grammar_curvature_seed, cross_language_compatible,
            )
            self._euclidean_distance = euclidean_distance
            self._grammar_curvature_seed = grammar_curvature_seed
            self._cross_language_compatible = cross_language_compatible
            for lang_code, path in [("en", LNS_GRAMMAR_EN), ("pl", LNS_GRAMMAR_PL)]:
                if path.exists():
                    profile = _load_yaml(path)
                    gauge = profile.get("grammar_as_gauge", {})
                    vec = gauge.get("local_vector", [])
                    self._grammar_profiles[lang_code] = [float(v) for v in vec if isinstance(v, (int, float))]
            self._grammar_math_loaded = True
            self._log_msg(f"grammar_math loaded: {len(self._grammar_profiles)} language profiles")
            return True
        except Exception as ex:
            self._log_msg(f"grammar_math FAILED: {ex}")
            return False

    def grammar_curvature(self, vector: list[float]) -> float:
        if not self.load_grammar_math():
            return 0.0
        return self._grammar_curvature_seed(vector)

    def semantic_distance(self, a: list[float], b: list[float]) -> float:
        if not self.load_grammar_math():
            return 1.0
        return self._euclidean_distance(a, b)

    def language_compatible(self, dist: float, eps: float = 0.75) -> bool:
        if not self.load_grammar_math():
            return True
        return self._cross_language_compatible(dist, eps)

    # ── case_gauge ──────────────────────────────────────────────────────

    def load_case_gauge(self) -> bool:
        if self._case_gauge_loaded:
            return True
        try:
            from lingophysics.case_gauge import (
                map_polish_case_to_language, decode_case_role, reconstruction_cost,
            )
            self._map_polish_case = map_polish_case_to_language
            self._decode_case_role = decode_case_role
            self._reconstruction_cost = reconstruction_cost
            self._case_gauge = _load_yaml(LNS_CASE_GAUGE)
            self._case_gauge_loaded = True
            n_cases = len(self._case_gauge.get("case_roles", []))
            self._log_msg(f"case_gauge loaded: {n_cases} PL cases")
            return True
        except Exception as ex:
            self._log_msg(f"case_gauge FAILED: {ex}")
            return False

    def analyze_case(self, text: str, target_lang: str = "en") -> list[dict]:
        if not self.load_case_gauge():
            return []
        lang = _detect_language(text)
        if lang != "pl":
            return [{"language": lang, "note": "non-PL text, case gauge skipped"}]
        gauge = self._case_gauge
        case_roles = gauge.get("case_roles", [])
        results = []
        words = text.lower().split()
        # Heuristic: common Polish case endings for nouns/adjectives
        # These are rough patterns, not a full morphological analyser.
        case_endings: list[tuple[str, list[str]]] = [
            ("Nom", ["a", "i", "y", "e", "o", "um", "us"]),
            ("Gen", ["y", "i", "ów", "ek", "a"]),
            ("Dat", ["owi", "owi", "u", "om"]),
            ("Acc", ["ę", "a", "ą"]),
            ("Ins", ["ą", "em", "ami", "ami"]),
            ("Loc", ["ie", "u", "ach"]),
            ("Voc", ["e", "u", "o"]),
        ]
        for word in words:
            matched_case = None
            for case_def in case_roles:
                case_name = case_def.get("ud", "")
                if not case_name:
                    continue
                markers = [case_def.get("pl_name", "").lower()]
                if any(m in word for m in markers):
                    matched_case = case_name
                    break
            if matched_case is None and len(words) > 1:
                for case_name, endings in case_endings:
                    for ending in endings:
                        if word.endswith(ending) and len(word) > len(ending):
                            matched_case = case_name
                            break
                    if matched_case:
                        break
            if matched_case:
                mapping = self._map_polish_case(matched_case, target_lang, gauge)
                role = self._decode_case_role(matched_case)
                cost = self._reconstruction_cost(matched_case, target_lang)
                results.append({
                    "word": word, "case": matched_case, "role": role,
                    "target_mapping": mapping,
                    "reconstruction_cost": cost,
                })
        return results if results else [{"language": lang, "case_analysis": "no PL case markers detected"}]

    # ── TAM-E ───────────────────────────────────────────────────────────

    def load_tame(self) -> bool:
        if self._tame_loaded:
            return True
        try:
            from lingophysics.tame import (
                encode_tame_signature, phase_distance, compatible_tame,
            )
            self._encode_tame = encode_tame_signature
            self._phase_distance = phase_distance
            self._compatible_tame = compatible_tame
            self._tame_system = _load_yaml(LNS_TAME_SYSTEM)
            self._tame_loaded = True
            n_dims = len(self._tame_system.get("dimensions", []))
            self._log_msg(f"TAM-E loaded: {n_dims} dimensions")
            return True
        except Exception as ex:
            self._log_msg(f"TAM-E FAILED: {ex}")
            return False

    _TAME_TENSE_MAP = {"past": "Past", "present": "Present", "future": "Future", "atemporal": "Atemporal"}
    _TAME_ASPECT_MAP = {"simple": "Perfective", "perfective": "Perfective", "imperfective": "Imperfective",
                        "progressive": "Progressive", "habitual": "Habitual", "perfect": "Perfective",
                        "perfect_progressive": "Progressive"}
    _TAME_MOOD_MAP = {"indicative": "Indicative", "imperative": "Imperative", "conditional": "Conditional",
                      "subjunctive": "Subjunctive", "necessity": "Indicative", "interrogative": "Indicative"}
    _TAME_MODALITY_MAP = {"neutral": "Possible", "necessity": "Necessary", "obligation": "Obligatory",
                          "ability": "Possible", "possibility": "Possible", "permission": "Permitted",
                          "prediction": "Possible"}
    _TAME_EV_MAP = {"direct": "Direct", "inferential": "Inferential", "reportative": "Reportative", "unknown": "Unknown"}

    def extract_tame(self, text: str) -> dict[str, Any]:
        if not self.load_tame():
            return {"tense": "unknown", "aspect": "unknown", "mood": "unknown"}
        words = text.lower().split()
        tense = "Present"
        aspect = "Perfective"
        mood = "Indicative"
        modality = "Possible"
        evidentiality = "Direct"

        tense_markers = {"was": "Past", "were": "Past", "will": "Future", "shall": "Future",
                         "był": "Past", "była": "Past", "będzie": "Future"}
        aspect_markers = {s: self._TAME_ASPECT_MAP[s] for s in ("progressive", "perfect", "perfect_progressive")}
        mood_markers = {"would": "Conditional", "could": "Conditional", "should": "Conditional",
                        "might": "Subjunctive", "may": "Subjunctive", "must": "Indicative",
                        "czy": "Indicative", "let": "Imperative", "niech": "Imperative"}
        modality_markers = {"must": "Necessary", "should": "Obligatory", "can": "Possible",
                           "could": "Possible", "may": "Permitted", "might": "Possible",
                           "will": "Possible", "trzeba": "Necessary", "można": "Possible",
                           "musi": "Necessary", "może": "Possible"}

        for w in words:
            if w in tense_markers:
                tense = tense_markers[w]
            if w in aspect_markers:
                aspect = aspect_markers[w]
            if w in mood_markers:
                mood = mood_markers[w]
            if w in modality_markers:
                modality = modality_markers[w]
            if w.endswith("ing") and len(w) > 4:
                aspect = "Progressive"

        sig = self._encode_tame(tense, aspect, mood, evidentiality, self._tame_system, modality) if self._encode_tame else None
        return {
            "tense": tense, "aspect": aspect, "mood": mood,
            "modality": modality, "evidentiality": evidentiality,
            "signature": str(sig) if sig else None,
        }

    # ── predicate_valency ───────────────────────────────────────────────

    def load_valency(self) -> bool:
        if self._valency_loaded:
            return True
        try:
            from lingophysics.predicate_valency import (
                validate_roles, get_frame, required_roles,
            )
            self._validate_roles = validate_roles
            self._get_frame = get_frame
            self._required_roles = required_roles
            self._event_frames = _load_yaml(LNS_EVENT_FRAMES)
            self._valency_loaded = True
            n_frames = len(self._event_frames.get("frames", []))
            self._log_msg(f"valency loaded: {n_frames} event frames")
            return True
        except Exception as ex:
            self._log_msg(f"valency FAILED: {ex}")
            return False

    def analyze_valency(self, text: str) -> dict[str, Any]:
        if not self.load_valency():
            return {"operator": "unknown", "frame": None, "valid": False}
        op_analysis = self.classify_operator(text)
        op_name = op_analysis.get("operator", "unknown")
        if op_name == "unknown":
            return {"operator": "unknown", "frame": None, "valid": False}
        frame = None
        try:
            frame = self._get_frame(op_name, self._event_frames) if self._get_frame else None
        except KeyError:
            pass
        roles_present = set()
        words = text.lower().split()
        for w in words:
            if w in {"to", "go", "do", "make", "have", "give", "take", "see", "say",
                     "want", "know", "think", "feel", "be"}:
                roles_present.add("agent")
            if w in {"at", "to", "from", "in", "on", "with", "by"}:
                roles_present.add("location")
        validation = None
        required = []
        try:
            required = list(self._required_roles(op_name, self._event_frames)) if self._required_roles else []
            validation = self._validate_roles(op_name, roles_present, self._event_frames) if self._validate_roles else None
        except KeyError:
            pass
        return {
            "operator": op_name,
            "domain": op_analysis.get("domain", ""),
            "frame": frame.get("label", "") if frame else None,
            "roles_present": list(roles_present),
            "required": required,
            "valid": validation.valid if validation else False,
            "missing_roles": getattr(validation, "missing_roles", []) if validation else [],
        }

    # ── concept_card / operator_card / card_ontology ────────────────────

    def load_card_models(self) -> bool:
        if self._card_models_loaded:
            return True
        try:
            from lingophysics.concept_card import ConceptCard, LanguageSurface
            from lingophysics.operator_card import OperatorCard, classify_word_card
            from lingophysics.card_ontology import (infer_card_type_from_path,
                                                     validate_payload_shape,
                                                     card_type_specs)
            self._ConceptCard = ConceptCard
            self._OperatorCard = OperatorCard
            self._classify_word_card = classify_word_card
            self._infer_card_type = infer_card_type_from_path
            self._validate_payload_shape = validate_payload_shape
            self._card_ontology_specs = card_type_specs(LNS_ROOT) if LNS_ROOT.exists() else {}
            self._card_models_loaded = True
            self._log_msg(f"card models loaded: {len(self._card_ontology_specs)} ontology specs")
            return True
        except Exception as ex:
            self._log_msg(f"card models FAILED: {ex}")
            return False

    def classify_card_type(self, card_data: dict) -> str:
        if not self.load_card_models():
            return "unresolved"
        card_path = card_data.get("card_id", "unknown")
        return self._infer_card_type(card_path, self._card_ontology_specs)

    def classify_word(self, pos: str, classes: list[str] | None = None) -> str:
        if not self.load_card_models():
            return "unknown"
        return self._classify_word_card(pos, classes)

    # ── diagnostic_geometry ─────────────────────────────────────────────

    def load_diagnostic(self) -> bool:
        if self._diagnostic_loaded:
            return True
        try:
            from lingophysics.diagnostic_geometry import (
                load_reconstruction_costs, load_conflict_registry,
                diagnostic_pass, max_cost,
            )
            self._recon_costs = load_reconstruction_costs(str(LNS_RECON_COSTS)) if LNS_RECON_COSTS.exists() else []
            self._conflict_registry = load_conflict_registry(str(LNS_CONFLICT_REG)) if LNS_CONFLICT_REG.exists() else {}
            self._max_cost_val = max_cost(self._recon_costs) if self._recon_costs else 0.0
            self._diagnostic_pass_fn = diagnostic_pass
            self._diagnostic_loaded = True
            self._log_msg(f"diagnostic loaded: {len(self._recon_costs)} cost entries")
            return True
        except Exception as ex:
            self._log_msg(f"diagnostic FAILED: {ex}")
            return False

    def cross_language_cost(self, source: str, target: str) -> float:
        if not self.load_diagnostic():
            return 1.0
        from lingophysics.diagnostic_geometry import cost_lookup
        return cost_lookup(self._recon_costs, source, target)

    def diagnostic_summary(self) -> dict:
        if not self.load_diagnostic():
            return {"cost_entries": 0, "max_cost": 0.0, "issues": 0}
        from lingophysics.diagnostic_geometry import issue_counts_by_severity
        counts = issue_counts_by_severity(self._conflict_registry)
        return {
            "cost_entries": len(self._recon_costs),
            "max_cost": self._max_cost_val,
            "issues_by_severity": counts,
        }

    # ── noema_router ────────────────────────────────────────────────────

    def load_router(self) -> bool:
        if self._router_loaded:
            return True
        try:
            from lingophysics.noema_router import route_query, detect_unresolved
            self._route_query = route_query
            self._detect_unresolved = detect_unresolved
            self._noema_index = _load_yaml(LNS_NOEMA_INDEX)
            self._routing_policy = _load_yaml(LNS_ROUTING_POLICY)
            self._router_loaded = True
            n_entries = len(self._noema_index.get("cards", []))
            self._log_msg(f"router loaded: {n_entries} index entries")
            return True
        except Exception as ex:
            self._log_msg(f"router FAILED: {ex}")
            return False

    def route_text(self, text: str, language: str | None = None) -> dict:
        if not self.load_router():
            return {"sector": "unresolved", "confidence": 0.0}
        lang = language or _detect_language(text)
        unresolved = self._detect_unresolved(text) if self._detect_unresolved else []
        route = self._route_query(text, self._noema_index, self._routing_policy, lang) if self._route_query else {}
        return {
            "sector": route.get("sector", "unresolved"),
            "confidence": route.get("confidence", 0.0),
            "language": lang,
            "unresolved_terms": unresolved if isinstance(unresolved, list) else [],
            "routing_path": route.get("path", ""),
        }

    # ── scope_quantifier ────────────────────────────────────────────────

    def load_scope(self) -> bool:
        if self._scope_loaded:
            return True
        try:
            from lingophysics.scope_quantifier import normalize_scope, encode_quantifier
            self._normalize_scope = normalize_scope
            self._encode_quantifier = encode_quantifier
            self._scope_system = _load_yaml(LNS_SCOPE)
            self._scope_loaded = True
            self._log_msg("scope/quantifier loaded")
            return True
        except Exception as ex:
            self._log_msg(f"scope FAILED: {ex}")
            return False

    def analyze_scope(self, text: str) -> dict:
        if not self.load_scope():
            return {"quantifiers": [], "negation": False, "scope": None}
        words = text.lower().split()
        quantifiers = []
        negation = False
        for w in words:
            if w in {"all", "every", "each", "some", "any", "no", "none", "many",
                     "few", "most", "several", "każdy", "wszystkie", "niektóre",
                     "żaden", "wiele", "mało", "kilka"}:
                qsig = self._encode_quantifier(w, self._scope_system) if self._encode_quantifier else None
                quantifiers.append({"word": w, "signature": str(qsig) if qsig else "known"})
            if w in {"not", "no", "never", "nothing", "nowhere", "nobody",
                     "nie", "nigdy", "nic", "nikt", "żaden"}:
                negation = True
        scope_expression = None
        if self._normalize_scope and quantifiers:
            qname = quantifiers[0].get("word", "some")
            negation_pos = "inside_predicate" if negation else "outside_quantifier"
            try:
                scope_expression = str(self._normalize_scope(qname, "predicate", negation_pos, self._scope_system))
            except Exception:
                scope_expression = f"{qname}(predicate,neg={negation})"
        return {
            "quantifiers": quantifiers,
            "negation": negation,
            "scope_expression": scope_expression,
        }

    # ── dynamic_deixis ──────────────────────────────────────────────────

    def load_deixis(self) -> bool:
        if self._deixis_loaded:
            return True
        try:
            from lingophysics.dynamic_deixis import (classify_dynamic_surface,
                                                      resolve_dynamic_anchor)
            self._classify_dynamic_surface = classify_dynamic_surface
            self._resolve_dynamic_anchor = resolve_dynamic_anchor
            self._deixis_data = _load_yaml(LNS_DEIXIS)
            self._deixis_loaded = True
            self._log_msg(f"deixis loaded: {len(self._deixis_data.get('cards', []))} operators")
            return True
        except Exception as ex:
            self._log_msg(f"deixis FAILED: {ex}")
            return False

    def analyze_deixis(self, text: str) -> list[dict]:
        if not self.load_deixis():
            return []
        words = text.lower().split()
        results = []
        deictic_markers = {"gdzieś": True, "kiedyś": True, "jakoś": True, "dokądś": True,
                          "skądś": True, "somewhere": True, "sometime": True, "somehow": True,
                          "anywhere": True, "anytime": True, "anyhow": True}
        for w in words:
            if w in deictic_markers:
                cls = self._classify_dynamic_surface(w) if self._classify_dynamic_surface else "indefinite"
                if cls is None:
                    cls = "indefinite"
                anchor = self._resolve_dynamic_anchor(cls) if self._resolve_dynamic_anchor else None
                results.append({
                    "surface": w,
                    "classification": cls,
                    "anchor_variable": str(anchor.variable) if anchor else None,
                    "anchor_constraint": str(anchor.equation) if anchor else None,
                })
        return results

    # ── ontological_aspect ──────────────────────────────────────────────

    def load_ontological(self) -> bool:
        if self._ontological_loaded:
            return True
        try:
            from lingophysics.ontological_aspect import (classify_ontological_surface,
                                                          resolve_be)
            self._classify_ontological = classify_ontological_surface
            self._resolve_be = resolve_be
            self._ontological_data = _load_yaml(LNS_ONTOLOGICAL)
            self._ontological_loaded = True
            self._log_msg(f"ontological aspect loaded")
            return True
        except Exception as ex:
            self._log_msg(f"ontological aspect FAILED: {ex}")
            return False

    def analyze_being(self, text: str) -> dict:
        if not self.load_ontological():
            return {"being_verbs": []}
        lang = _detect_language(text)
        words = text.lower().split()
        results = []
        if lang == "en":
            being_words = {"is": "be", "are": "be", "was": "be", "were": "be",
                          "am": "be", "being": "be", "been": "be"}
        elif lang == "pl":
            being_words = {"jest": "be", "są": "be", "był": "be", "była": "be",
                          "byli": "be", "były": "be", "być": "be", "będzie": "be",
                          "jestem": "be", "jesteś": "be", "jesteśmy": "be",
                          "jesteście": "be", "będę": "be", "będziesz": "be"}
        else:
            being_words = {}
        for w in words:
            if w in being_words:
                cls = self._classify_ontological(w, lang, self._ontological_data) if self._classify_ontological else ""
                results.append({"word": w, "ontological_class": cls})
        return {"being_verbs": results, "language": lang}

    # ── semantic_neural (cielingo wrapper) ──────────────────────────────

    def load_semantic(self) -> bool:
        if self._semantic_loaded:
            return True
        try:
            from cielingo_core.semantic_neural import (
                CIELingoSemanticEncoder, EncoderResult, encode, get_encoder,
                semantic_collatz_route,
            )
            self._CIELingoSemanticEncoder = CIELingoSemanticEncoder
            self._EncoderResult = EncoderResult
            self._encode = encode
            self._get_encoder = get_encoder
            self._semantic_collatz = semantic_collatz_route
            if CIELingoSemanticEncoder is not None:
                self._semantic_encoder = get_encoder() if get_encoder else None
            self._semantic_loaded = True
            self._log_msg("semantic_neural loaded")
            return True
        except Exception as ex:
            self._log_msg(f"semantic_neural FAILED: {ex}")
            return False

    def semantic_encode(self, text: str) -> dict:
        if not self.load_semantic() or self._encode is None:
            return {"encoded": False}
        try:
            result = self._encode(text)
            return {
                "encoded": True,
                "sector": result.sector if hasattr(result, "sector") else "unknown",
                "vector": result.vector.tolist() if hasattr(result, "vector") and result.vector is not None else [],
                "confidence": result.confidence if hasattr(result, "confidence") else 0.0,
            }
        except Exception as ex:
            return {"encoded": False, "error": str(ex)}

    def semantic_route(self, text: str) -> dict:
        if not self.load_semantic() or self._semantic_collatz is None:
            return {"routed": False}
        try:
            route = self._semantic_collatz(text)
            return {
                "routed": True,
                "path": getattr(route, "path", []),
                "summary": getattr(route, "summary", ""),
            }
        except Exception:
            return {"routed": False}

    # ── language_spaces (cielingo wrapper) ──────────────────────────────

    def load_language_spaces(self) -> bool:
        if self._lang_spaces_loaded:
            return True
        try:
            from cielingo_core.language_spaces import (
                LNSLanguageCard, load_all_language_cards,
                PolishLinguisticDatabase, load_polish_database,
            )
            self._LNSLanguageCard = LNSLanguageCard
            self._load_all_language_cards = load_all_language_cards
            self._PolishLinguisticDatabase = PolishLinguisticDatabase
            self._load_polish_database = load_polish_database
            self._lang_spaces_loaded = True
            self._log_msg("language_spaces loaded")
            return True
        except Exception as ex:
            self._log_msg(f"language_spaces FAILED: {ex}")
            return False

    def language_card_search(self, query: str) -> list[dict]:
        if not self.load_language_spaces() or self._load_all_language_cards is None:
            return []
        try:
            cards = self._load_all_language_cards()
            results = []
            q_lower = query.lower()
            for card in (cards or []):
                name = (getattr(card, "name", "") or "").lower()
                if q_lower in name:
                    results.append({"name": getattr(card, "name", ""), "language": getattr(card, "language", "")})
            return results[:5]
        except Exception:
            return []

    # ── FULL CIELINGO PIPELINE ─────────────────────────────────────────

    def enrich_text(self, text: str) -> dict[str, Any]:
        """Pełny pipeline CIELingo LNS: wszystkie subsystemy na jednym tekście."""
        result: dict[str, Any] = {
            "text": text[:128],
            "language": _detect_language(text),
            "operator": self.classify_operator(text),
            "grammar": {},
            "case": [],
            "tame": {},
            "valency": {},
            "card_type": "",
            "router": {},
            "scope": {},
            "deixis": [],
            "ontological": {},
            "semantic": {},
            "subsystem_log": self._log[:],
        }

        # grammar curvature
        self.load_grammar_math()
        gf = self._grammar_profiles.get(result["language"], [])
        if gf and isinstance(gf, list):
            gv = [float(v) for v in gf if isinstance(v, (int, float))]
        else:
            gv = []
        if gv:
            result["grammar"] = {
                "curvature": self.grammar_curvature(gv),
                "profile_language": result["language"],
                "profile_vector": gv,
            }

        # case gauge (PL only)
        if result["language"] == "pl":
            result["case"] = self.analyze_case(text)

        # TAM-E
        result["tame"] = self.extract_tame(text)

        # valency
        result["valency"] = self.analyze_valency(text)

        # card type
        result["card_type"] = self.classify_word(
            result["operator"].get("domain", ""),
            ["operator", "concept", "hybrid"],
        )

        # NOEMA route
        result["router"] = self.route_text(text, result["language"])

        # scope
        result["scope"] = self.analyze_scope(text)

        # deixis
        result["deixis"] = self.analyze_deixis(text)

        # ontological aspect
        result["ontological"] = self.analyze_being(text)

        # semantic encoding
        result["semantic"] = self.semantic_encode(text)

        return result

    def status(self) -> dict[str, Any]:
        """Status wszystkich subsystemów."""
        return {
            "operator_algebra": self._operator_algebra_loaded,
            "grammar_math": self._grammar_math_loaded,
            "grammar_profiles": list(self._grammar_profiles.keys()),
            "case_gauge": self._case_gauge_loaded,
            "tame": self._tame_loaded,
            "valency": self._valency_loaded,
            "card_models": self._card_models_loaded,
            "diagnostic": self._diagnostic_loaded,
            "router": self._router_loaded,
            "scope": self._scope_loaded,
            "deixis": self._deixis_loaded,
            "ontological": self._ontological_loaded,
            "semantic": self._semantic_loaded,
            "language_spaces": self._lang_spaces_loaded,
            "reconstruction_cost_entries": len(self._recon_costs),
            "max_cross_lang_cost": self._max_cost_val,
        }


# ═══ GŁÓWNY BRIDGE ═══════════════════════════════════════════════════════


class PhaseNavLearningBridge:
    """PhaseNav ↔ CIELingo ↔ CIELingo LNS — pełny most semantyczny."""

    def __init__(
        self,
        state: CIELingoStateEngine | None = None,
        solver: PhaseNavSolver | None = None,
        auto_init: bool = True,
        debug: bool = False,
    ):
        self.state = state or CIELingoStateEngine()
        self._solver = solver
        self._last_solver_check = 0.0
        self._debug = debug

        # CIELingo LNS subsystems
        self._cielingo: CIELingoSubsystems | None = None

        self._cards_canon: list[dict] = []
        self._cards_lib: list[dict] = []
        self._cards_dir: list[dict] = []
        self._cards_loaded = False

        self._card_by_id: dict[str, dict] = {}
        self._operator_index: dict[str, list[str]] = {}
        self._ontology_index: dict[str, list[str]] = {}

        self._doc_concepts: list[dict] = []
        self._doc_concepts_loaded = False
        self._doc_operators: dict[str, float] = {}
        self._top_operators: list[tuple[str, float]] = []

        if auto_init:
            self.load_cards()
            self.load_doc_concepts()

    @property
    def ci(self) -> CIELingoSubsystems:
        if self._cielingo is None:
            self._cielingo = CIELingoSubsystems(debug=self._debug)
        return self._cielingo

    # ── PhaseNav solver ─────────────────────────────────────────────────

    @property
    def solver(self) -> PhaseNavSolver | None:
        if self._solver is not None:
            return self._solver
        if time.time() - self._last_solver_check > 30.0:
            self._last_solver_check = time.time()
            try:
                self._solver = PhaseNavSolver.load()
                self._hydrate_solver()
            except Exception as ex:
                if self._debug:
                    print(f"[PNBridge] solver load failed: {ex}")
                self._solver = None
        return self._solver

    def _hydrate_solver(self) -> None:
        if self._solver is None:
            return
        s = self._solver
        if s.data.concept_phases:
            return
        for card_id, card in self._card_by_id.items():
            vec = (
                card.get("phase_vector_36d")
                or card.get("runtime_card", {}).get("phase_vector_36d")
                or np.zeros(36).tolist()
            )
            ops = (
                card.get("operator_bindings")
                or card.get("runtime_card", {}).get("runtime", {}).get("operator_bindings", [])
            )
            mass = (
                card.get("semantic_mass")
                or card.get("runtime_card", {}).get("runtime", {}).get("semantic_mass")
                or 0.25
            )
            s.data.concept_phases[card_id] = {
                "phase": hash(card_id) % 100000 / 100000.0,
                "mass": mass,
                "operators": ops,
                "source": "cielingo_card",
                "card_id": card_id,
                "vector_36d": vec,
            }

    # ── KARTY CIELingo ──────────────────────────────────────────────────

    def load_cards(self, force: bool = False) -> dict[str, int]:
        if self._cards_loaded and not force:
            return self._card_counts()
        self._cards_canon = _load_jsonl(CIELINGO_CARDS_CANON)
        self._cards_lib = _load_jsonl(CIELINGO_CARDS_LIB)
        dir_cards = []
        if CIELINGO_CARDS_DIR.exists():
            for f in sorted(CIELINGO_CARDS_DIR.iterdir()):
                if f.suffix in (".json", ".jsonl"):
                    dir_cards.extend(_load_jsonl(f))
        self._cards_dir = dir_cards
        self._rebuild_index()
        self._cards_loaded = True
        if self._debug:
            print(f"[PNBridge] loaded {len(self._card_by_id)} cards, {len(self._operator_index)} operators")
        return self._card_counts()

    def _rebuild_index(self) -> None:
        self._card_by_id.clear()
        self._operator_index.clear()
        self._ontology_index.clear()
        for card in self._cards_canon + self._cards_lib + self._cards_dir:
            cid = card.get("card_id") or card.get("runtime_card", {}).get("card_id", "")
            if not cid or cid in self._card_by_id:
                continue
            self._card_by_id[cid] = card
            ops = (
                card.get("operator_bindings")
                or card.get("runtime_card", {}).get("runtime", {}).get("operator_bindings", [])
            )
            for op in ops:
                self._operator_index.setdefault(op, []).append(cid)
            ont = card.get("ontology_class") or card.get("runtime_card", {}).get("ontology_class", "unresolved")
            self._ontology_index.setdefault(ont, []).append(cid)

    def _card_counts(self) -> dict[str, int]:
        return {
            "canon": len(self._cards_canon),
            "library_cards": len(self._cards_lib),
            "dir_cards": len(self._cards_dir),
            "total": len(self._card_by_id),
        }

    @property
    def all_cards(self) -> list[dict]:
        self.load_cards()
        return list(self._card_by_id.values())

    def cards_summary(self) -> dict[str, Any]:
        self.load_cards()
        pn = self.solver
        ci_status = self.ci.status()
        return {
            "n_cards_total": len(self._card_by_id),
            "n_cards_canon": len(self._cards_canon),
            "n_cards_library": len(self._cards_lib),
            "n_cards_dir": len(self._cards_dir),
            "unique_operators": len(self._operator_index),
            "top_operators": sorted(
                [(op, len(cids)) for op, cids in self._operator_index.items()],
                key=lambda x: -x[1],
            )[:10],
            "ontology_classes": {ont: len(cids) for ont, cids in sorted(
                self._ontology_index.items(), key=lambda x: -len(x[1])
            )},
            "concepts": len(pn.data.concept_phases) if pn else 0,
            "edges": len(pn.data.edges) if pn else 0,
            "cielingo_subsystems": ci_status,
        }

    # ── DOC_CONCEPTS ────────────────────────────────────────────────────

    def load_doc_concepts(self, force: bool = False) -> dict[str, int]:
        if self._doc_concepts_loaded and not force:
            return {"doc_concepts": len(self._doc_concepts), "unique_operators": len(self._doc_operators)}
        conn = _connect(KNOWLEDGE_DB)
        try:
            rows = conn.execute("SELECT doc_idx, operator_id, score FROM doc_concepts ORDER BY doc_idx").fetchall()
        except sqlite3.OperationalError:
            rows = []
        conn.close()
        self._doc_concepts = [dict(r) for r in rows]
        self._doc_operators.clear()
        for r in rows:
            op = r["operator_id"]
            self._doc_operators[op] = self._doc_operators.get(op, 0.0) + r["score"]
        self._top_operators = sorted(self._doc_operators.items(), key=lambda x: -x[1])[:50]
        self._doc_concepts_loaded = True
        if self._debug:
            print(f"[PNBridge] loaded {len(self._doc_concepts)} doc_concepts, {len(self._doc_operators)} unique ops")
        return {"doc_concepts": len(self._doc_concepts), "unique_operators": len(self._doc_operators)}

    # ── ZAPIS DO KNOWLEDGE.DB ───────────────────────────────────────────

    _PN_TABLES_CREATED = False

    def _ensure_pn_tables(self, conn: sqlite3.Connection) -> None:
        if PhaseNavLearningBridge._PN_TABLES_CREATED:
            return
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS phasenav_entries (
                entry_id TEXT PRIMARY KEY,
                card_id TEXT,
                operator_id TEXT,
                harmonic_fingerprint TEXT,
                semantic_mass REAL,
                source TEXT,
                created_at REAL,
                updated_at REAL
            );
            CREATE TABLE IF NOT EXISTS phasenav_relations (
                relation_id TEXT PRIMARY KEY,
                source_card TEXT,
                target_card TEXT,
                operator_hook TEXT,
                affordance REAL,
                viscosity REAL,
                source TEXT,
                created_at REAL
            );
        """)
        PhaseNavLearningBridge._PN_TABLES_CREATED = True

    def read_phasenav_entries(self, limit: int = 100) -> list[dict]:
        conn = _connect(KNOWLEDGE_DB)
        try:
            rows = conn.execute(
                "SELECT * FROM phasenav_entries ORDER BY created_at DESC LIMIT ?", (limit,)
            ).fetchall()
        except sqlite3.OperationalError:
            rows = []
        conn.close()
        return [dict(r) for r in rows]

    def write_knowledge_entry(self, card_id: str, operator_id: str,
                              fingerprint: str, mass: float, source: str = "phasenav") -> None:
        conn = _connect(KNOWLEDGE_DB)
        self._ensure_pn_tables(conn)
        entry_id = f"pn_{_sha(card_id)}_{_sha(operator_id)}"
        conn.execute(
            """INSERT OR REPLACE INTO phasenav_entries
               (entry_id, card_id, operator_id, harmonic_fingerprint, semantic_mass, source, created_at, updated_at)
               VALUES (?,?,?,?,?,?,?,?)""",
            (entry_id, card_id, operator_id, fingerprint, mass, source, _now(), _now()),
        )
        conn.commit()
        conn.close()

    def write_relation(self, source_card: str, target_card: str, operator_hook: str,
                       affordance: float, viscosity: float, source_tag: str = "phasenav") -> None:
        conn = _connect(KNOWLEDGE_DB)
        self._ensure_pn_tables(conn)
        rid = f"pn_rel_{_sha(source_card + target_card + operator_hook)}"
        conn.execute(
            """INSERT OR REPLACE INTO phasenav_relations
               (relation_id, source_card, target_card, operator_hook, affordance, viscosity, source, created_at)
               VALUES (?,?,?,?,?,?,?,?)""",
            (rid, source_card, target_card, operator_hook, affordance, viscosity, source_tag, _now()),
        )
        conn.commit()
        conn.close()

    # ── ZAPIS DO MEMORIES.DB ────────────────────────────────────────────

    def write_memory_entry(self, entry_type: str, ref: str, data: dict) -> None:
        conn = _connect(MEMORIES_DB)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS phasenav_learning (
                id TEXT PRIMARY KEY,
                entry_type TEXT,
                ref TEXT,
                data_json TEXT,
                created_at REAL
            )
        """)
        eid = f"pn_learn_{_sha(ref + str(_now()))}"
        conn.execute(
            """INSERT OR REPLACE INTO phasenav_learning
               (id, entry_type, ref, data_json, created_at)
               VALUES (?,?,?,?,?)""",
            (eid, entry_type, ref, json.dumps(data, ensure_ascii=False), _now()),
        )
        conn.commit()
        conn.close()

    # ── PHASENAV INDEX NPY ──────────────────────────────────────────────

    def update_phasenav_index(self, card_id: str, operator_vector: list[float]) -> None:
        idx_path = PHASENAV_INDEX
        meta_path = PHASENAV_META
        idx = np.load(str(idx_path)) if idx_path.exists() and idx_path.stat().st_size > 0 else np.zeros((0, 36), dtype=np.complex128)
        meta = _load_jsonl(meta_path)
        vec_36 = np.array(operator_vector[:36], dtype=np.complex128).reshape(1, 36)
        found = False
        for i, m in enumerate(meta):
            if m.get("card_id") == card_id:
                idx[i] = vec_36
                found = True
                break
        if not found:
            idx = np.vstack([idx, vec_36]) if idx.shape[0] else vec_36
            meta.append({"card_id": card_id, "added_at": _now()})
        np.save(str(idx_path), idx)
        _append_jsonl(meta_path, meta[-1] if not found else meta[-1])

    # ── SZUKANIE KART ───────────────────────────────────────────────────

    def find_cards_by_operator(self, operator: str) -> list[str]:
        self.load_cards()
        return self._operator_index.get(operator, [])

    def find_cards_by_ontology(self, ontology: str) -> list[str]:
        self.load_cards()
        return self._ontology_index.get(ontology, [])

    def search_cards(self, query: str, top_k: int = 10) -> list[dict]:
        self.load_cards()
        words = [w.lower() for w in query.split() if len(w) > 1]
        scored: list[tuple[float, str, dict]] = []
        for cid, card in self._card_by_id.items():
            name = (card.get("name") or card.get("lemma") or cid).lower()
            meaning = (card.get("root_meaning") or card.get("function") or "").lower()
            ops = (
                card.get("operator_bindings")
                or card.get("runtime_card", {}).get("runtime", {}).get("operator_bindings", [])
            )
            score = 0.0
            for w in words:
                if w == name or name.startswith(w) or w in name:
                    score += 2.0
                if w in meaning:
                    score += 1.0
                for op in ops:
                    if w in op.lower():
                        score += 0.5
            if score > 0:
                scored.append((score, cid, card))
        scored.sort(key=lambda x: -x[0])
        return [
            {
                "card_id": cid,
                "name": card.get("name") or card.get("lemma") or cid,
                "score": round(s, 2),
                "operators": card.get("operator_bindings") or card.get("runtime_card", {}).get("runtime", {}).get("operator_bindings", []),
                "ontology": card.get("ontology_class") or card.get("runtime_card", {}).get("ontology_class", ""),
            }
            for s, cid, card in scored[:top_k]
        ]

    # ── GŁÓWNE METODY UCZENIA ───────────────────────────────────────────

    def learn_trace(self, trace: PhaseNavTrace, source: str = "phasenav") -> dict:
        if isinstance(trace, str) or not trace:
            return {"learned": False, "reason": "empty_trace" if not trace else trace, "n_steps": 0}
        if not trace.steps:
            return {"learned": False, "reason": "empty_trace", "n_steps": 0}
        operator_chain = [s.operator_hook for s in trace.steps]
        concept_chain = trace.card_sequence

        from cielingo_core.meaning.meaning_loop import LoopState, MeaningLoop, SemanticScar, SemanticScarType

        trace_id = _sha("::".join(concept_chain))
        closure = max(0.0, min(1.0, 1.0 - trace.total_path_integral / max(len(trace.steps), 1e-9)))

        scars = []
        for step in trace.steps:
            if step.holonomic_viscosity > 0.7:
                scars.append(SemanticScar(
                    scar_type=SemanticScarType.COUPLING_RESIDUE,
                    source_ref=f"{step.source_card_id}→{step.target_card_id}",
                    severity=min(1.0, step.holonomic_viscosity),
                    memory_effect="hold",
                    repair_hint=f"PhaseNav visc={step.holonomic_viscosity:.3f} op={step.operator_hook}",
                    scar_id=f"pn_scar_{_sha(str(step.__dict__))}",
                ))

        allow_writeback = closure >= 0.85 and not scars
        loop = MeaningLoop(
            loop_id=f"pn_trace_{trace_id}_{int(_now())}",
            input_ref=" → ".join(concept_chain[:5]),
            response_ref=None,
            loop_state=LoopState.SCARRED if scars else LoopState.CLOSED,
            closure_score=closure,
            contradiction_score=0.0,
            residue_score=0.0,
            return_required=bool(scars),
            scars=scars,
            noema_writeback_allowed=allow_writeback,
        )
        self.state.save_loop(loop.to_dict())

        self.state.log_experience(
            "phasenav_trace_learned", source,
            f"Trace {trace_id}: {len(concept_chain)}c, {len(operator_chain)}op, visc={trace.mean_viscosity:.3f}",
            details=json.dumps({
                "trace_id": trace_id, "card_sequence": concept_chain,
                "operator_chain": operator_chain, "total_path_integral": trace.total_path_integral,
            }),
            salience=0.5 + closure * 0.3,
        )

        for step in trace.steps:
            self.state.write_knowledge_relation(
                step.source_card_id, step.target_card_id,
                f"phasenav_{step.operator_hook}", strength=step.phasenav_affordance,
            )
            self.write_relation(
                step.source_card_id, step.target_card_id,
                step.operator_hook, step.phasenav_affordance, step.holonomic_viscosity,
            )
            self.write_knowledge_entry(
                step.source_card_id, step.operator_hook,
                "trace", step.phasenav_affordance,
            )

        self.write_memory_entry("trace", trace_id, {
            "concept_chain": concept_chain,
            "operator_chain": operator_chain,
            "mean_affordance": trace.mean_affordance,
            "closure": closure,
        })

        return {
            "learned": True, "trace_id": trace_id,
            "n_steps": len(trace.steps), "n_concepts": len(concept_chain),
            "operator_chain": operator_chain, "closure": closure,
            "n_scars": len(scars), "loop_id": loop.loop_id,
        }

    def enrich_and_learn(self, text: str, source: str = "external") -> dict:
        # 1. PhaseNav enrichment (existing harmonic fingerprint)
        try:
            pn = phasenav_enrich(text, name=text[:48])
        except Exception as ex:
            if self._debug:
                print(f"[PNBridge] enrich failed: {ex}")
            pn = {}

        op_id = pn.get("operator_id", "unknown")
        vec_36 = pn.get("operator_vector_24d", [])
        fingerprint = pn.get("harmonic_fingerprint", "?")
        semantic_mass = pn.get("semantic_mass", 0.25)
        card_id = f"pn_learned_{_sha(text)}"

        # 2. CIELingo LNS enrichment (gramatyka, walencja, TAM-E, case, deixis, scope...)
        ci_analysis = self.ci.enrich_text(text)

        # 3. Szukaj kart CIELingo
        self.load_cards()
        matching_cards = self.search_cards(text, top_k=5)
        related = []
        for mc in matching_cards:
            related.append({
                "card_id": mc["card_id"],
                "name": mc["name"],
                "score": mc["score"],
                "operators": mc["operators"],
            })
        for cid in self.find_cards_by_operator(op_id)[:5]:
            if not any(r["card_id"] == cid for r in related):
                related.append({
                    "card_id": cid,
                    "name": self._card_by_id.get(cid, {}).get("name", cid),
                    "score": 0.5,
                    "operator_match": True,
                })

        # 4. Zapisz MeaningLoop z pełnym kontekstem CIELingo
        from cielingo_core.meaning.meaning_loop import LoopState, MeaningLoop
        enrich_closure = min(1.0, semantic_mass * 1.5)
        loop = MeaningLoop(
            loop_id=f"pn_enrich_{_sha(text)}_{int(_now())}",
            input_ref=text[:64],
            response_ref=None,
            loop_state=LoopState.CLOSED,
            closure_score=enrich_closure,
            contradiction_score=0.0,
            residue_score=0.0,
            return_required=False,
            noema_writeback_allowed=enrich_closure >= 0.85,
        )
        self.state.save_loop(loop.to_dict())
        self.state.log_experience(
            "phasenav_enrichment", source,
            f"Enriched op={op_id} fp={fingerprint} mass={semantic_mass:.4f} matched={len(related)} "
            f"cielingo_operator={ci_analysis['operator'].get('operator', '?')} "
            f"tame={ci_analysis['tame'].get('tense', '?')}",
            details=json.dumps({
                "phasenav": {"operator_id": op_id, "fingerprint": fingerprint, "semantic_mass": semantic_mass},
                "cielingo": {
                    "operator": ci_analysis["operator"],
                    "tame": ci_analysis["tame"],
                    "valency": ci_analysis["valency"],
                    "router": ci_analysis["router"],
                    "grammar": ci_analysis["grammar"],
                    "scope": ci_analysis["scope"],
                },
                "matching_cards": related,
            }),
            salience=semantic_mass,
        )

        # 5. Zapisz do wszystkich baz (znaczniki CIELingo w tagach)
        ci_op = ci_analysis["operator"].get("operator", "unknown")
        ci_domain = ci_analysis["operator"].get("domain", "unknown")
        tag = f"{op_id}::{ci_op}::{ci_domain}"
        self.write_knowledge_entry(card_id, tag, fingerprint, semantic_mass, source)
        for rc in related:
            self.state.write_knowledge_relation(card_id, rc["card_id"], f"phasenav_{op_id}", strength=rc["score"])
            self.write_relation(card_id, rc["card_id"], op_id, rc["score"], 0.0)
        self.write_memory_entry("enrichment", card_id, {
            "operator_id": op_id,
            "fingerprint": fingerprint,
            "semantic_mass": semantic_mass,
            "cielingo_analysis": {
                "operator": ci_analysis["operator"],
                "tame": ci_analysis["tame"],
                "valency": ci_analysis["valency"],
                "router_sector": ci_analysis["router"].get("sector", ""),
                "case_results": ci_analysis["case"],
                "deixis": ci_analysis["deixis"],
                "scope": ci_analysis["scope"],
                "grammar_curvature": ci_analysis["grammar"].get("curvature", 0.0),
            },
            "matching_cards": related,
        })
        self.update_phasenav_index(card_id, vec_36)

        # 6. Feedback do LNS modelu (jeśli wystarczająco wysoka pewność)
        if semantic_mass > 0.6:
            lang = ci_analysis.get("language", "en")
            grammar_vec = ci_analysis.get("grammar", {}).get("profile_vector", [])
            if grammar_vec and len(grammar_vec) == 36:
                self.update_grammar_profile(lang, grammar_vec, observation_weight=semantic_mass * 0.15)
            op_name = ci_analysis["operator"].get("operator", "unknown")
            if op_name != "unknown":
                self.update_operator_weights(op_name, delta=semantic_mass * 0.05)
                self.state.increment_metric("model_update_count")

        return {
            "enriched": True,
            "operator_id": op_id,
            "harmonic_fingerprint": fingerprint,
            "semantic_mass": semantic_mass,
            "n_matching_cards": len(related),
            "matched_cards": related,
            "cielingo_analysis": {
                "operator": ci_analysis["operator"],
                "language": ci_analysis["language"],
                "tame": ci_analysis["tame"],
                "valency": ci_analysis["valency"],
                "router_sector": ci_analysis["router"].get("sector", ""),
                "router_confidence": ci_analysis["router"].get("confidence", 0.0),
                "grammar_curvature": ci_analysis["grammar"].get("curvature", 0.0),
                "scope_quantifiers": ci_analysis["scope"].get("quantifiers", []),
                "scope_negation": ci_analysis["scope"].get("negation", False),
                "deictic_markers": len(ci_analysis["deixis"]),
                "being_verbs": len(ci_analysis["ontological"].get("being_verbs", [])),
                "case_analysis": ci_analysis["case"][:3] if ci_analysis.get("case") else [],
            },
            "loop_id": loop.loop_id,
        }

    def scan_scars_via_phasenav(self, auto_apply: bool = True) -> dict:
        """Skanuj blizny → CIELingo operator + gramatyka → znajdź ścieżki PhaseNav.

        If auto_apply=True, saves repair candidates for paths with
        mean_affordance > 0.7 and score > 1.5, and marks scars as pending-repair.
        """
        solver = self.solver
        if solver is None:
            return {"scanned": False, "reason": "phasenav_solver_unavailable"}

        scars = self.state.get_scars(unresolved_only=True)
        if not scars:
            return {"scanned": True, "n_scars": 0, "n_card_matches": 0, "repair_paths": []}

        self.load_cards()
        repair_paths = []
        auto_applied = 0
        for scar in scars[:10]:
            source_ref = scar.get("source_ref", "")
            if not source_ref:
                continue

            scar_id = scar.get("scar_id", "?")
            loop_id = scar.get("loop_id")

            ci_analysis = self.ci.enrich_text(source_ref)
            scar_op = ci_analysis["operator"]
            scar_domain = scar_op.get("domain", "unknown")

            best_card_id = None
            best_score = 0.0
            source_lower = source_ref.lower()
            for cid, card in self._card_by_id.items():
                name = (card.get("name") or card.get("lemma") or cid).lower()
                if source_lower in name or name in source_lower:
                    if 2.0 > best_score:
                        best_score = 2.0
                        best_card_id = cid
                ops = (
                    card.get("operator_bindings")
                    or card.get("runtime_card", {}).get("runtime", {}).get("operator_bindings", [])
                )
                for op in ops:
                    if op.lower() in source_lower or scar_domain in op.lower():
                        if 1.5 > best_score:
                            best_score = 1.5
                            best_card_id = cid

                card_vec = card.get("phase_vector_36d") or card.get("runtime_card", {}).get("phase_vector_36d", [])
                if card_vec and scar_domain != "unknown":
                    card_name_meaning = (card.get("root_meaning") or card.get("function") or "").lower()
                    if scar_domain in card_name_meaning:
                        if 1.0 > best_score:
                            best_score = 1.0
                            best_card_id = cid

            trace = None
            mean_affordance = 0.0
            operator_hooks = []
            if best_card_id and best_score > 0.5:
                concepts = list(solver.data.concept_phases.keys())
                if best_card_id in concepts:
                    others = [c for c in concepts[:10] if c != best_card_id][:3]
                    if others:
                        try:
                            trace = solver.trace([best_card_id] + others)
                            mean_affordance = trace.mean_affordance
                            operator_hooks = [s.operator_hook for s in trace.steps]
                        except Exception as exc:
                            _log.debug("trace skipped: %s", exc)

            path_entry = {
                "scar_id": scar_id,
                "source_ref": source_ref,
                "matched_card": best_card_id,
                "score": best_score,
                "trace_steps": len(trace.steps) if trace else 0,
                "operator_hooks": operator_hooks,
                "mean_affordance": mean_affordance,
                "cielingo_domain": scar_domain,
                "cielingo_operator": scar_op.get("operator", "?"),
            }
            repair_paths.append(path_entry)

            if auto_apply and best_card_id and best_score > 1.5 and mean_affordance > 0.7:
                self.state.save_repair({
                    "repair_id": f"auto_{scar_id}",
                    "loop_id": loop_id,
                    "scar_id": scar_id,
                    "route_kind": f"phasenav_{scar_domain}",
                    "target_ref": best_card_id,
                    "description": f"Auto-repair via PhaseNav: {best_card_id} (aff={mean_affordance:.2f})",
                    "required_before_closure": True,
                    "confidence": min(1.0, best_score / 3.0 + mean_affordance / 2.0),
                    "status": "pending",
                })
                if trace:
                    self.learn_trace(trace, source=f"auto_repair_{scar_id}")
                auto_applied += 1

        if repair_paths:
            self.state.log_experience(
                "phasenav_scar_scan", "self_cycle",
                f"Found {len(repair_paths)} repair paths, auto-applied {auto_applied} "
                f"domains: {set(p['cielingo_domain'] for p in repair_paths)}",
                details=json.dumps({"repair_paths": repair_paths, "auto_applied": auto_applied}),
                salience=0.7,
            )
            self.write_memory_entry("scar_scan", str(_now()), {
                "n_scars": len(scars), "repair_paths": repair_paths, "auto_applied": auto_applied,
            })

        return {
            "scanned": True,
            "n_scars": len(scars),
            "n_card_matches": len(repair_paths),
            "repair_paths": repair_paths,
            "auto_applied": auto_applied,
        }

    # ── FEEDBACK DO LNS MODELU ──────────────────────────────────────────

    def update_grammar_profile(self, language: str, observed_vector: list[float],
                                 observation_weight: float = 0.1) -> dict:
        profile_path = LNS_GRAMMAR_EN if language == "en" else LNS_GRAMMAR_PL
        if not profile_path.exists():
            return {"updated": False, "reason": f"no_profile_for_{language}"}

        import copy
        profile = _load_yaml(profile_path)
        gauge = profile.get("grammar_as_gauge", {})
        current_vec = gauge.get("local_vector", [])
        if not current_vec or len(current_vec) != len(observed_vector):
            return {"updated": False, "reason": "vector_dim_mismatch",
                    "current_dim": len(current_vec), "observed_dim": len(observed_vector)}

        alpha = min(0.5, observation_weight)
        new_vec = [(1 - alpha) * float(v) + alpha * float(o)
                   for v, o in zip(current_vec, observed_vector)]
        gauge["local_vector"] = [round(v, 6) for v in new_vec]
        gauge["updated_at"] = _now()
        gauge["update_source"] = "phasenav_learning_bridge"

        profile["grammar_as_gauge"] = gauge
        import tempfile, shutil
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False, encoding="utf-8")
        try:
            import yaml
            yaml.dump(profile, tmp, default_flow_style=False, allow_unicode=True, sort_keys=False)
            tmp.close()
            shutil.move(tmp.name, str(profile_path))
        except Exception as ex:
            return {"updated": False, "error": str(ex)}
        finally:
            if not tmp.closed:
                tmp.close()

        self.ci._grammar_profiles[language] = [float(v) for v in new_vec]
        self.state.log_experience("grammar_profile_updated", "phasenav",
                                  f"Grammar profile {language} updated (α={alpha:.2f})",
                                  f"prev={current_vec[:4]}... new={new_vec[:4]}...",
                                  salience=observation_weight)
        return {"updated": True, "language": language, "alpha": alpha}

    def update_operator_weights(self, operator_id: str, delta: float = 0.05) -> dict:
        if not operator_id:
            return {"updated": False, "reason": "no_operator_id"}
        current = self.state.get_metric(f"op_weight_{operator_id}", 0.5)
        new_weight = max(0.0, min(1.0, current + delta))
        self.state.update_metric(f"op_weight_{operator_id}", new_weight)
        self.state.log_experience("operator_weight_updated", "phasenav",
                                  f"Operator {operator_id}: {current:.3f} → {new_weight:.3f}",
                                  salience=abs(delta))
        return {"updated": True, "operator_id": operator_id,
                "previous": current, "new": new_weight}

    # ── STATUS / METRYKI ────────────────────────────────────────────────

    def status(self) -> dict[str, Any]:
        """Kompletny status bridge'a — PhaseNav + CIELingo LNS."""
        self.load_cards()
        self.load_doc_concepts()
        solver = self.solver
        n_conc = len(solver.data.concept_phases) if solver else 0
        n_edges = len(solver.data.edges) if solver else 0
        n_ops = len(solver.data.operator_vectors) if solver else 0
        db_stats = self.knowledge_db_stats()
        pn_entries = self.read_phasenav_entries(5)
        ci_status = self.ci.status()
        diag = self.ci.diagnostic_summary()
        return {
            "solver_available": solver is not None,
            "card_count": len(self._card_by_id),
            "card_operators": len(self._operator_index),
            "cielingo_concepts": n_conc,
            "cielingo_edges": n_edges,
            "cielingo_operators": n_ops,
            "doc_concepts": len(self._doc_concepts),
            "doc_op_unique": len(self._doc_operators),
            "doc_top_ops": [{"op": op, "score": round(s, 2)} for op, s in self._top_operators[:10]],
            "knowledge_db": db_stats,
            "last_phasenav_entries": pn_entries,
            "cielingo_lns": ci_status,
            "cross_language": diag,
        }

    def count(self) -> dict[str, int]:
        self.load_cards()
        self.load_doc_concepts()
        solver = self.solver
        n_conc = len(solver.data.concept_phases) if solver else 0
        n_edges = len(solver.data.edges) if solver else 0
        n_ops = len(solver.data.operator_vectors) if solver else 0
        return {
            "cielingo_cards": len(self._card_by_id),
            "cielingo_operators": len(self._operator_index),
            "doc_concepts_in_db": len(self._doc_concepts),
            "doc_operators_unique": len(self._doc_operators),
            "concepts": n_conc,
            "edges": n_edges,
            "operators": n_ops,
        }

    def knowledge_db_stats(self) -> dict:
        conn = _connect(KNOWLEDGE_DB)
        stats = {}
        for table in ["doc_analysis", "doc_concepts", "phasenav_entries", "phasenav_relations", "doc_orbital_position"]:
            try:
                row = conn.execute(f"SELECT COUNT(*) as c FROM {table}").fetchone()
                stats[table] = row["c"]
            except sqlite3.OperationalError:
                stats[table] = 0
        conn.close()
        return stats

    def top_operators_from_db(self, n: int = 20) -> list[dict]:
        self.load_doc_concepts()
        return [{"operator_id": op, "total_score": round(score, 2)} for op, score in self._doc_operators.items()][:n]


# ─── FUNKCJE WYGODY ──────────────────────────────────────────────────────

def phasenav_learn_trace(card_ids: list[str], state: CIELingoStateEngine | None = None) -> dict:
    bridge = PhaseNavLearningBridge(state=state)
    solver = bridge.solver
    if solver is None:
        return {"learned": False, "reason": "phasenav_unavailable"}
    trace = solver.trace(card_ids)
    return bridge.learn_trace(trace)


def phasenav_enrich_text(text: str, state: CIELingoStateEngine | None = None) -> dict:
    bridge = PhaseNavLearningBridge(state=state)
    return bridge.enrich_and_learn(text)


def phasenav_scan_scars(state: CIELingoStateEngine | None = None) -> dict:
    bridge = PhaseNavLearningBridge(state=state)
    return bridge.scan_scars_via_phasenav()


def phasenav_cielingo_analyze(text: str) -> dict:
    """Szybka analiza CIELingo LNS bez persistencji."""
    bridge = PhaseNavLearningBridge(auto_init=False)
    return bridge.ci.enrich_text(text)


def phasenav_cielingo_status() -> dict:
    """Status wszystkich CIELingo LNS subsystemów."""
    bridge = PhaseNavLearningBridge(auto_init=False)
    return bridge.ci.status()


__all__ = [
    "PhaseNavLearningBridge",
    "CIELingoSubsystems",
    "phasenav_learn_trace",
    "phasenav_enrich_text",
    "phasenav_scan_scars",
    "phasenav_cielingo_analyze",
    "phasenav_cielingo_status",
]
