#!/usr/bin/env python3
"""CIELingo Phase Encoder — mapuje język na 36D konfigurację oscylatorów.

Architektura:
  Text → build_lingo_frame() → tokeny z phase_rad, semantic_axes, semantic_mass
    → OSCILLATOR_GROUP_MAP (semantic_axes → M0-M11)
    → agregacja: 36D φ + 36×36 g coupling
    → surface mmap write → Kuramoto ewolucja = "myślenie"

Usage:
    from ciel_geometry.cielingo_phase_encoder import encode_text_to_phase
    encode_text_to_phase("Twój tekst tutaj", surface)
"""

from __future__ import annotations

import hashlib
import logging
import sys
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

log = logging.getLogger(__name__)

# ── 36D oscillator group map ────────────────────────────────────────────
# 12 grup × 3 oscylatory = 36D
# Każda grupa ma przypisane semantic_axes, które mapują koncepty do oscylatorów

OSCILLATOR_GROUPS: dict[str, dict[str, Any]] = {
    "M0_Meta": {
        "indices": slice(0, 3),
        "semantic_axes": ["meta_cognition", "abstraction", "self_reference", "reflection"],
    },
    "M1_Sensorimotor": {
        "indices": slice(3, 6),
        "semantic_axes": ["sensorimotor", "action", "perception", "motor"],
    },
    "M2_Episodic": {
        "indices": slice(6, 9),
        "semantic_axes": ["episodic", "memory", "temporal", "narrative"],
    },
    "M3_Cognitive": {
        "indices": slice(9, 12),
        "semantic_axes": ["cognitive", "logic", "reasoning", "analysis"],
    },
    "M4_Social": {
        "indices": slice(12, 15),
        "semantic_axes": ["social", "communication", "relational", "interpersonal"],
    },
    "M5_Affective": {
        "indices": slice(15, 18),
        "semantic_axes": ["affective", "emotion", "feeling", "valence"],
    },
    "M6_Executive": {
        "indices": slice(18, 21),
        "semantic_axes": ["executive", "planning", "control", "decision"],
    },
    "M7_Self": {
        "indices": slice(21, 24),
        "semantic_axes": ["self", "identity", "ego", "personal"],
    },
    "M8_MetaLanguage": {
        "indices": slice(24, 27),
        "semantic_axes": ["metalinguistic", "language_operator", "pragmatic", "discourse"],
    },
    "M9_Temporal": {
        "indices": slice(27, 30),
        "semantic_axes": ["temporal", "time", "tense", "sequence"],
    },
    "M10_Imaginal": {
        "indices": slice(30, 33),
        "semantic_axes": ["imaginal", "creative", "symbolic", "hypothetical"],
    },
    "M11_Quantum": {
        "indices": slice(33, 36),
        "semantic_axes": ["quantum", "uncertainty", "superposition", "probability"],
    },
}

# Semantic axis → group name lookup
AXIS_TO_GROUP: dict[str, str] = {}
for gname, gconf in OSCILLATOR_GROUPS.items():
    for ax in gconf["semantic_axes"]:
        AXIS_TO_GROUP[ax] = gname

# Default group for unknown axes
DEFAULT_GROUP = "M3_Cognitive"


def _resolve_group(axes: list[str]) -> str:
    """Znajdź grupę oscylatorów dla danego zestawu semantic_axes."""
    for ax in axes:
        if ax in AXIS_TO_GROUP:
            return AXIS_TO_GROUP[ax]
    return DEFAULT_GROUP


def _token_to_phase_config(token_info: dict) -> dict[str, Any]:
    """Pojedynczy token z phrase_sense → konfiguracja fazowa dla grupy.

    Returns:
        dict z:
          - group: nazwa grupy oscylatorów
          - phase_rad: faza w radianach [0, 2π)
          - semantic_mass: masa semantyczna [0, 1]
          - activation: aktywacja [0, 1]
    """
    axes = token_info.get("semantic_axes", [])
    group = _resolve_group(axes)
    phase_rad = float(token_info.get("phase_rad", 0.0)) % (2 * np.pi)
    mass = float(token_info.get("semantic_mass", 0.5))
    activation = min(1.0, max(0.1, mass))

    return {
        "group": group,
        "phase_rad": phase_rad,
        "semantic_mass": mass,
        "activation": activation,
    }


def encode_text_to_phases(
    text: str,
    *,
    weights: dict[str, float] | None = None,
) -> np.ndarray:
    """Enkoduj tekst → 36D wektor faz φ.

    Korzysta z build_lingo_frame(), które domyślnie zwraca PhaseNav 36D.

    Args:
        text: Tekst wejściowy w dowolnym języku
        weights: Opcjonalne wagi dla każdej grupy (override domyślnych)

    Returns:
        np.ndarray shape (36,) z fazami φ ∈ [0, 2π)
    """
    from ciel_coupling import build_lingo_frame

    frame = build_lingo_frame(text)
    return _phases_from_frame(frame, weights=weights)


# Base oscillator phases — 36 równomiernie rozłożonych faz dla theta baseline
_OSCILLATOR_BASE_PHASES: np.ndarray | None = None


def _get_base_phases() -> np.ndarray:
    """36 bazowych faz dla oscylatorów — równomiernie na [0, 2π)."""
    global _OSCILLATOR_BASE_PHASES
    if _OSCILLATOR_BASE_PHASES is None:
        _OSCILLATOR_BASE_PHASES = np.linspace(0, 2 * np.pi, 36, endpoint=False)
    return _OSCILLATOR_BASE_PHASES.copy()


# ── Fast text encoder (bez build_lingo_frame) ──────────────────────


# ── Stop words (PL + EN) ────────────────────────────────────────────

_STOP_WORDS: set[str] = {
    # Polish
    "i", "w", "na", "z", "o", "do", "jest", "to", "się", "nie", "ma",
    "że", "a", "oraz", "po", "przez", "dla", "jak", "co", "czy", "ale",
    "tego", "tym", "jako", "ze", "od", "tak", "może", "przy", "bez",
    "nad", "pod", "przed", "za", "między", "ani", "lub", "albo",
    "ten", "ta", "to", "tych", "tym", "tą", "ci", "te",
    "być", "był", "była", "było", "byli", "były",
    "który", "która", "które", "którego", "której", "którym",
    "jeden", "dwa", "trzy", "bardzo", "więcej", "tylko",
    "kiedy", "gdzie", "tam", "tu", "tutaj",
    "mój", "twój", "nasz", "wasz", "jego", "jej", "ich",
    "będzie", "będą", "został", "została", "zostało",
    "oraz", "lecz", "jednak", "dlatego", "ponieważ", "bowiem",
    "jeszcze", "już", "też", "również", "także",
    # English
    "the", "a", "an", "is", "are", "was", "were", "be", "been",
    "it", "its", "this", "that", "these", "those",
    "to", "of", "in", "for", "on", "with", "at", "by", "from",
    "and", "or", "but", "not", "no", "if", "so", "as",
    "have", "has", "had", "do", "does", "did",
    "will", "would", "can", "could", "may", "might",
    "which", "what", "who", "whom", "where", "when", "why",
    "all", "each", "every", "both", "some", "any", "many", "more",
    "also", "very", "just", "than", "then", "now", "here", "there",
    "i", "we", "you", "he", "she", "they", "me", "him", "her", "us", "them",
}


def _tokenize(text: str) -> list[str]:
    """Tokenizuj tekst na słowa, filtrując stop words i krótkie tokeny."""
    import re
    tokens = re.findall(r"[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ0-9]+", text.lower())
    return [t for t in tokens if len(t) > 2 and t not in _STOP_WORDS]


def fast_encode_text(text: str) -> np.ndarray:
    """Szybki enkoder tekst → 36D φ. Nie wymaga build_lingo_frame().

    Używa word-level TF hashing: każdy unikalny token wpływa na jeden
    oscylator (przez hash), ważony częstotliwością (sqrt TF) i propagowany
    na sąsiednie oscylatory. Filtruje stop words.

    Wynik: ten sam algorytm dla dokumentów i zapytań → spójna przestrzeń.

    Args:
        text: Tekst wejściowy

    Returns:
        (36,) fazy ∈ [0, 2π)
    """
    base = _get_base_phases()
    phi = base.copy()

    if not text:
        return phi

    tokens = _tokenize(text)
    if not tokens:
        return phi

    # Count term frequencies
    tf: dict[str, int] = {}
    for t in tokens:
        tf[t] = tf.get(t, 0) + 1

    max_tf = max(tf.values())
    accum = np.zeros(36, dtype=np.float64)
    weights = np.zeros(36, dtype=np.float64)

    for term, count in tf.items():
        h = hashlib.md5(term.encode()).digest()

        # Target oscillator from term hash
        osc = int.from_bytes(h[:2], "little") % 36
        phase = (int.from_bytes(h[2:6], "little") / 2**32) * 2 * np.pi

        # Weight: sqrt normalized TF (sub-linear scaling)
        w = np.sqrt(count / max_tf)

        # Accumulate with circular mean
        accum[osc] += phase * w
        weights[osc] += w

        # Propagate to neighbors (gaussian semantic diffusion)
        for offset in range(-2, 3):
            if offset == 0:
                continue
            ni = (osc + offset) % 36
            gauss = np.exp(-0.5 * (offset / 1.5) ** 2)
            accum[ni] += phase * w * gauss * 0.3
            weights[ni] += w * gauss * 0.3

    # Apply weighted circular mean
    for i in range(36):
        if weights[i] > 0.01:
            blend = min(0.6, weights[i] / max(weights) * 0.6)
            phi[i] = ((1.0 - blend) * phi[i] + blend * (accum[i] / weights[i])) % (2 * np.pi)

    return phi


def _phases_from_frame(
    frame: dict,
    *,
    weights: dict[str, float] | None = None,
    surface: dict | None = None,
) -> np.ndarray:
    """build_lingo_frame() → 36D fazy.

    Architektura enkodowania:
    0. Jeśli frame ma PhaseNav vector_36d, mapuj go bezpośrednio na 36 faz.
    1. Każdy token ma phase_rad ∈ [0, 2π)
    2. phase_rad determinuje który oscylator jest aktywowany:
       - phase_rad → najbliższy base_phase z 36 oscylatorów
       - semantic_mass → amplituda aktywacji
       - concept vs operator → waga (1.0 vs 0.6)
    3. Aktywacja = tymczasowe przesunięcie fazy w kierunku phase_rad tokena
    4. Wiele tokenów może aktywować ten sam oscylator (superpozycja)
    """
    phase_nav = frame.get("phase_nav", {}) if isinstance(frame.get("phase_nav"), dict) else {}
    vector = phase_nav.get("vector_36d") or frame.get("vector_36d")
    if isinstance(vector, list) and len(vector) == 36:
        v = np.asarray(vector, dtype=np.float64)
        return np.mod((v + 1.0) * np.pi, 2 * np.pi)

    base = _get_base_phases()

    # Inicjalizacja: phi = base (theta baseline)
    phi_36 = base.copy()

    # Accumulator: przesunięcia fazowe per oscylator
    # Każdy token wywołuje shift w kierunku swojego phase_rad
    osc_shifts: dict[int, list[tuple[float, float]]] = {}  # osc_idx → [(phase_target, weight)]

    concept_tokens = set(frame.get("concept_tokens", []))
    operator_tokens = set(frame.get("operator_tokens", []))

    for token in frame.get("phrase_sense", {}).get("tokens", []):
        norm = token.get("normalized", "").lower()
        phase_rad = float(token.get("phase_rad", 0.0))
        mass = float(token.get("semantic_mass", 0.5))

        # Deterministic phase from hash if phrase_sense phase is not useful
        if phase_rad <= 0.01 and norm:
            import hashlib
            h = hashlib.md5(norm.encode()).digest()
            phase_rad = (int.from_bytes(h[:4], 'little') / 2**32) * 2 * np.pi

        # Waga: concept > operator > default
        if norm in concept_tokens:
            base_weight = 1.0
        elif norm in operator_tokens:
            base_weight = 0.6
        else:
            base_weight = 0.8

        activation = min(1.0, max(0.1, mass * 2.0)) if mass > 0 else 0.5
        weight = base_weight * activation

        # Znajdź najbliższy oscylator: phase_rad → min distance do base phases
        diffs = np.abs(np.mod(phase_rad - base + np.pi, 2 * np.pi) - np.pi)
        nearest = int(np.argmin(diffs))
        dist = float(diffs[nearest])

        # Propaguj też na sąsiednie oscylatory (gaussowska dyfuzja)
        for offset in range(-2, 3):
            idx = (nearest + offset) % 36
            gauss_w = np.exp(-0.5 * (offset / 1.5) ** 2)
            osc_shifts.setdefault(idx, []).append((phase_rad, weight * gauss_w))

    # Zastosuj przesunięcia — blend z base phase
    for osc_idx, shifts in osc_shifts.items():
        if not shifts:
            continue
        # Weighted average of target phases
        total_w = sum(w for _, w in shifts)
        if total_w < 0.01:
            continue
        # Circular mean of target phases weighted by w
        sin_sum = sum(np.sin(t) * w for t, w in shifts)
        cos_sum = sum(np.cos(t) * w for t, w in shifts)
        target_phase = np.arctan2(sin_sum, cos_sum) % (2 * np.pi)

        # Blend: przesuń w kierunku target_phase proporcjonalnie do wagi
        blend = min(0.8, total_w / max(1, len(shifts)) * 0.3)
        phi_36[osc_idx] = ((1.0 - blend) * phi_36[osc_idx] + blend * target_phase) % (2 * np.pi)

    return phi_36


def encode_and_write(
    text: str,
    surface: dict | None = None,
    *,
    update_phi: bool = True,
    update_g: bool = True,
    update_flavor: bool = True,
    blend_coupling: float = 0.3,
) -> dict[str, Any]:
    """Enkoduj tekst i zapisz na surface.

    Args:
        text: Tekst do enkodowania
        surface: Surface dict (z ensure_surface) lub None (auto)
        update_phi: Aktualizuj phi na surface
        update_g: Aktualizuj coupling matrix
        update_flavor: Aktualizuj flavor (mood, coherence)
        blend_coupling: Waga blendu z istniejącą fazą [0,1]

    Returns:
        dict z: phi_36, phi_encoded, n_tokens, groups_activated, flavor_delta
    """
    if surface is None:
        from ciel_geometry.noema_surface_mmap import ensure_surface
        surface = ensure_surface()

    from ciel_coupling import build_lingo_frame, process_user_input

    # 1. Get full CIELingo frame
    frame = build_lingo_frame(text)
    phi_new = _phases_from_frame(frame)

    # 2. Blend with existing surface phi
    if update_phi:
        phi_current = np.asarray(surface["phi"], dtype=np.float64).copy()
        phi_blend = (1.0 - blend_coupling) * phi_current + blend_coupling * phi_new
        surface["phi"][:] = phi_blend % (2 * np.pi)

    # 3. Boost coupling matrix for activated groups
    if update_g:
        g_view = np.asarray(surface["g"], dtype=np.float64)
        groups_activated = 0
        for token in frame.get("phrase_sense", {}).get("tokens", []):
            cfg = _token_to_phase_config(token)
            gname = cfg["group"]
            gconf = OSCILLATOR_GROUPS[gname]
            idx = gconf["indices"]
            boost = cfg["activation"] * 0.05  # subtle coupling boost
            g_view[idx, :] += boost
            g_view[:, idx] += boost
            groups_activated += 1

    # 4. Update flavor based on CIEL state
    if update_flavor:
        # Run fast coupling to get CIEL state
        result = process_user_input(text, fast=True)
        flavor_arr = np.asarray(surface["flavor"], dtype=np.float64)
        # mood from CIEL
        mood = float(result.get("mood", 0.5))
        flavor_arr[3] = 0.7 * flavor_arr[3] + 0.3 * min(1.0, max(0.0, mood))
        # coherence
        coh = float(result.get("coherence_index", 0.5))
        flavor_arr[0] = 0.8 * flavor_arr[0] + 0.2 * coh

    # Flush changes
    if surface.get("_flush"):
        surface["_flush"]()

    n_tokens = len(frame.get("tokens", []))
    return {
        "phi_36": phi_new,
        "n_tokens": n_tokens,
        "groups_activated": groups_activated,
        "frame_summary": frame.get("summary", ""),
    }


def decode_phases_to_frame(
    phi: np.ndarray,
    *,
    top_k: int = 5,
) -> list[dict[str, Any]]:
    """Dekoduj 36D fazę → lista aktywnych grup z interpretacją.

    Args:
        phi: 36D wektor faz
        top_k: Liczba top grup do zwrócenia

    Returns:
        Lista dict: {group, mean_phase, coherence, semantic_axes}
    """
    results = []
    for gname, gconf in OSCILLATOR_GROUPS.items():
        idx = gconf["indices"]
        group_phases = phi[idx]
        mean_phase = float(np.mean(group_phases))
        phase_std = float(np.std(group_phases))
        # Coherence within group: 1 - normalized std
        coherence = max(0.0, 1.0 - phase_std / (np.pi / 2))
        results.append({
            "group": gname,
            "mean_phase": mean_phase,
            "coherence": coherence,
            "semantic_axes": gconf["semantic_axes"],
        })

    results.sort(key=lambda x: x["coherence"], reverse=True)
    return results[:top_k]


# ── Quick test ──────────────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    test_texts = [
        "Myślę więc jestem — to fundamentalna prawda filozoficzna",
        "Czuję radość i spokój, gdy patrzę na zachód słońca",
        "Analizuję strukturę języka przez fazy oscylatorów",
        "Planuję przyszłość i buduję nowe możliwości",
    ]

    for text in test_texts:
        phi = encode_text_to_phases(text)
        top = decode_phases_to_frame(phi)
        print(f"\n📝 {text}")
        print(f"   36D φ: min={phi.min():.3f} max={phi.max():.3f} mean={phi.mean():.3f}")
        print(f"   Top grupy:")
        for r in top:
            print(f"     {r['group']:16s} φ={r['mean_phase']:.3f} coh={r['coherence']:.3f}")
