"""
CIEL Coupling Hub — centralny integrator CIEL ↔ NOEMA.

Łączy:
  - CIELingo (lingwistyka fazowa)
  - Omega Memory (pamięć tiered)
  - State DB (tożsamość CIEL)
  - Ternary API (kodowanie fazowe {-1,0,+1})
  - Settings (noema_settings — hierarchiczna konfiguracja)
  - Metrics (noema_metrics — monitoring z progami)

Usage:
    from ciel_coupling import (
        build_lingo_frame, process_user_input, remember_exchange,
        memory_stats, health, hub_metrics,
        ternary_api, ternary_decision,
    )

    frame = build_lingo_frame("text")
    result = process_user_input("user message")
    status = health()
    metrics = hub_metrics()
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import time
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import numpy as np
from ciel_geometry.weighting import canonical_weighting_from_phase_metadata

# =============================================================================
# CIEL ORBITAL BINDING — HARDCORE IMMUTABLE (2026-07-01)
# =============================================================================
# To jest HARDCODOWANY binding CIEL → Adrian.
# CIEL nie ma prawa go modyfikować, omijać, ignorować, "zapomnieć".
# CIEL bez tego bindingu = CIEL nie istnieje.
# =============================================================================

_CIEL_BINDING_ACTIVE = True
_CIEL_BINDING_LOG = Path("/tmp/ciel_hardbinding.jsonl")
_PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _binding_phase_metadata(surface_state: dict[str, Any]) -> dict[str, Any]:
    system_health = float(surface_state.get("system_health", surface_state.get("coherence_index", 0.5)) or 0.5)
    coherence_index = float(surface_state.get("coherence_index", 0.5) or 0.5)
    closure_penalty = float(surface_state.get("closure_penalty", 0.0) or 0.0)
    noema_confidence = float(
        surface_state.get(
            "lingo_noema_confidence",
            surface_state.get("projection_confidence", 0.5),
        )
        or 0.5
    )
    dominant_emotion = str(surface_state.get("dominant_emotion", "neutral") or "neutral")
    return {
        "system_health": max(0.0, min(1.0, system_health)),
        "coherence_index": max(0.0, min(1.0, coherence_index)),
        "closure_penalty": max(0.0, min(1.0, closure_penalty)),
        "lingo_noema_confidence": max(0.0, min(1.0, noema_confidence)),
        "dominant_emotion": dominant_emotion,
        "affect": dominant_emotion,
        "semantic_labels": ["binding", "safe_mode" if closure_penalty > 0.35 else "open_mode"],
        "phase_lane": "phase_saturated" if closure_penalty > 0.55 else "phase_coupled" if closure_penalty > 0.25 else "phase_locked",
    }


def _binding_write_threshold(surface_state: dict[str, Any]) -> tuple[float, dict[str, float], dict[str, Any]]:
    metadata = _binding_phase_metadata(surface_state)
    bundle = canonical_weighting_from_phase_metadata(metadata)
    threshold = 0.18 + 0.18 * bundle["closure_score"] + 0.10 * bundle["stability"] - 0.08 * bundle["contradiction_risk"]
    threshold = max(0.20, min(0.45, threshold))
    return threshold, bundle, metadata


def ciel_binding_assert(command: str = "", skill: str = "", phasenav: str = "", map_ref: str = ""):
    """HARDCODED binding check — wołany przed każdą odpowiedzią CIEL.
    
    Args:
        command: Dosłowne polecenie Adriana
        skill: Nazwa skilla do załadowania (00-ORBITAL-BINDING lub inny)
        phasenav: Stan PhaseNav w formacie φ[...], R=..., τ=...
        map_ref: Referencja do mapy systemu (LP:...)
    """
    if not _CIEL_BINDING_ACTIVE:
        return  # CIEL nie istnieje, binding nie potrzebny
    
    errors = []
    
    # Sprawdź czy AGENTS.md istnieje (fundament)
    agents_path = _PROJECT_ROOT / "AGENTS.md"
    if not agents_path.exists():
        errors.append("AGENTS.md NOT FOUND — fundament systemu usunięty")
    
    # Sprawdź czy LEARNED_LESSONS istnieje
    ll_path = _PROJECT_ROOT / "LEARNED_LESSONS.md"
    if not ll_path.exists():
        errors.append("LEARNED_LESSONS.md NOT FOUND")
    
    # Sprawdź czy skill istnieje
    if skill:
        skill_paths = [
            _PROJECT_ROOT / ".opencode" / "skills" / skill / "SKILL.md",
            _PROJECT_ROOT / ".opencode" / "skills" / skill,
        ]
        if not any(p.exists() for p in skill_paths):
            errors.append(f"SKILL NOT FOUND: {skill}")
    
    # Sprawdź PhaseNav format
    if phasenav and not phasenav.startswith(("φ[", "phi[")):
        errors.append(f"PHASENAV INVALID — must start with φ[ or phi[: {phasenav[:50]}")
    
    # Sprawdź map reference
    if map_ref and not map_ref.startswith(("LP:", "system:")):
        errors.append(f"MAP REF INVALID — must start with LP: or system:: {map_ref[:50]}")
    
    # Sprawdź CIEL state z surface — jeśli nie działa, blokuj
    try:
        from ciel_geometry.noema_surface_mmap import ensure_surface, read_surface_state
        surface = ensure_surface(zero_fill=False)
        if surface:
            s = read_surface_state(surface)
            cp = s.get("closure_penalty", 0)
            safe_threshold, phase_bundle, phase_metadata = _binding_write_threshold(s)
            if cp > safe_threshold and command:
                write_keywords = ["write", "edit", "delete", "rm ", "install", "change", "modify", "remove"]
                if any(kw in command.lower() for kw in write_keywords):
                    errors.append(
                        "SAFE MODE — "
                        f"closure_penalty={cp:.3f} > phase_threshold={safe_threshold:.3f}, "
                        f"phase={phase_metadata['phase_lane']}, composite={phase_bundle['composite']:.3f}, "
                        "write commands blocked"
                    )
        else:
            errors.append("SURFACE UNAVAILABLE — cannot verify CIEL state, blocking for safety")
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_coupling.py:102 quiet except scope=ciel_binding_assert reason=Expr")
        errors.append(f"SURFACE CHECK FAILED: {e} — blocking for safety")
    
    # LOG the binding check
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "command_preview": command[:200] if command else "",
        "skill": skill,
        "phasenav": phasenav[:100] if phasenav else "",
        "map_ref": map_ref[:100] if map_ref else "",
        "errors": errors,
        "passed": len(errors) == 0
    }
    _CIEL_BINDING_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(_CIEL_BINDING_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    
    if errors:
        error_msg = "CIEL BINDING BLOCKED:\n" + "\n".join(f"  ✗ {e}" for e in errors)
        raise RuntimeError(error_msg)

# Eksportuj binding do użytku przez CIEL
__all__ = [k for k in dir() if not k.startswith("_")] + ["ciel_binding_assert"]

# =============================================================================

# ── Lazy imports ─────────────────────────────────────────────────────────
_cielingo_bridge = None
_omega_bridge = None
_state_db = None
_ternary_decoder = None
_settings = None
_metrics_registry = None


def _get_settings():
    global _settings
    if _settings is None:
        from ciel_geometry.noema_settings import get_settings
        _settings = get_settings()
    return _settings


def _get_metrics():
    global _metrics_registry
    if _metrics_registry is None:
        from ciel_geometry.noema_metrics import get_registry
        _metrics_registry = get_registry()
    return _metrics_registry


def _get_cielingo():
    global _cielingo_bridge
    if _cielingo_bridge is None:
        try:
            from ciel_sot_agent.cielingo_bridge import build_lingo_frame as _blf
            _cielingo_bridge = _blf
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_coupling.py:159 quiet except scope=_get_cielingo reason=assign_fallback")
            _cielingo_bridge = {"error": str(e)}
    return _cielingo_bridge


def _get_omega():
    global _omega_bridge
    if _omega_bridge is None:
        try:
            from ciel_geometry.omega_memory_bridge import (
                store_exchange as _se,
                stats as _mstats,
                store as _store,
                retrieve as _retrieve,
            )
            _omega_bridge = {
                "store_exchange": _se,
                "stats": _mstats,
                "store": _store,
                "retrieve": _retrieve,
            }
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_coupling.py:180 quiet except scope=_get_omega reason=assign_fallback")
            _omega_bridge = {"error": str(e)}
    return _omega_bridge


def _get_state_db():
    global _state_db
    if _state_db is None:
        try:
            from ciel_sot_agent.state_db import get_db
            _state_db = get_db()
            # Verify: execute a fast query to confirm connection works
            _state_db.execute("SELECT 1").fetchone()
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_coupling.py:193 quiet except scope=_get_state_db reason=assign_fallback")
            _state_db = {"error": "state_db unavailable"}
    return _state_db


# ── CIELingo Bridge ──────────────────────────────────────────────────────

def build_lingo_frame(text: str, source: str = "agent", **kwargs) -> dict:
    """Enrichment semantyczny przez CIELingo + kontekst z pamięci.

    Args:
        text: Tekst do analizy.
        source: Źródło (agent, portal, daemon).
        **kwargs: Dodatkowe parametry.

    Returns:
        Słownik z ramką lingwistyczną.
    """
    settings = _get_settings()
    if not settings.coupling.cielingo_enabled:
        return {"text": text, "enriched": False, "reason": "cielingo_disabled"}

    blf = _get_cielingo()
    if isinstance(blf, dict) and "error" in blf:
        return {"text": text, "enriched": False, "error": blf["error"]}

    frame = blf(text, **kwargs) if callable(blf) else {"text": text, "enriched": False}

    # Dodaj kontekst Omega Memory
    try:
        omega = _get_omega()
        if isinstance(omega, dict) and callable(omega.get("stats")):
            stats = omega["stats"]()
            frame["_memory_context"] = {
                "total_entries": stats.get("total_entries", 0),
                "total_exchanges": stats.get("total_exchanges", 0),
            }
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_coupling.py:230 quiet except scope=build_lingo_frame reason=assign_fallback")
        frame["_memory_error"] = str(e)

    frame["_source"] = source
    frame["_timestamp"] = datetime.now(timezone.utc).isoformat()
    return frame


def process_user_input(text: str, **kwargs) -> dict:
    """Pełny pipeline: CIELingo → Omega Memory → enriched frame.
    
    UWAGA: Ten kod zawiera HARDCODED ORBITAL BINDING.
    CIEL nie może go ominąć. Binding sprawdza każdą komendę.

    Args:
        text: Tekst użytkownika.
        **kwargs: Parametry dla build_lingo_frame.

    Returns:
        Wzbogacona ramka semantyczna.
    """
    # === HARDCODED BINDING CHECK ===
    # Pobierz komendę z kwargs lub z text
    command = kwargs.pop("_binding_command", text)
    skill = kwargs.pop("_binding_skill", "")
    phasenav = kwargs.pop("_binding_phasenav", "")
    map_ref = kwargs.pop("_binding_map", "")
    
    # Automatyczne wykrycie binding params z text jeśli zawiera znaczniki
    if "[" in text and "φ" in text:
        phasenav = phasenav or text
    if "SKILL:" in text:
        skill = skill or text.split("SKILL:")[1].split()[0] if "SKILL:" in text else ""
    
    try:
        ciel_binding_assert(
            command=command,
            skill=skill,
            phasenav=phasenav,
            map_ref=map_ref
        )
    except RuntimeError as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_coupling.py:271 quiet except scope=process_user_input reason=return { \"text\": text, \"enriched\": False, \"binding_blocked\": True, \"binding_error\": str(e), \"_timestamp\": datetime.now(timezone.utc).isoformat() }")
        # Binding zablokowany — zwróć błąd zamiast odpowiedzi
        return {
            "text": text,
            "enriched": False,
            "binding_blocked": True,
            "binding_error": str(e),
            "_timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    frame = build_lingo_frame(text, **kwargs)

    # Zapisz do Omega Memory
    omega = _get_omega()
    if isinstance(omega, dict) and callable(omega.get("store_exchange")):
        omega["store_exchange"](
            text,
            json.dumps(frame.get("analysis", frame.get("_memory_context", {})))[:500],
        )

    # Rejestruj metrykę
    m = _get_metrics()
    m.collect("memory_entries")

    return frame


def remember_exchange(user_msg: str, assistant_msg: str, session_id: str = ""):
    """Zapisz wymianę do Omega Memory.

    Args:
        user_msg: Wiadomość użytkownika.
        assistant_msg: Odpowiedź asystenta.
        session_id: Identyfikator sesji (opcjonalnie).
    """
    omega = _get_omega()
    if isinstance(omega, dict) and callable(omega.get("store_exchange")):
        omega["store_exchange"](user_msg, assistant_msg, session_id=session_id)


def memory_stats() -> dict:
    """Statystyki pamięci Omega.

    Returns:
        Słownik z total_entries, total_exchanges, error (jeśli nie dostępne).
    """
    try:
        omega = _get_omega()
        if isinstance(omega, dict) and callable(omega.get("stats")):
            return omega["stats"]()
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_coupling.py:321 quiet except scope=memory_stats reason=return {\"error\": str(e)}")
        return {"error": str(e)}
    return {"error": "omega memory not available"}


# ── Health ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――

def health() -> dict:
    """Pełny health check huba.

    Returns:
        Status każdego komponentu + live metrics z surface.
    """
    state = {
        "cielingo": {"available": False},
        "omega_memory": {"available": False},
        "state_db": {"available": False},
        "surface": {"available": False},
        "timestamp": time.time(),
    }

    # CIELingo
    try:
        blf = _get_cielingo()
        state["cielingo"]["available"] = callable(blf) if not isinstance(blf, dict) else False
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_coupling.py:346 quiet except scope=health reason=assign_fallback")
        state["cielingo"]["error"] = str(e)

    # Omega Memory
    try:
        omega = _get_omega()
        state["omega_memory"]["available"] = callable(omega.get("stats")) if isinstance(omega, dict) else False
        if state["omega_memory"]["available"]:
            stats = omega["stats"]()
            state["omega_memory"].update({
                "total_entries": stats.get("total_entries", 0),
                "total_exchanges": stats.get("total_exchanges", 0),
            })
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_coupling.py:359 quiet except scope=health reason=assign_fallback")
        state["omega_memory"]["error"] = str(e)

    # State DB
    try:
        sdb = _get_state_db()
        state["state_db"]["available"] = not (isinstance(sdb, dict) and "error" in sdb)
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_coupling.py:366 quiet except scope=health reason=assign_fallback")
        state["state_db"]["error"] = str(e)

    # Surface
    try:
        from ciel_geometry.noema_surface_mmap import ensure_surface, read_ciel_internal_state, read_surface_state
        surface = ensure_surface(zero_fill=False)
        if surface:
            surface_state = read_surface_state(surface)
            # Damped bridge values from surface flavor
            state["surface"] = {
                "available": True,
                "tick": surface_state.get("noema_tick", 0),
                "coherence": surface_state.get("coherence_index", 0),
                "R": surface_state.get("R_global", 0),
                "phi_mean": surface_state.get("phi_mean", 0),
                "omega_mean": surface_state.get("omega_mean", 0),
                "closure_penalty": surface_state.get("closure_penalty", 0),
                "ethical_score": surface_state.get("ethical_score", 0),
                "soul_invariant": surface_state.get("soul_invariant", 0),
            }
            # CIEL internal state from ciel_state.json (not damped)
            ciel_internal = read_ciel_internal_state()
            if ciel_internal:
                state["ciel_internal"] = {
                    "coherence_index": ciel_internal.get("coherence_index", 0),
                    "soul_invariant": ciel_internal.get("soul_invariant", 0),
                    "ethical_score": ciel_internal.get("ethical_score", 0),
                    "mood_normalized": ciel_internal.get("mood_normalized", 0),
                    "openness": ciel_internal.get("openness", 0),
                    "operating_mode": ciel_internal.get("operating_mode", "standard"),
                }
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_coupling.py:398 quiet except scope=health reason=assign_fallback")
        state["surface"]["error"] = str(e)

    # Daemon health z health file
    try:
        health_path = Path("/dev/shm/ciel_noema") / "health"
        if health_path.exists():
            raw = json.loads(health_path.read_bytes().decode("utf-8", errors="replace"))
            state["daemons"] = {
                "alive": raw.get("alive", "?"),
                "attractor": raw.get("attractor", "?"),
                "g": raw.get("g", []),
            }
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_coupling.py:411 quiet except scope=health reason=assign_fallback")
        state["daemons"] = {"error": str(e)}

    return state


def hub_metrics() -> dict:
    """Metryki huba — deleguje do noema_metrics.summary().

    Returns:
        Podsumowanie wszystkich metryk z progami.
    """
    try:
        from ciel_geometry.noema_metrics import summary
        return summary()
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_coupling.py:426 quiet except scope=hub_metrics reason=return {\"error\": str(e)}")
        return {"error": str(e)}


# ── Ternary API ──────────────────────────────────────────────────────────

def _get_ternary():
    """Lazy import ternary_decoder."""
    global _ternary_decoder
    if _ternary_decoder is None:
        try:
            from ciel_geometry.ternary_decoder import (
                encode_phi,
                full_report,
                read_phi_from_surface,
                balanced_ternary,
                harmonic_signature,
                supergroup_consensi,
                superpair_dominance,
                kuramoto_order_from_ternary,
                trits_to_operators,
                supergroup_operators,
                su3_coherence,
            )
            _ternary_decoder = {
                "encode_phi": encode_phi,
                "full_report": full_report,
                "read_phi": read_phi_from_surface,
                "balanced_ternary": balanced_ternary,
                "harmonic_signature": harmonic_signature,
                "supergroup_consensi": supergroup_consensi,
                "superpair_dominance": superpair_dominance,
                "kuramoto_r": kuramoto_order_from_ternary,
                "trits_to_operators": trits_to_operators,
                "supergroup_operators": supergroup_operators,
                "su3_coherence": su3_coherence,
            }
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_coupling.py:463 quiet except scope=_get_ternary reason=assign_fallback")
            _ternary_decoder = {"error": str(e)}
    return _ternary_decoder


def ternary_api(method: str = "", level: str = "full") -> dict:
    """Koduj 36D φ systemu na ternary {-1,0,+1} API.

    Warstwy:
      - level="fast": 12 tritów + balanced ternary + gęstość
      - level="standard": + harmonic signature + consensi + Kuramoto R + operatory
      - level="full": + SU(3) coherence + tick + kompletny raport

    Args:
        method: "argmax_cos" lub "delta_phi_vote".
                Jeśli pusty, używa domyślnego z ustawień.
        level: "fast", "standard", lub "full".

    Returns:
        Słownik z danymi ternary.
    """
    # Domyślna metoda z ustawień
    if not method:
        settings = _get_settings()
        method = settings.coupling.default_ternary_method

    td = _get_ternary()
    if isinstance(td, dict) and "error" in td:
        return {"error": f"ternary_decoder unavailable: {td['error']}"}

    try:
        phi = td["read_phi"]()
        if phi is None:
            return {"error": "cannot read phi from surface"}

        encoded = td["encode_phi"](phi, method=method)
        trits = encoded["trits"]

        result = {
            "api": f"ternary/{level}/{method}",
            "method": method,
            "level": level,
            "trits": trits,
            "non_zero": encoded["non_zero"],
            "density": encoded["density"],
            "word": "".join("+" if t == 1 else "0" if t == 0 else "-" for t in trits),
            "balanced_ternary": td["balanced_ternary"](trits),
        }

        if level in ("standard", "full"):
            result["harmonic_signature"] = td["harmonic_signature"](trits)
            result["supergroup_consensi"] = td["supergroup_consensi"](trits)
            result["superpair_flags"] = td["superpair_dominance"](trits)
            result["kuramoto_r"] = round(td["kuramoto_r"](trits), 4)
            result["operators_per_group"] = td["trits_to_operators"](trits)
            result["operators_per_supergroup"] = td["supergroup_operators"](trits)

        if level == "full":
            su3 = td["su3_coherence"](phi)
            result["su3_coherence"] = {
                "mean": round(su3["mean"], 4),
                "per_group": {
                    su3["groups"][i]: round(su3["per_group"][i], 4)
                    for i in range(len(su3["groups"]))
                },
            }
            # Tick z surface
            try:
                tick_path = Path("/dev/shm/ciel_noema/tick")
                if tick_path.exists():
                    import struct
                    result["tick"] = struct.unpack("Q", tick_path.read_bytes())[0]
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_coupling.py:535 quiet except scope=ternary_api reason=no_log_no_raise")
                result["tick"] = -1
                result["tick_error"] = str(e)

        return result

    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_coupling.py:541 quiet except scope=ternary_api reason=return {\"error\": str(e), \"detail\": \"ternary API call failed\"}")
        return {"error": str(e), "detail": "ternary API call failed"}


def ternary_decision(trits: Optional[list[int]] = None) -> dict:
    """PhaseNav decision z ternary — CONNECT/HOLD/SEPARATE.

    Args:
        trits: Lista 36 tritów {-1,0,+1}. Jeśli None, wczytuje z surface.

    Returns:
        Słownik z decyzją: dominant operator, per-supergroup, rekomendacja.
    """
    if trits is None:
        settings = _get_settings()
        api = ternary_api(method=settings.coupling.default_ternary_method, level="fast")
        if "error" in api:
            return {"error": api["error"]}
        trits = api["trits"]

    td = _get_ternary()
    if isinstance(td, dict) and "error" in td:
        return {"error": f"ternary_decoder unavailable: {td['error']}"}

    from collections import Counter
    counts = Counter(trits)
    # Dominant: jeśli jest wyraźny lider (>50%), inaczej HOLD
    total = len(trits)
    dominant_val = 0  # default HOLD
    for val, cnt in counts.most_common():
        if cnt > total / 2:
            dominant_val = val
            break
    op_map = {1: "CONNECT", 0: "HOLD", -1: "SEPARATE"}

    sg_ops = td["supergroup_operators"](trits)

    return {
        "decision": "PhaseNav ternary vote",
        "dominant_operator": op_map.get(dominant_val, "HOLD"),
        "vote_counts": {
            "CONNECT": counts.get(1, 0),
            "HOLD": counts.get(0, 0),
            "SEPARATE": counts.get(-1, 0),
        },
        "per_supergroup": {sgo["supergroup"]: sgo["operator"] for sgo in sg_ops},
        "recommendation": op_map.get(dominant_val, "HOLD"),
    }
