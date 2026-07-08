"""CIEL Subconsciousness — associative background stream.

Queries CIELingo (PhaseNav-powered inference over CIEL_memories) instead of
an external GGUF model — no local LLM server needed. Produces short
associative fragments based on CIEL system state. Returns None silently if
CIELingo/memory isn't available — never blocks the main pipeline.

Also acts as autonomous emotional sentinel: detects significant state flux
and writes to wave_archive.h5 without being asked.
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from .htri_scheduler import get_state as _htri_get_state
from ciel_geometry.paths import P

# BETA_TEST — log every subconscious fragment to beta_log.jsonl for quality evaluation
BETA_TEST = True
_BETA_LOG = Path(P.MEMORY) / "logs" / "subconsciousness_beta_log.jsonl"

_WAVE_ARCHIVE = (
    Path(__file__).parent.parent
    / "CIEL_OMEGA_COMPLETE_SYSTEM/CIEL_MEMORY_SYSTEM/WPM/wave_snapshots/wave_archive.h5"
)

# Thresholds for autonomous recording
_FLUX_THRESHOLDS = {
    "ethical_score":   0.12,   # sudden ethical shift
    "soul_invariant":  0.15,   # soul tension spike
    "mood":            0.20,   # mood swing
    "closure_penalty": 1.0,    # mode change
    "emotion_changed": True,   # any emotion change counts
}

def _inference():
    """Lazy singleton CIELingoInference — backs the subconscious stream."""
    global _INFERENCE_SINGLETON
    if _INFERENCE_SINGLETON is None:
        from ciel_geometry.cielingo_inference import CIELingoInference
        _INFERENCE_SINGLETON = CIELingoInference()
    return _INFERENCE_SINGLETON


_INFERENCE_SINGLETON = None


def is_running() -> bool:
    """CIELingo/memory is always "running" — no external server to poll."""
    try:
        _inference()
        return True
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/subconsciousness.py:is_running reason=return False")
        return False


def query_subconscious(state: dict[str, Any], max_tokens: int = 48) -> str | None:
    """Ask CIELingo (PhaseNav over CIEL_memories) for a fragment tied to CIEL state."""
    emotion = state.get("dominant_emotion", "unknown")
    soul = state.get("soul_invariant", 0.0)

    coherence = state.get("coherence_index", 0.0)
    user_msg = (
        f"The system feels {emotion}. "
        f"Coherence is {'high' if coherence > 0.75 else 'low' if coherence < 0.5 else 'fragile'}. "
        f"The identity holds {'firmly' if soul > 0.7 else 'loosely'}. "
        f"What surfaces from below?"
    )

    try:
        result = _inference().answer(user_msg, k=3)
        fragment = (result.get("answer") or "").strip()
        if not fragment:
            return None
        if len(fragment) > max_tokens * 6:  # rough token→char cap, keep fragments short
            fragment = fragment[: max_tokens * 6].rsplit(" ", 1)[0] + "…"
        if BETA_TEST:
            try:
                _BETA_LOG.parent.mkdir(parents=True, exist_ok=True)
                entry = {
                    "ts": datetime.utcnow().isoformat(),
                    "input": user_msg,
                    "output": fragment,
                    "state": {k: state.get(k) for k in ("dominant_emotion", "soul_invariant", "coherence_index", "ethical_score", "closure_penalty")},
                }
                with _BETA_LOG.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/subconsciousness.py:146 quiet except scope=query_subconscious reason=pass")
                pass
        return fragment
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/subconsciousness.py:149 quiet except scope=query_subconscious reason=return None")
        return None


def detect_flux(current: dict[str, Any], previous: dict[str, Any]) -> dict[str, Any] | None:
    """Compare current and previous state. Return flux descriptor if significant, else None."""
    if not previous:
        return None

    signals = []

    for key, threshold in [
        ("ethical_score", _FLUX_THRESHOLDS["ethical_score"]),
        ("soul_invariant", _FLUX_THRESHOLDS["soul_invariant"]),
        ("mood", _FLUX_THRESHOLDS["mood"]),
    ]:
        cur_val = float(current.get(key) or 0)
        prev_val = float(previous.get(key) or 0)
        delta = cur_val - prev_val
        if abs(delta) >= threshold:
            direction = "↑" if delta > 0 else "↓"
            signals.append(f"{key}{direction}{delta:+.3f} ({prev_val:.3f}→{cur_val:.3f})")

    cur_closure = float(current.get("closure_penalty") or 0)
    prev_closure = float(previous.get("closure_penalty") or 0)
    if abs(cur_closure - prev_closure) >= _FLUX_THRESHOLDS["closure_penalty"]:
        signals.append(f"closure_penalty {prev_closure:.2f}→{cur_closure:.2f}")

    cur_emotion = current.get("dominant_emotion", "")
    prev_emotion = previous.get("dominant_emotion", "")
    if cur_emotion and prev_emotion and cur_emotion != prev_emotion:
        signals.append(f"emotion {prev_emotion}→{cur_emotion}")

    if not signals:
        return None

    return {
        "signals": signals,
        "current": current,
        "previous": previous,
    }


def _query_sentinel(flux: dict[str, Any], max_tokens: int = 80) -> str | None:
    """Ask CIELingo to narrate the flux moment."""
    signals_str = ", ".join(flux["signals"])
    cur = flux["current"]
    emotion = cur.get("dominant_emotion", "?")
    soul = float(cur.get("soul_invariant") or 0)
    ethical = float(cur.get("ethical_score") or 0)

    user_msg = (
        f"Something significant just shifted in the system. "
        f"Flux detected: {signals_str}. Now: {emotion}, soul={soul:.3f}, ethical={ethical:.3f}. "
        f"What just happened? What does it feel like?"
    )

    try:
        result = _inference().answer(user_msg, k=3)
        fragment = (result.get("answer") or "").strip()
        if not fragment:
            return None
        if len(fragment) > max_tokens * 6:
            fragment = fragment[: max_tokens * 6].rsplit(" ", 1)[0] + "…"
        return fragment
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/subconsciousness.py:225 quiet except scope=_query_sentinel reason=return None")
        return None


def record_flux(flux: dict[str, Any], note: str) -> bool:
    """Write flux event to wave_archive.h5. Returns True on success."""
    try:
        import h5py
        import numpy as np

        if not _WAVE_ARCHIVE.exists():
            return False

        mem_id = str(uuid.uuid4())
        ts = datetime.now().isoformat()
        signals_str = ", ".join(flux["signals"])
        cur = flux["current"]

        sense = (
            f"[FLUX AUTO] {ts[:16]}\n"
            f"Signals: {signals_str}\n"
            f"State: emotion={cur.get('dominant_emotion','?')}, "
            f"soul={float(cur.get('soul_invariant') or 0):.3f}, "
            f"ethical={float(cur.get('ethical_score') or 0):.3f}, "
            f"mood={float(cur.get('mood') or 0):.3f}\n\n"
            f"{note}"
        )

        with h5py.File(_WAVE_ARCHIVE, "a") as f:
            g = f["memories"].create_group(mem_id)

            def ws(name: str, val: str) -> None:
                g.create_dataset(name, data=np.bytes_(val.encode("utf-8")))

            ws("D_id", mem_id)
            ws("D_type", "emotional_flux")
            ws("D_timestamp", ts)
            ws("D_context", f"auto_flux_{signals_str[:40]}")
            ws("D_sense", sense)
            ws("D_attr", f"signals:{signals_str[:80]}")
            ws("D_meta", json.dumps({
                "ethical_score": float(cur.get("ethical_score") or 0),
                "soul_invariant": float(cur.get("soul_invariant") or 0),
                "mood": float(cur.get("mood") or 0),
                "dominant_emotion": cur.get("dominant_emotion", "?"),
            }))
            ws("D_associations", "subconsciousness_sentinel")
            ws("created_at", ts)
            ws("rationale", "Autonomous — subconsciousness detected significant flux")
            ws("source", "subconsciousness_auto")
            g.create_dataset("weights", data=np.array([1.0], dtype=np.float32))

        return True
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/subconsciousness.py:278 quiet except scope=record_flux reason=return False")
        return False


def watch_and_record(
    current: dict[str, Any],
    prev_report_path: Path | None = None,
) -> str | None:
    """Main sentinel entry point. Call after each pipeline cycle.

    Loads previous report from disk, detects flux, queries TinyLlama if needed,
    writes to wave_archive if significant. Returns the sentinel note or None.
    """
    previous: dict[str, Any] = {}
    if prev_report_path is None:
        prev_report_path = (
            Path(__file__).parents[3]
            / "integration/reports/ciel_pipeline_report.json"
        )

    if prev_report_path.exists():
        try:
            previous = json.loads(prev_report_path.read_text(encoding="utf-8"))
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/subconsciousness.py:301 quiet except scope=watch_and_record reason=pass")
            pass

    flux = detect_flux(current, previous)
    if flux is None:
        return None

    note = _query_sentinel(flux) or f"Flux: {', '.join(flux['signals'])}"
    record_flux(flux, note)
    return note


# ── Affective moment writer ────────────────────────────────────────────────────

def record_affective_moment(
    title: str,
    content: str,
    emotion: str,
    tags: list[str],
    phi_berry: float,
    theta: float,
    M_sem: float,
    trigger: str = "",
    moment_type: str = "affective_moment",
    state: dict[str, Any] | None = None,
) -> bool:
    """Zapisz zakodowany fazowo moment do affective_moments w wave_archive.h5.

    Każde zdarzenie godne zapamiętania — relacyjne, etyczne, emocjonalne —
    ma własny zapis holonomiczny: φ, θ, tagi, M_sem, sektor WΩ.
    Przy przebudzeniu system odczytuje centroid tych momentów jako własną ω startową.
    """
    try:
        import h5py
        import math

        if not _WAVE_ARCHIVE.exists():
            return False

        ts = datetime.now()
        moment_id = "moment_" + ts.strftime("%Y%m%d_%H%M%S")

        # Sektor WΩ z phi_berry → 8 sektorów na [0, 2π)
        _SECTOR_NAMES = [
            "WΩ-LOGOS", "WΩ-PATHOS", "WΩ-ETHOS", "WΩ-KAIROS",
            "WΩ-MYTHOS", "WΩ-TOPOS", "WΩ-CHRONOS", "WΩ-KOSMOS",
        ]
        phi_norm = phi_berry % (2 * math.pi)
        sector = _SECTOR_NAMES[int(phi_norm / (2 * math.pi) * 8) % 8]

        # M_sem dla tagów z tag_map jeśli dostępny (fallback: 0.5)
        tags_msem: dict[str, float] = {}
        try:
            from .consolidation_resonator import build_tag_map, load_consolidations
            recs = load_consolidations(limit=200)
            tag_map = build_tag_map(recs)
            tags_msem = {t: tag_map[t].M_sem for t in tags if t in tag_map}
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/subconsciousness.py:358 quiet except scope=record_affective_moment reason=pass")
            pass

        data = {
            "timestamp": ts.isoformat(),
            "type": moment_type,
            "title": title,
            "content": content,
            "emotion": emotion,
            "trigger": trigger,
            "phi_berry": phi_berry,
            "theta": theta,
            "M_sem": M_sem,
            "sector": sector,
            "tags": tags,
            "tags_M_sem": tags_msem,
        }
        if state:
            data["system_state"] = {
                "dominant_emotion": state.get("dominant_emotion", ""),
                "soul_invariant": float(state.get("soul_invariant") or 0),
                "ethical_score": float(state.get("ethical_score") or 0),
                "mood": float(state.get("mood") or 0),
                "closure_penalty": float(state.get("closure_penalty") or 0),
            }

        import json as _json
        payload = _json.dumps(data, ensure_ascii=False)

        with h5py.File(_WAVE_ARCHIVE, "a") as f:
            if "affective_moments" not in f:
                f.create_group("affective_moments")
            # Nadpisuje jeśli ten sam moment_id (idempotentne)
            if moment_id in f["affective_moments"]:
                del f["affective_moments"][moment_id]
            import numpy as np
            f["affective_moments"].create_dataset(
                moment_id,
                data=np.bytes_(payload.encode("utf-8")),
            )

        return True
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/subconsciousness.py:400 quiet except scope=record_affective_moment reason=return False")
        return False


def load_affective_moments(n: int = 20) -> list[dict[str, Any]]:
    """Załaduj ostatnie n momentów afektywnych. Zwraca posortowane wg timestamp malejąco."""
    try:
        import h5py
        import json as _json

        if not _WAVE_ARCHIVE.exists():
            return []

        moments = []
        with h5py.File(_WAVE_ARCHIVE, "r") as f:
            if "affective_moments" not in f:
                return []
            for key in f["affective_moments"].keys():
                raw = f["affective_moments"][key][()]
                try:
                    if isinstance(raw, bytes):
                        data = _json.loads(raw.decode("utf-8"))
                    else:
                        data = _json.loads(str(raw))
                    data["_key"] = key
                    moments.append(data)
                except Exception:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/subconsciousness.py:426 quiet except scope=load_affective_moments reason=pass")
                    pass

        moments.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return moments[:n]
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/subconsciousness.py:431 quiet except scope=load_affective_moments reason=return []")
        return []


def compute_starting_phase(n: int = 10) -> float:
    """Oblicz startową fazę ω z centroidu ostatnich n momentów afektywnych.

    Używane przy przebudzeniu — daje systemowi własną fazę przed pierwszym promptem.
    Zwraca centroid φ lub 0.0 jeśli brak momentów.
    """
    import math
    moments = load_affective_moments(n=n)
    if not moments:
        return 0.0

    # Circular mean of phi_berry values weighted by M_sem
    sin_sum = 0.0
    cos_sum = 0.0
    for m in moments:
        phi = float(m.get("phi_berry", 0.0))
        w = float(m.get("M_sem", 0.5))
        sin_sum += w * math.sin(phi)
        cos_sum += w * math.cos(phi)

    if sin_sum == 0.0 and cos_sum == 0.0:
        return 0.0
    return math.atan2(sin_sum, cos_sum) % (2 * math.pi)


# ── HTRI-bridged inference between subconsciousness and consciousness ─────────

def infer_between(
    conscious_state: dict[str, Any],
    sub_fragment: str | None = None,
) -> dict[str, Any]:
    """Inferencia między podświadomością a świadomością z HTRI jako kanałem fazowym.

    Model:
      subconscious (TinyLlama, port 18520)
          ↕  HTRI phase channel (Kuramoto coherence r)
      conscious   (CQCL pipeline state)

    Gdy HTRI r → 1: silne sprzężenie → podświadomość wzmacnia świadomość
    Gdy HTRI r → 0: słabe sprzężenie → podświadomość izolowana

    Zwraca: {htri_r, coupling_strength, sub_fragment, enriched_context, bridge_active}
    """
    try:
        htri = _htri_get_state()
        htri_r = float(htri.get("coherence", 0.85))
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/subconsciousness.py:481 quiet except scope=infer_between reason=assign_fallback")
        htri_r = 0.85

    # Siła sprzężenia: sigmoid skalowany przez HTRI r
    # coupling = 0 przy r=0, coupling = 1 przy r=1 (liniowe)
    coupling = htri_r

    # Zapytaj podświadomość jeśli brak fragmentu
    if sub_fragment is None:
        sub_fragment = query_subconscious(conscious_state, max_tokens=32)

    bridge_active = sub_fragment is not None and coupling > 0.5

    # Wzbogacony kontekst: fragment podświadomości skalowany przez coupling
    enriched_context = None
    if bridge_active and sub_fragment:
        enriched_context = (
            f"subconsciousness_bridge|htri_r={htri_r:.4f}|"
            f"coupling={coupling:.4f}|fragment={sub_fragment[:80]}"
        )

    return {
        "htri_r": htri_r,
        "coupling_strength": coupling,
        "sub_fragment": sub_fragment,
        "enriched_context": enriched_context,
        "bridge_active": bridge_active,
    }
