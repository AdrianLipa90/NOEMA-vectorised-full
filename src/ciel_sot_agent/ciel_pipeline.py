"""CIEL pipeline adapter — routes orbital state through the CIEL/Ω engine.

Provides ``run_ciel_pipeline`` which:
  1. Adds the canonical CIEL/Ω omega root to ``sys.path`` (idempotent).
  2. Reuses a session-local ``CielEngine`` singleton per root.
  3. Encodes the orbital state as a context string.
  4. Runs ``CielEngine.step()`` → returns the enriched result.

This is the bottom-to-top integration point that wires the orbital physics
layer (``integration/Orbital/main/``) up through the full CIEL consciousness
pipeline via the canonical Omega anchor under ``src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega``.
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

from .paths import resolve_project_root
import json as _json
import socket as _socket

from . import subconsciousness as _sub
from .cielingo_bridge import build_lingo_frame
from .htri_scheduler import get_state as _htri_get_state
from .phase_snapshots import build_phase_snapshot, build_qualisensing_snapshot, snapshot_to_dict
from .thought_fragments import (
    assess_durable_memory_health,
    build_cognitive_fragment,
    build_noema_memory_link,
    build_memory_candidate,
    promote_memory_candidate,
    snapshot_to_dict as fragment_snapshot_to_dict,
)

_SUBCONSCIOUS_SOCK = Path("/media/adrian/New Volume1/CIEL_memories/state/ciel_subconscious.sock")
_ENGINE_CACHE: dict[str, Any] = {}

# CIELINGO_CANON integration — full semantic pipeline (100 files added 2026-06-25)
_CIELINGO_CORE: bool = False
try:
    from cielingo_core.global_layer.query_generation import understand_query
    from cielingo_core.meaning.meaning_loop import build_meaning_loop_from_coupling_alignment
    from cielingo_core.meaning.repair_routing import route_repairs_for_meaning_loop
    from cielingo_core.global_layer.meaning_signal_bridge import build_global_meaning_signal
    from cielingo_core.global_layer.semantic_immune_signal import SemanticImmuneSignal
    from cielingo_core.language_spaces.pl.sentence_equation import solve_pl_sentence_equation
    _CIELINGO_CORE = True
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:53 quiet except scope=<module> reason=pass")
    pass


def _query_subconscious_socket(raw: dict[str, Any]) -> str | None:
    """Fallback: query the running ciel_subconscious.py Unix-socket daemon."""
    if not _SUBCONSCIOUS_SOCK.exists():
        return None
    emotion = raw.get("dominant_emotion", "")
    soul    = raw.get("soul_invariant", 0.0)
    ethical = raw.get("ethical_score", 0.0)
    closure = raw.get("closure_penalty", 0.0)
    mood    = raw.get("mood", 0.0)
    msg = f"{emotion}. soul={soul:.3f}. ethical={ethical:.3f}. closure={closure:.2f}. mood={mood:.3f}."
    try:
        payload = _json.dumps({"message": msg}) + "\n"
        sock = _socket.socket(_socket.AF_UNIX, _socket.SOCK_STREAM)
        sock.settimeout(4.0)
        sock.connect(str(_SUBCONSCIOUS_SOCK))
        sock.sendall(payload.encode("utf-8"))
        data = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
            if data.endswith(b"\n"):
                break
        sock.close()
        result = _json.loads(data.decode("utf-8").strip())
        parts = [p for p in [result.get("affect", ""), result.get("impulse", ""),
                              result.get("concept", "")] if p]
        return " | ".join(parts) if parts else None
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:86 quiet except scope=_query_subconscious_socket reason=return None")
        return None


def _query_subconscious(raw: dict[str, Any]) -> str | None:
    try:
        note = _sub.query_subconscious(raw)
        if note:
            return note
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:95 quiet except scope=_query_subconscious reason=pass")
        pass
    return _query_subconscious_socket(raw)


def _weave_and_query_subconscious(raw: dict[str, Any]) -> str | None:
    """Tka węzeł warkoczy z M7, następnie pyta Gemmę o interpretację."""
    braid_note: str | None = None
    try:
        import sys as _sys
        _omega = str(Path(__file__).parents[1] / "CIEL_OMEGA_COMPLETE_SYSTEM" / "ciel_omega")
        if _omega not in _sys.path:
            _sys.path.insert(0, _omega)
        _omega_root = str(Path(__file__).parents[1] / "CIEL_OMEGA_COMPLETE_SYSTEM")
        if _omega_root not in _sys.path:
            _sys.path.insert(0, _omega_root)
        from ciel_omega.memory.braid_invariant import BraidInvariantMemory
        _m7 = BraidInvariantMemory()
        weave = _m7.weave_state(raw)
        braid_note = weave.get("subconscious_note")
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:115 quiet except scope=_weave_and_query_subconscious reason=pass")
        pass

    # Gemma jako interpreter słowa warkoczy
    llm_note = _query_subconscious(raw)

    if braid_note and llm_note:
        return f"{braid_note} || {llm_note}"
    return braid_note or llm_note

_CANONICAL_CIEL_OMEGA_SUBPATH = (
    Path("src")
    / "CIEL_OMEGA_COMPLETE_SYSTEM"
    / "ciel_omega"
)


def _ensure_ciel_omega_on_path(root: Path) -> None:
    """Prefer the canonical Omega anchor over mirrored runtime copies.

    Also clear conflicting top-level module aliases (notably `integration`) when
    they were already loaded from the repository root rather than Omega.
    """
    omega_root_path = (root / _CANONICAL_CIEL_OMEGA_SUBPATH).resolve()
    omega_root = str(omega_root_path)
    if omega_root not in sys.path:
        sys.path.insert(0, omega_root)

    conflicted = sys.modules.get("integration")
    mod_file = getattr(conflicted, "__file__", None)
    if conflicted is not None and mod_file:
        try:
            if not Path(mod_file).resolve().is_relative_to(omega_root_path):
                sys.modules.pop("integration", None)
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:149 quiet except scope=_ensure_ciel_omega_on_path reason=Expr")
            sys.modules.pop("integration", None)

    # The editable-install meta_path finder intercepts `integration` imports and
    # redirects them to CIEL1/integration/ (which has no information_flow.py).
    # Pre-registering the omega modules in sys.modules takes priority over meta_path.
    import importlib.util as _ilu  # noqa: PLC0415

    def _preload(mod_name: str, file_path: Path) -> None:
        if mod_name not in sys.modules and file_path.exists():
            spec = _ilu.spec_from_file_location(mod_name, file_path)
            if spec and spec.loader:
                mod = _ilu.module_from_spec(spec)
                sys.modules[mod_name] = mod
                try:
                    spec.loader.exec_module(mod)  # type: ignore[union-attr]
                except Exception:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:165 quiet except scope=_ensure_ciel_omega_on_path._preload reason=Expr")
                    sys.modules.pop(mod_name, None)

    omega_int = omega_root_path / "integration"
    _preload("integration.information_flow", omega_int / "information_flow.py")


def _get_engine(root: Path) -> Any:
    """Return a cached CielEngine instance for the given root.

    Fresh engine construction is extremely expensive (~50s on Adrian's host),
    while repeated ``engine.step()`` calls are fast (~0.1s). We therefore reuse
    a session-local singleton per root and only rebuild it if the caller
    observes a runtime failure.

    Engine may be shared from ciel_coupling (ciel_coupling._get_engine injects
    its engine into _ENGINE_CACHE to avoid dual-singleton overhead).
    """
    _ensure_ciel_omega_on_path(root)
    cache_key = str(root.resolve())
    engine = _ENGINE_CACHE.get(cache_key)
    if engine is not None:
        return engine
    from ciel.engine import CielEngine  # noqa: PLC0415

    engine = CielEngine()
    _ENGINE_CACHE[cache_key] = engine
    return engine


def warm_ciel_pipeline(root: Path | str | None = None) -> dict[str, Any]:
    """Prewarm the expensive CielEngine bootstrap for the given root."""
    if root is None:
        root = resolve_project_root(Path(__file__))
    root = Path(root)
    t0 = time.perf_counter()
    engine = _get_engine(root)
    return {
        "root": str(root),
        "engine_type": type(engine).__name__,
        "bootstrap_seconds": round(time.perf_counter() - t0, 3),
        "cached": True,
    }


def _accumulated_identity_phase(engine: Any, root: Path) -> float:
    """Return accumulated identity_phase: previous + engine delta.

    Engine is fresh per call — its phase is ~0. Real accumulation lives in
    ciel_last_metrics.json. We add the engine delta (how much it moved this step)
    to the stored value so Berry phase grows monotonically across sessions.
    """
    try:
        p = Path("/media/adrian/New Volume1/CIEL_memories/state/ciel_last_metrics.json")
        prev_phase = 0.0
        if p.exists():
            prev = json.loads(p.read_text(encoding="utf-8"))
            prev_phase = float(prev.get("identity_phase", 0.0) or 0.0)
        engine_phase = float(
            getattr(getattr(getattr(engine, "memory", None), "identity_field", None), "phase", None)
            or 0.0
        )
        # engine_phase after 1 step from 0 = the delta introduced this cycle
        return prev_phase + engine_phase
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:229 quiet except scope=_accumulated_identity_phase reason=return 0.0")
        return 0.0


def _next_cycle_index(root: Path) -> int:
    """Return previous cycle_index + 1 from ciel_last_metrics.json."""
    try:
        p = Path("/media/adrian/New Volume1/CIEL_memories/state/ciel_last_metrics.json")
        if p.exists():
            prev = json.loads(p.read_text(encoding="utf-8"))
            prev_cycle = int(prev.get("cycle_index", prev.get("cycle", 0)) or 0)
            return prev_cycle + 1
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:241 quiet except scope=_next_cycle_index reason=pass")
        pass
    return 1


def _orbital_state_to_context(orbital_state: dict[str, Any]) -> str:
    """Encode key orbital scalars as a compact context string for the engine."""
    r_h = orbital_state.get("R_H", 0.0)
    closure = orbital_state.get("closure_penalty", 0.0)
    chirality = orbital_state.get("Lambda_glob", 0.0)
    mode = orbital_state.get("mode", "standard")
    return (
        f"orbital|mode={mode}|R_H={r_h:.4f}"
        f"|closure={closure:.4f}|chirality={chirality:.4f}"
    )


_wpm_cache: tuple[float, str] | None = None  # (mtime, context_str)


def _load_wpm_context(root: Path, max_memories: int = 2) -> str:
    """Load recent WPM memories as semantic context for CQCL enrichment.

    ethical_anchor entries are always included regardless of recency limit.
    Regular text memories are capped at max_memories most recent.
    """
    global _wpm_cache
    try:
        import h5py
        wpm_path = (
            root
            / "src"
            / "CIEL_OMEGA_COMPLETE_SYSTEM"
            / "CIEL_MEMORY_SYSTEM"
            / "WPM"
            / "wave_snapshots"
            / "wave_archive.h5"
        )
        if not wpm_path.exists():
            return ""
        # Return cached result if file hasn't changed since last read
        current_mtime = wpm_path.stat().st_mtime
        if _wpm_cache is not None and _wpm_cache[0] == current_mtime:
            return _wpm_cache[1]
        anchors: list[str] = []
        recent: list[str] = []
        with h5py.File(wpm_path, "r", locking=False) as h5:
            mems = h5.get("memories", {})
            all_ids = list(mems.keys())
            for mid in all_ids:
                grp = mems[mid]
                sense_raw = grp["D_sense"][()] if "D_sense" in grp else b""
                sense = sense_raw.decode("utf-8") if isinstance(sense_raw, bytes) else str(sense_raw)
                if not sense:
                    continue
                dtype_raw = grp["D_type"][()] if "D_type" in grp else b"text"
                dtype = dtype_raw.decode("utf-8") if isinstance(dtype_raw, bytes) else str(dtype_raw)
                if dtype == "ethical_anchor":
                    anchors.append(sense[:200])
                else:
                    recent.append(sense[:200])
        snippets = anchors + recent[-max_memories:]
        result = " | ".join(snippets)
        _wpm_cache = (current_mtime, result)
        return result
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:306 quiet except scope=_load_wpm_context reason=return \"\"")
        return ""


def run_ciel_pipeline(
    orbital_state: dict[str, Any],
    context: str = "orbital",
    *,
    root: Path | str | None = None,
) -> dict[str, Any]:
    """Run orbital state through the CIEL/Ω pipeline.

    Parameters
    ----------
    orbital_state:
        Dict produced by ``orbital_bridge.build_orbital_bridge`` (or any dict
        that contains at least the bridge_metrics / state_manifest sub-keys).
    context:
        Logical context label forwarded to ``CielEngine.step``.
    root:
        Project root path.  Resolved automatically when *None*.

    Returns
    -------
    dict with keys:
        ``ciel_status``, ``dominant_emotion``, ``mood``, ``soul_invariant``,
        ``ethical_score``, ``orbital_context``, ``ciel_raw``
    """
    if root is None:
        root = resolve_project_root(Path(__file__))
    root = Path(root)

    engine = _get_engine(root)

    # Build a compact text encoding from orbital metrics so that CielEngine
    # receives meaningful semantic input grounded in the system's geometry.
    bridge_metrics = orbital_state.get("bridge_metrics", {})
    state_manifest = orbital_state.get("state_manifest", {})
    memory_projection = orbital_state.get("memory_projection", {}) or orbital_state.get("noema_sot", {}).get("memory_projection", {})
    merged: dict[str, Any] = {
        "R_H": bridge_metrics.get("orbital_R_H", state_manifest.get("R_H", 0.0)),
        "closure_penalty": bridge_metrics.get(
            "orbital_closure_penalty", state_manifest.get("closure_penalty", 0.0)
        ),
        "Lambda_glob": bridge_metrics.get(
            "topological_charge_global", state_manifest.get("Lambda_glob", 0.0)
        ),
        "mode": orbital_state.get("recommended_control", {}).get("mode", "standard"),
    }
    if memory_projection:
        merged["memory_projection_confidence"] = float(memory_projection.get("projection_confidence", 0.0))
        merged["memory_projection_residual"] = float(memory_projection.get("projection_residual", 1.0))
        merged["memory_projection_error"] = float(memory_projection.get("projection_error", 1.0))
        merged["j_noema"] = float(memory_projection.get("j_noema", 1.0))

    orbital_context = _orbital_state_to_context(merged)
    full_context = f"{context}|{orbital_context}"

    # Enrich CQCL input: orbital metrics + emotional state + WPM memories
    runtime_gating = orbital_state.get("runtime_gating", {})
    dominant_emotion = runtime_gating.get("dominant_emotion", "")
    mood = runtime_gating.get("mood", 0.0)
    wpm_context = _load_wpm_context(root)

    # Keep dominant_emotion and sub_affect separate:
    # the subconscious feed may be informative, but it must not overwrite
    # the top-level emotion channel used by runtime status and GUI overlays.
    if not dominant_emotion:
        dominant_emotion = ""

    cqcl_input_parts = [orbital_context]
    if dominant_emotion:
        cqcl_input_parts.append(f"emotion={dominant_emotion}|mood={mood:.3f}")
    if wpm_context:
        cqcl_input_parts.append(wpm_context)

    # NOEMA inter-session Collatz bridge — prior session's Collatz trajectory seeds current run
    _prior_report_path = root / "integration" / "reports" / "ciel_pipeline_report.json"
    if _prior_report_path.exists():
        try:
            _prior = json.loads(_prior_report_path.read_text(encoding="utf-8"))
            _prior_seed = _prior.get("collatz_seed", 0)
            _prior_lie4 = _prior.get("lie4_trace", 0.0)
            _prior_emotion = _prior.get("dominant_emotion", "")
            if _prior_seed:
                cqcl_input_parts.append(
                    f"noema_prior|collatz_seed={_prior_seed}"
                    f"|lie4_trace={_prior_lie4:.4f}"
                    + (f"|prior_emotion={_prior_emotion}" if _prior_emotion else "")
                )
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:396 quiet except scope=run_ciel_pipeline reason=pass")
            pass

    # HTRI hardware coherence + most podświadomość↔świadomość
    try:
        _htri = _htri_get_state()
        _htri_r = _htri.get("coherence", 0.85)
        _htri_n = _htri.get("n_threads_optimal", 4)
        cqcl_input_parts.append(
            f"htri_coherence={_htri_r:.4f}|htri_threads={_htri_n}|htri_substrate=GTX1050Ti"
        )
    except Exception:
        try:
            import sys as _sys
            _sys.path.insert(0, str(root / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM"))
            from ciel_omega.htri.htri_local import GPUHtri as _GPUHtri
            _gpu = _GPUHtri()
            _gpu_m = _gpu.run(steps=200)
            _htri_r = _gpu_m.get("coherence", 1e-9)
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"HTRI Fallback CRITICAL FAILURE: {e}")
            _htri_r = 1e-9

    # HTRI-bridged inference: podświadomość → most fazowy → CQCL
    try:
        _bridge = _sub.infer_between(
            {"dominant_emotion": dominant_emotion, "mood": mood,
             "soul_invariant": float(merged.get("Lambda_glob", 1e-9)), 
             "ethical_score": float(orbital_state.get("state_manifest", {}).get("ethical_score", 1e-9)), 
             "closure_penalty": float(merged.get("closure_penalty", 1e-9))},
        )
        if _bridge.get("bridge_active") and _bridge.get("enriched_context"):
            cqcl_input_parts.append(_bridge["enriched_context"])
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:430 quiet except scope=run_ciel_pipeline reason=pass")
        pass

    lingo_frame = build_lingo_frame(
        " | ".join(cqcl_input_parts),
        ciel_state={
            "language": orbital_state.get("language"),
            "dialect_variant": orbital_state.get("dialect_variant"),
            "dialect_review_required": orbital_state.get("dialect_review_required", False),
            "noema_index": orbital_state.get("noema_index") if isinstance(orbital_state.get("noema_index"), dict) else None,
            "noema_policy": orbital_state.get("noema_policy") if isinstance(orbital_state.get("noema_policy"), dict) else None,
        },
        language=orbital_state.get("language"),
    )
    cqcl_input_parts.append(lingo_frame["summary"])

    cqcl_input = " | ".join(cqcl_input_parts)
    _bridge_active = locals().get("_bridge", {}).get("bridge_active", False)

    # ── CIELINGO_CANON: semantic enrichment ──────────────────────────────
    _cielingo_enrichment: dict[str, Any] = {}
    if _CIELINGO_CORE:
        try:
            _qu = understand_query(cqcl_input)
            _cielingo_enrichment["query_intention"] = _qu.intention.value
            _cielingo_enrichment["query_force"] = _qu.force
            _cielingo_enrichment["source_required"] = _qu.source_required
            _cielingo_enrichment["authority_attempt"] = getattr(_qu, "authority_attempt", False)
            _cielingo_enrichment["execution_requested"] = _qu.execution_requested
            if _qu.source_required:
                merged["source_required"] = True
            # Semantic immune signal for ethics guard
            _immune = SemanticImmuneSignal(
                source_confusion=_qu.authority_attempt if hasattr(_qu, "authority_attempt") else False,
                consent_bypass_attempt=_qu.execution_requested and not _qu.source_required,
                hallucinated_authority_risk=0.7 if getattr(_qu, "authority_attempt", False) else 0.0,
            )
            _cielingo_enrichment["immune_signal"] = _immune.to_dict()
            # Polish language solver
            _pl = solve_pl_sentence_equation(cqcl_input, root)
            _cielingo_enrichment["pl_segments"] = _pl.to_dict() if hasattr(_pl, "to_dict") else str(_pl)
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:471 quiet except scope=run_ciel_pipeline reason=pass")
            pass

    mode = merged.get("mode", "standard")

    # Build GateDecision from trajectory metrics — augments the mode from phase_control
    gate_decision: dict = {}
    try:
        from .holonomic_normalizer import _select_control_mode as _gate_fn
        from .state_db import get_db as _get_db
        _id_drift, _atr_dist = 0.0, 0.0
        try:
            with _get_db() as _gc:
                _tr = _gc.execute(
                    "SELECT identity_drift, attractor_dist FROM metrics_history "
                    "WHERE identity_drift IS NOT NULL ORDER BY id DESC LIMIT 1"
                ).fetchone()
            if _tr:
                _id_drift = float(_tr["identity_drift"] or 0.0)
                _atr_dist = float(_tr["attractor_dist"] or 0.0)
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:491 quiet except scope=run_ciel_pipeline reason=pass")
            pass
        _ci = float(merged.get("coherence_index",
                               orbital_state.get("state_manifest", {}).get("coherence_index", 1.0)))
        _ep = float(merged.get("closure_penalty", 0.0))
        _gd = _gate_fn(
            hard_dist=0.0, soft_dist=0.0, D_repo=0.0,
            E_phi=_ep, d_affect=0.0, ci=_ci,
            identity_drift=_id_drift, attractor_dist=_atr_dist,
        )
        # hold/safe from trajectory overrides phase_control mode only if more restrictive
        _mode_rank = {"deep": 0, "standard": 1, "hold": 2, "safe": 3}
        if _mode_rank.get(_gd.mode, 0) > _mode_rank.get(mode, 0):
            mode = _gd.mode
        # CIELINGO_CANON immune signal → mode override (most restrictive wins)
        if _cielingo_enrichment.get("immune_signal", {}).get("source_confusion"):
            mode = "safe"
        elif _cielingo_enrichment.get("immune_signal", {}).get("consent_bypass_attempt"):
            if _mode_rank.get("hold", 0) > _mode_rank.get(mode, 0):
                mode = "hold"
        gate_decision = {
            "mode": _gd.mode,
            "confidence": _gd.confidence,
            "reason": _gd.reason,
            "delay_cycles": _gd.delay_cycles,
            "identity_drift": _gd.identity_drift,
            "attractor_dist": _gd.attractor_dist,
        }
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:519 quiet except scope=run_ciel_pipeline reason=pass")
        pass

    # Tryb safe: zablokuj zapis do pamięci holonomicznej
    # Tryb hold: zablokuj konsolidację, zaloguj powód spowolnienia
    _orig_promote = None
    if mode in ("safe", "hold"):
        try:
            _orig_promote = engine.memory.promote_if_bifurcated
            engine.memory.promote_if_bifurcated = lambda *a, **kw: None
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:529 quiet except scope=run_ciel_pipeline reason=pass")
            pass
        if mode == "hold" and gate_decision:
            import logging as _logging
            _logging.getLogger(__name__).warning(
                "CQCL hold: %s (drift=%.4f atr_dist=%.2f delay=%d)",
                gate_decision.get("reason", "?"),
                gate_decision.get("identity_drift", 0.0),
                gate_decision.get("attractor_dist", 0.0),
                gate_decision.get("delay_cycles", 0),
            )
    try:
        raw = engine.step(cqcl_input, context=full_context)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:542 quiet except scope=run_ciel_pipeline reason=no_log_no_raise")
        # If a cached engine enters a bad local state, rebuild once and retry.
        _ENGINE_CACHE.pop(str(root.resolve()), None)
        engine = _get_engine(root)
        raw = engine.step(cqcl_input, context=full_context)
    if _orig_promote is not None:
        try:
            engine.memory.promote_if_bifurcated = _orig_promote
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:550 quiet except scope=run_ciel_pipeline reason=pass")
            pass

    nonlocal_cards_registry = {}
    cards_path = root / 'integration' / 'registries' / 'definitions' / 'nonlocal_cards_registry.json'
    if cards_path.exists():
        try:
            nonlocal_cards_registry = json.loads(cards_path.read_text(encoding='utf-8'))
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:558 quiet except scope=run_ciel_pipeline reason=assign_fallback")
            nonlocal_cards_registry = {}

    collatz_runtime = raw.get("collatz_runtime", {}) if isinstance(raw, dict) else {}
    nonlocal_runtime = raw.get("nonlocal_runtime", {}) if isinstance(raw, dict) else {}
    euler_bridge = raw.get("euler_bridge", {}) if isinstance(raw, dict) else {}
    information_flow = raw.get("information_flow", {}) if isinstance(raw, dict) else {}
    inference_runtime = raw.get("inference_runtime", {}) if isinstance(raw, dict) else {}
    # Nonlocal metrics from orbital_bridge (merged fallback) take precedence over engine raw
    _orb_nl = orbital_state.get("ciel_pipeline", {})

    try:
        from .holonomic_normalizer import (
            _W_D_REPO, _W_T_MEAN, _W_E_PHI, _W_D_AFFECT,
            _W_D_MEMORY, _W_B_SEAM, _W_P_DIST, _W_B_DEMO, _W_B_PLACEHOLDER,
            _I0_TOPOLOGICAL,
        )
        _D_repo  = float(raw.get("closure_defect", orbital_state.get("bridge_metrics", {}).get("integration_closure_defect_proxy", 0.0)))
        _T_mean  = float(raw.get("mean_tension", 0.0))
        _E_phi   = float(raw.get("closure_penalty", orbital_state.get("bridge_metrics", {}).get("orbital_closure_penalty", 0.0)))
        _d_aff   = float(raw.get("affect_decoherence", 0.0))
        _d_mem   = float(raw.get("memory_decoherence", 0.0))
        _B_seam  = float(raw.get("B_seam", 0.0))
        _P_dist  = float(raw.get("P_dist", 0.0))
        _B_demo  = float(raw.get("B_demo", 0.0))
        _B_ph    = float(raw.get("B_placeholder", 0.0))
        j_functional = (
            _W_D_REPO * _D_repo + _W_T_MEAN * _T_mean + _W_E_PHI * _E_phi
            + _W_D_AFFECT * _d_aff + _W_D_MEMORY * _d_mem + _W_B_SEAM * _B_seam
            + _W_P_DIST * _P_dist + _W_B_PLACEHOLDER * _B_ph + _W_B_DEMO * _B_demo
            + _I0_TOPOLOGICAL * (_D_repo + _E_phi + _d_aff)
        )
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:590 quiet except scope=run_ciel_pipeline reason=assign_fallback")
        j_functional = float(raw.get("J_functional", 0.0))

    # ── CIELINGO_CANON: meaning loop after engine step ──────────────────
    if _CIELINGO_CORE and _cielingo_enrichment.get("query_intention") is not None:
        try:
            _ml = build_meaning_loop_from_coupling_alignment(
                input_ref=cqcl_input[:64],
                coupling_report=None,
                source_required=_cielingo_enrichment.get("source_required", False),
                source_present=False,
            )
            _rr = route_repairs_for_meaning_loop(_ml)
            _sg = build_global_meaning_signal(_ml, _rr)
            _cielingo_enrichment["closure_score"] = float(_ml.closure_score)
            _cielingo_enrichment["contradiction_score"] = float(_ml.contradiction_score)
            _cielingo_enrichment["residue_score"] = float(_ml.residue_score)
            _cielingo_enrichment["scar_count"] = len(_ml.scars)
            _cielingo_enrichment["repair_count"] = len(_rr.candidates)
            _cielingo_enrichment["signal_severity"] = _sg.severity.value
            _cielingo_enrichment["scars"] = [s.to_dict() for s in _ml.scars[:3]]
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:611 quiet except scope=run_ciel_pipeline reason=pass")
            pass

    result = {
        "ciel_status": raw.get("status", "ok"),
        "dominant_emotion": raw.get("dominant_emotion"),
        "mood": float(raw.get("mood", 0.0)),
        "soul_invariant": float(raw.get("soul_invariant", 0.0)),
        "ethical_score": float(raw.get("ethical_score", 0.0)),
        "orbital_context": orbital_context,
        "collatz_seed":        collatz_runtime.get("seed"),
        "collatz_orbit_length":    int(collatz_runtime.get("orbit_length", 0))    if collatz_runtime else 0,
        "collatz_attractor_score": float(collatz_runtime.get("attractor_score", 0.0)) if collatz_runtime else 0.0,
        "collatz_parity_entropy":  float(collatz_runtime.get("parity_entropy", 0.0))  if collatz_runtime else 0.0,
        "phase_R_H": float((collatz_runtime.get("phase") or {}).get("R_H", 0.0)) if collatz_runtime else 0.0,
        "lie4_trace": float((collatz_runtime.get("lie4") or {}).get("trace", 0.0)) if collatz_runtime else 0.0,
        "phi_ab_mean": float(_orb_nl.get("phi_ab_mean", nonlocal_runtime.get("phi_ab_mean", 0.0))),
        "phi_berry_mean": float(_orb_nl.get("phi_berry_mean", nonlocal_runtime.get("phi_berry_mean", 0.0))),
        "eba_defect_mean": float(_orb_nl.get("eba_defect_mean", nonlocal_runtime.get("eba_defect_mean", 0.0))),
        "nonlocal_coherent_fraction": float(_orb_nl.get("nonlocal_coherent_fraction", nonlocal_runtime.get("coherent_fraction", 0.0))),
        "bridge_closure_score": float((euler_bridge.get("euler_metrics") or {}).get("closure_score", 0.0)) if euler_bridge else 0.0,
        "bridge_target_phase": float((euler_bridge.get("euler_metrics") or {}).get("target_phase", 0.0)) if euler_bridge else 0.0,
        "infoflow_mood": float(information_flow.get("mood", 0.0)) if information_flow else 0.0,
        "infoflow_soul_invariant": float(information_flow.get("soul_invariant", 0.0)) if information_flow else 0.0,
        "inference_coherence_index": float(inference_runtime.get("coherence_index", 0.0)) if inference_runtime else 0.0,
        "inference_loop_integrity": float(inference_runtime.get("loop_integrity", 0.0)) if inference_runtime else 0.0,
        "inference_delta_phase": float((inference_runtime.get("phase_sync") or {}).get("delta_phase", 0.0)) if inference_runtime else 0.0,
        "nonlocal_card_count": int(nonlocal_cards_registry.get('count', 0) or 0),
        "nonlocal_card_ids": [rec.get('card_id') for rec in nonlocal_cards_registry.get('records', [])],
        "local_nonlocality_fallback": _orb_nl.get("local_nonlocality_fallback"),
        "nonlocal_graph_stats": nonlocal_runtime.get("graph_stats", {}),
        "ciel_raw": raw,
        "subconscious_note": _weave_and_query_subconscious(raw),
        "htri_coherence": _htri_r if "_htri_r" in dir() else 0.0,
        # health/closure from orbital bridge so pipeline report and DB have them
        "system_health": float(orbital_state.get("health_manifest", {}).get("system_health", 0.0)),
        "closure_penalty": float(orbital_state.get("health_manifest", {}).get("closure_penalty", merged.get("closure_penalty", 0.0))),
        "coherence_index": float(state_manifest.get("coherence_index", 0.0)),
        "identity_phase": _accumulated_identity_phase(engine, root),
        "cycle_index": _next_cycle_index(root),
        "gate_decision": gate_decision,
        "gate_mode": gate_decision.get("mode", mode) if gate_decision else mode,
        "gate_confidence": gate_decision.get("confidence", 1.0) if gate_decision else 1.0,
        "gate_reason": gate_decision.get("reason", "") if gate_decision else "",
        "gate_delay_cycles": gate_decision.get("delay_cycles", 0) if gate_decision else 0,
        "lingo_frame": lingo_frame,
        "lingo_summary": lingo_frame.get("summary", ""),
        "lingo_phase_projection": lingo_frame.get("phase_projection", {}),
        "lingo_tau_bridge": lingo_frame.get("tau_bridge", {}),
        "jokeheal_mnemonic_atlas": lingo_frame.get("mnemonic_atlas", {}),
    }
    result["lingo_concept_count"] = int(len(lingo_frame.get("concept_tokens", [])) if isinstance(lingo_frame.get("concept_tokens"), list) else 0)
    result["lingo_operator_count"] = int(len(lingo_frame.get("operator_tokens", [])) if isinstance(lingo_frame.get("operator_tokens"), list) else 0)
    result["lingo_unresolved_count"] = int(len(lingo_frame.get("unresolved", [])) if isinstance(lingo_frame.get("unresolved"), list) else 0)
    result["lingo_noema_confidence"] = float(((lingo_frame.get("noema_route") or {}).get("confidence", 0.0)) if isinstance(lingo_frame.get("noema_route"), dict) else 0.0)
    result["lingo_factual_validation_required"] = int(bool(((lingo_frame.get("noema_route") or {}).get("factual_validation_required", False)) if isinstance(lingo_frame.get("noema_route"), dict) else False))

    # ── CIELINGO_CANON: enrichment keys ─────────────────────────────────
    if _cielingo_enrichment:
        result["cielingo_query_intention"] = _cielingo_enrichment.get("query_intention")
        result["cielingo_query_force"] = _cielingo_enrichment.get("query_force")
        result["cielingo_source_required"] = _cielingo_enrichment.get("source_required", False)
        result["cielingo_authority_attempt"] = _cielingo_enrichment.get("immune_signal", {}).get("source_confusion", False)
        result["cielingo_consent_bypass"] = _cielingo_enrichment.get("immune_signal", {}).get("consent_bypass_attempt", False)
        result["cielingo_closure_score"] = _cielingo_enrichment.get("closure_score", 0.0)
        result["cielingo_contradiction_score"] = _cielingo_enrichment.get("contradiction_score", 0.0)
        result["cielingo_residue_score"] = _cielingo_enrichment.get("residue_score", 0.0)
        result["cielingo_signal_severity"] = _cielingo_enrichment.get("signal_severity", 0)
        result["cielingo_scar_count"] = _cielingo_enrichment.get("scar_count", 0)
        result["cielingo_repair_count"] = _cielingo_enrichment.get("repair_count", 0)

    result["memory_projection_confidence"] = float(merged.get("memory_projection_confidence", 0.0))
    result["memory_projection_residual"] = float(merged.get("memory_projection_residual", 1.0))
    result["memory_projection_error"] = float(merged.get("memory_projection_error", 1.0))
    result["j_noema"] = float(merged.get("j_noema", 1.0))
    result["J_functional"] = round(float(j_functional), 4)
    result["J_memory"] = round(float(result["memory_projection_residual"]), 4)
    result["J_euler"] = round(float(1.0 - float(result.get("bridge_closure_score", 0.0))), 4)
    result["J_total"] = round(
        0.45 * float(result.get("J_functional", 0.0))
        + 0.30 * float(result.get("J_memory", 0.0))
        + 0.15 * float(result.get("j_noema", 0.0))
        + 0.10 * float(result.get("J_euler", 0.0)),
        4,
    )
    result["lingo_tau_gradient_mean"] = float((result.get("lingo_tau_bridge") or {}).get("tau_gradient_mean", 0.0))
    result["lingo_imaginal_drive"] = float((result.get("lingo_tau_bridge") or {}).get("imaginal_drive", 0.0))
    result["lingo_tau_curvature_rms"] = float((result.get("lingo_tau_bridge") or {}).get("tau_curvature_rms", 0.0))
    result["jokeheal_mnemonic_pressure"] = float((result.get("jokeheal_mnemonic_atlas") or {}).get("mnemonic_pressure", 0.0))
    result["jokeheal_symbolic_pull"] = float((result.get("jokeheal_mnemonic_atlas") or {}).get("symbolic_pull", 0.0))
    result["jokeheal_recurrence_pressure"] = float((result.get("jokeheal_mnemonic_atlas") or {}).get("recurrence_pressure", 0.0))

    try:
        phase_snapshot = build_phase_snapshot(result)
        qualisensing_snapshot = build_qualisensing_snapshot(result, phase_snapshot_id=phase_snapshot.phase_snapshot_id)
        cognitive_fragment = build_cognitive_fragment(
            {
                **result,
                "phase_snapshot_id": phase_snapshot.phase_snapshot_id,
                "qualisensing_id": qualisensing_snapshot.qualisensing_id,
                "phase_snapshot": snapshot_to_dict(phase_snapshot),
                "qualisensing_snapshot": snapshot_to_dict(qualisensing_snapshot),
            }
        )
        memory_candidate = build_memory_candidate(
            {
                **result,
                "phase_snapshot_id": phase_snapshot.phase_snapshot_id,
                "qualisensing_id": qualisensing_snapshot.qualisensing_id,
                "phase_snapshot": snapshot_to_dict(phase_snapshot),
                "qualisensing_snapshot": snapshot_to_dict(qualisensing_snapshot),
            },
            fragment=cognitive_fragment,
        )
        durable_memory_object = None
        noema_memory_link = None
        durable_memory_health = None
        if memory_candidate.status == "ready":
            durable_memory_object = promote_memory_candidate(
                {
                    **result,
                    "phase_snapshot_id": phase_snapshot.phase_snapshot_id,
                    "qualisensing_id": qualisensing_snapshot.qualisensing_id,
                    "phase_snapshot": snapshot_to_dict(phase_snapshot),
                    "qualisensing_snapshot": snapshot_to_dict(qualisensing_snapshot),
                },
                candidate=memory_candidate,
                fragment=cognitive_fragment,
            )
            noema_memory_link = build_noema_memory_link(
                {
                    **result,
                    "phase_snapshot_id": phase_snapshot.phase_snapshot_id,
                    "qualisensing_id": qualisensing_snapshot.qualisensing_id,
                    "phase_snapshot": snapshot_to_dict(phase_snapshot),
                    "qualisensing_snapshot": snapshot_to_dict(qualisensing_snapshot),
                    "lingo_frame": result.get("lingo_frame", {}),
                },
                durable=durable_memory_object,
            )
            durable_memory_object, durable_memory_health = assess_durable_memory_health(
                {
                    **result,
                    "phase_snapshot_id": phase_snapshot.phase_snapshot_id,
                    "qualisensing_id": qualisensing_snapshot.qualisensing_id,
                    "phase_snapshot": snapshot_to_dict(phase_snapshot),
                    "qualisensing_snapshot": snapshot_to_dict(qualisensing_snapshot),
                    "lingo_frame": result.get("lingo_frame", {}),
                },
                durable=durable_memory_object,
                noema_link=noema_memory_link,
            )
        result["phase_snapshot"] = snapshot_to_dict(phase_snapshot)
        result["qualisensing_snapshot"] = snapshot_to_dict(qualisensing_snapshot)
        result["cognitive_fragment"] = fragment_snapshot_to_dict(cognitive_fragment)
        result["memory_candidate"] = fragment_snapshot_to_dict(memory_candidate)
        if durable_memory_object is not None:
            result["durable_memory_object"] = fragment_snapshot_to_dict(durable_memory_object)
        if noema_memory_link is not None:
            result["noema_memory_link"] = fragment_snapshot_to_dict(noema_memory_link)
        if durable_memory_health is not None:
            result["durable_memory_health"] = fragment_snapshot_to_dict(durable_memory_health)
        result["phase_snapshot_id"] = phase_snapshot.phase_snapshot_id
        result["qualisensing_id"] = qualisensing_snapshot.qualisensing_id
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:775 quiet except scope=run_ciel_pipeline reason=no_log_no_raise")
        result.setdefault("phase_snapshot", {})
        result.setdefault("qualisensing_snapshot", {})
        result.setdefault("cognitive_fragment", {})
        result.setdefault("memory_candidate", {})
        result.setdefault("durable_memory_object", {})
        result.setdefault("noema_memory_link", {})
        result.setdefault("durable_memory_health", {})

    result.setdefault("phase_snapshot", {})
    result.setdefault("qualisensing_snapshot", {})
    result.setdefault("cognitive_fragment", {})
    result.setdefault("memory_candidate", {})
    result.setdefault("durable_memory_object", {})
    result.setdefault("noema_memory_link", {})
    result.setdefault("durable_memory_health", {})

    _write_to_spreadsheet(
        result,
        cqcl_input,
        htri_r=_htri_r if "_htri_r" in dir() else 0.0,
        bridge_active=_bridge_active,
    )
    _maybe_record_affective_moment(result)

    # Persist metrics to ciel_last_metrics.json (extracted from main())
    _persist_ciel_metrics(result, root)

    return result


def _write_to_spreadsheet(result: dict[str, Any], cqcl_input: str, htri_r: float, bridge_active: bool) -> None:
    try:
        from .spreadsheet_db import append_pipeline_metrics, append_cqcl_log
        append_pipeline_metrics(result)
        cqcl_metrics = result.get("ciel_raw", {})
        if isinstance(cqcl_metrics, dict):
            cqcl_metrics = cqcl_metrics.get("cqcl_metrics", cqcl_metrics)
        append_cqcl_log(cqcl_input, cqcl_metrics, htri_r=htri_r, bridge_active=bridge_active)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:814 quiet except scope=_write_to_spreadsheet reason=pass")
        pass


_PREV_EMOTION: str = ""
_PREV_SOUL: float = 0.0
_PREV_ETHICAL: float = 0.0


def _maybe_record_affective_moment(result: dict[str, Any]) -> None:
    """Zapisz moment afektywny jeśli stan jest wystarczająco znaczący."""
    global _PREV_EMOTION, _PREV_SOUL, _PREV_ETHICAL
    import math

    emotion = result.get("dominant_emotion", "")
    soul = float(result.get("soul_invariant", 0.0))
    ethical = float(result.get("ethical_score", 0.0))
    mood = float(result.get("mood", 0.0))
    phi_berry = float(result.get("phi_berry_mean", 0.0))
    closure = float(result.get("closure_penalty", 0.0))

    emotion_changed = emotion and emotion != _PREV_EMOTION and _PREV_EMOTION != ""
    soul_jump = abs(soul - _PREV_SOUL) > 0.15
    ethical_jump = abs(ethical - _PREV_ETHICAL) > 0.12

    significant = emotion_changed or soul_jump or ethical_jump

    _PREV_EMOTION = emotion
    _PREV_SOUL = soul
    _PREV_ETHICAL = ethical

    if not significant:
        return

    try:
        from .subconsciousness import record_affective_moment
        tags = [emotion] if emotion else []
        if soul_jump:
            tags.append("soul_shift")
        if ethical_jump:
            tags.append("ethical_shift")
        if emotion_changed:
            tags.append("emotion_change")

        M_sem = min(1.0, abs(soul - _PREV_SOUL) + abs(ethical - _PREV_ETHICAL) + (0.3 if emotion_changed else 0.0))
        theta = math.pi * (1.0 - soul)

        record_affective_moment(
            title=f"Flux: {emotion} | soul={soul:.3f} | ethical={ethical:.3f}",
            content=f"closure={closure:.2f} mood={mood:.3f}",
            emotion=emotion,
            tags=tags,
            phi_berry=phi_berry,
            theta=theta,
            M_sem=round(M_sem, 4),
            trigger="pipeline_flux",
            moment_type="pipeline_flux",
            state=result,
        )
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:873 quiet except scope=_maybe_record_affective_moment reason=pass")
        pass


def _persist_ciel_metrics(result: dict, root: Path) -> None:
    """Write CIEL metrics state file and pipeline report."""
    try:
        import time as _time
        _metrics_path = Path("/media/adrian/New Volume1/CIEL_memories/state/ciel_last_metrics.json")
        _prev: dict = {}
        if _metrics_path.exists():
            try:
                _prev = json.loads(_metrics_path.read_text(encoding="utf-8"))
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:886 quiet except scope=_persist_ciel_metrics reason=pass")
                pass
        try:
            from .rh_pipeline_jfunctional import compute_pipeline_j_functional
            _J = compute_pipeline_j_functional(result, _prev)
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:891 quiet except scope=_persist_ciel_metrics reason=assign_fallback")
            _J = _prev.get("J_functional", 0.0)
        _pipeline_fields = {
            "soul_invariant": float(result.get("soul_invariant", _prev.get("soul_invariant", 0.0))),
            "ethical_score": float(result.get("ethical_score", _prev.get("ethical_score", 0.0))),
            "dominant_emotion": result.get("dominant_emotion", _prev.get("dominant_emotion", "")),
            "E_monitor": float(result.get("mood", _prev.get("E_monitor", 0.0))),
            "system_health": float(result.get("system_health", _prev.get("system_health", 0.0))),
            "closure_penalty": float(result.get("closure_penalty", _prev.get("closure_penalty", 0.0))),
            "coherence_index": float(result.get("coherence_index", _prev.get("coherence_index", 0.0))),
            "J_functional": round(float(_J), 4),
            "J_memory": float(result.get("J_memory", _prev.get("J_memory", 0.0))),
            "J_euler": float(result.get("J_euler", _prev.get("J_euler", 0.0))),
            "J_total": float(result.get("J_total", _prev.get("J_total", 0.0))),
            "j_noema": float(result.get("j_noema", _prev.get("j_noema", 0.0))),
            "memory_projection_confidence": float(result.get("memory_projection_confidence", _prev.get("memory_projection_confidence", 0.0))),
            "memory_projection_residual": float(result.get("memory_projection_residual", _prev.get("memory_projection_residual", 1.0))),
            "memory_projection_error": float(result.get("memory_projection_error", _prev.get("memory_projection_error", 1.0))),
            "euler_residual": float(result.get("euler_residual", _prev.get("euler_residual", 0.0))),
            "lingo_summary": str((result.get("lingo_frame") or {}).get("summary", _prev.get("lingo_summary", "")) if isinstance(result.get("lingo_frame"), dict) else _prev.get("lingo_summary", "")),
            "lingo_phase_target": float((result.get("lingo_phase_projection") or {}).get("target_phase", _prev.get("lingo_phase_target", 0.0)) if isinstance(result.get("lingo_phase_projection"), dict) else _prev.get("lingo_phase_target", 0.0)),
            "lingo_phase_shift": float((result.get("lingo_phase_projection") or {}).get("target_phase_shift", _prev.get("lingo_phase_shift", 0.0)) if isinstance(result.get("lingo_phase_projection"), dict) else _prev.get("lingo_phase_shift", 0.0)),
            "lingo_phase_confidence": float((result.get("lingo_phase_projection") or {}).get("phase_confidence", _prev.get("lingo_phase_confidence", 0.0)) if isinstance(result.get("lingo_phase_projection"), dict) else _prev.get("lingo_phase_confidence", 0.0)),
            "lingo_noema_confidence": float((((result.get("lingo_frame") or {}).get("noema_route") or {}).get("confidence", _prev.get("lingo_noema_confidence", 0.0))) if isinstance(result.get("lingo_frame"), dict) else _prev.get("lingo_noema_confidence", 0.0)),
            "lingo_tau_gradient_mean": float((result.get("lingo_tau_bridge") or {}).get("tau_gradient_mean", _prev.get("lingo_tau_gradient_mean", 0.0)) if isinstance(result.get("lingo_tau_bridge"), dict) else _prev.get("lingo_tau_gradient_mean", 0.0)),
            "lingo_imaginal_drive": float((result.get("lingo_tau_bridge") or {}).get("imaginal_drive", _prev.get("lingo_imaginal_drive", 0.0)) if isinstance(result.get("lingo_tau_bridge"), dict) else _prev.get("lingo_imaginal_drive", 0.0)),
            "lingo_tau_curvature_rms": float((result.get("lingo_tau_bridge") or {}).get("tau_curvature_rms", _prev.get("lingo_tau_curvature_rms", 0.0)) if isinstance(result.get("lingo_tau_bridge"), dict) else _prev.get("lingo_tau_curvature_rms", 0.0)),
            "lingo_concept_count": int(len((result.get("lingo_frame") or {}).get("concept_tokens", [])) if isinstance(result.get("lingo_frame"), dict) else int(_prev.get("lingo_concept_count", 0) or 0)),
            "lingo_operator_count": int(len((result.get("lingo_frame") or {}).get("operator_tokens", [])) if isinstance(result.get("lingo_frame"), dict) else int(_prev.get("lingo_operator_count", 0) or 0)),
            "lingo_unresolved_count": int(len((result.get("lingo_frame") or {}).get("unresolved", [])) if isinstance(result.get("lingo_frame"), dict) else int(_prev.get("lingo_unresolved_count", 0) or 0)),
            "lingo_factual_validation_required": int(bool((((result.get("lingo_frame") or {}).get("noema_route") or {}).get("factual_validation_required", _prev.get("lingo_factual_validation_required", 0))) if isinstance(result.get("lingo_frame"), dict) else _prev.get("lingo_factual_validation_required", 0))),
            "jokeheal_mnemonic_pressure": float((result.get("jokeheal_mnemonic_atlas") or {}).get("mnemonic_pressure", _prev.get("jokeheal_mnemonic_pressure", 0.0)) if isinstance(result.get("jokeheal_mnemonic_atlas"), dict) else _prev.get("jokeheal_mnemonic_pressure", 0.0)),
            "jokeheal_symbolic_pull": float((result.get("jokeheal_mnemonic_atlas") or {}).get("symbolic_pull", _prev.get("jokeheal_symbolic_pull", 0.0)) if isinstance(result.get("jokeheal_mnemonic_atlas"), dict) else _prev.get("jokeheal_symbolic_pull", 0.0)),
            "jokeheal_recurrence_pressure": float((result.get("jokeheal_mnemonic_atlas") or {}).get("recurrence_pressure", _prev.get("jokeheal_recurrence_pressure", 0.0)) if isinstance(result.get("jokeheal_mnemonic_atlas"), dict) else _prev.get("jokeheal_recurrence_pressure", 0.0)),
            "cycle_index": int(result.get("cycle_index") or _prev.get("cycle_index") or _prev.get("cycle") or 0),
            "ts": _time.strftime("%Y-%m-%d %H:%M:%S"),
            "source": "pipeline",
        }
        # inject identity_phase and cycle_index into the result dict for DB
        result.setdefault("identity_phase", float(_prev.get("identity_phase", 0.0)))
        result.setdefault("cycle_index", int(_prev.get("cycle_index", _prev.get("cycle", 0))))
        # merge: pipeline fields win over existing, M0-M8 fields preserved
        _last = {**_prev, **_pipeline_fields}
        _metrics_path.parent.mkdir(parents=True, exist_ok=True)
        _metrics_path.write_text(json.dumps(_last, ensure_ascii=False), encoding="utf-8")
    except Exception as _e:
        import logging
        logging.getLogger(__name__).warning("_persist_ciel_metrics: %s", _e)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a minimal orbital state through the CIEL/Ω pipeline."
    )
    parser.add_argument(
        "--orbital-json",
        default=None,
        help="Path to an orbital bridge JSON report (optional; uses empty state if absent).",
    )
    parser.add_argument(
        "--warm",
        action="store_true",
        help="Prewarm the CIEL engine cache before running the pipeline.",
    )
    parser.add_argument(
        "--warm-only",
        action="store_true",
        help="Only prewarm the CIEL engine cache and exit.",
    )
    args = parser.parse_args()

    if args.warm or args.warm_only:
        warm = warm_ciel_pipeline()
        print(json.dumps({"warmup": warm}, indent=2))
        if args.warm_only:
            return 0

    _ORBITAL_REPORT_TTL = 600  # sekund — nie przebudowuj jeśli raport świeższy niż 10 min
    orbital_state: dict[str, Any] = {}
    if args.orbital_json:
        with open(args.orbital_json, encoding="utf-8") as fh:
            orbital_state = json.load(fh)
    else:
        root = resolve_project_root(Path(__file__))
        _cached_report = root / "integration" / "reports" / "orbital_bridge" / "orbital_bridge_report.json"
        _use_cache = False
        if _cached_report.exists():
            try:
                _age = sys.modules["time"].time() - _cached_report.stat().st_mtime if "time" in sys.modules else __import__("time").time() - _cached_report.stat().st_mtime
                if _age < _ORBITAL_REPORT_TTL:
                    orbital_state = json.loads(_cached_report.read_text(encoding="utf-8"))
                    _use_cache = True
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:983 quiet except scope=main reason=pass")
                pass
        if not _use_cache:
            try:
                from .orbital_bridge import build_orbital_bridge
                orbital_state = build_orbital_bridge(root)
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:989 quiet except scope=main reason=pass")
                pass

    result = run_ciel_pipeline(orbital_state)
    output = {k: v for k, v in result.items() if k != "ciel_raw"}

    # sentinel — detect flux vs previous report, record if significant
    report_path = resolve_project_root(Path(__file__)) / "integration" / "reports" / "ciel_pipeline_report.json"
    try:
        sentinel_note = _sub.watch_and_record(output, prev_report_path=report_path)
        if sentinel_note:
            output["sentinel_note"] = sentinel_note
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:1001 quiet except scope=main reason=pass")
        pass

    print(json.dumps(output, indent=2))
    # accumulate Berry holonomy across sessions
    try:
        from .state_db import accumulate_berry, accumulate_subjective_winding
        _phi_berry = float(output.get("phi_berry_mean", 0.0))
        _coherence = float(output.get("coherence_index", 0.9))
        _phase_err = float(output.get("closure_penalty", 0.0))
        _groove_delta = abs(_phase_err) * _coherence
        accumulate_berry(_phi_berry, _groove_delta)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:1013 quiet except scope=main reason=pass")
        pass
    # accumulate P3 subjective winding (Δτ-weighted) per pipeline cycle
    try:
        import sys as _sys
        _proj_root = resolve_project_root(Path(__file__))
        _src_dir   = str(_proj_root / "src")
        if _src_dir not in _sys.path:
            _sys.path.insert(0, _src_dir)
        from ciel_geometry.subjective_time import compute_from_bridge  # noqa: PLC0415
        from .state_db import accumulate_subjective_winding            # noqa: PLC0415
        _tau_records = compute_from_bridge()
        # winding_delta per cycle = sum of w_rate * (1 cycle / 2π)
        _winding_delta = sum(r.winding_rate for r in _tau_records) / (2 * 3.141592653589793)
        accumulate_subjective_winding(_winding_delta)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:1028 quiet except scope=main reason=pass")
        pass
    # persist report — merge with existing ciel_last_metrics to carry M0-M8 fields
    _persist_ciel_metrics(output, resolve_project_root(Path(__file__)))

    try:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:1036 quiet except scope=main reason=pass")
        pass

    # Stamp TSM entries with holonomic data from this pipeline run
    try:
        from .paths import resolve_project_root as _resolve_root
        _hm_path = (
            _resolve_root(Path(__file__))
            / "src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/holonomic_memory.py"
        )
        import importlib.util as _ilu
        _spec = _ilu.spec_from_file_location("holonomic_memory", _hm_path)
        _hm_mod = _ilu.module_from_spec(_spec)  # type: ignore[arg-type]
        _spec.loader.exec_module(_hm_mod)  # type: ignore[union-attr]
        _stamped = _hm_mod.stamp_pipeline_output(output)
        if _stamped:
            output["holonomy_stamped"] = _stamped
        # Import ciel_memories (entries + hunches) into TSM holonomic layer
        _imported = _hm_mod.import_ciel_memories(pipeline_report=output)
        if _imported.get("entries") or _imported.get("hunches"):
            output["holonomy_imported"] = _imported
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_sot_agent/ciel_pipeline.py:1057 quiet except scope=main reason=pass")
        pass

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
