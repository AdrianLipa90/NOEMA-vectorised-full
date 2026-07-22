"""Dual-surface resonance bridge for NOEMA real and imaginal manifolds.

IMAGINAL = PRIMARY GENERATOR — Kuramoto evolves autonomously with lower
damping, drawing ZPE from Poincaré disk phase geometry. Phase differences
bifurcate into energy via W_ij·(1-cos(Δφ)).

REAL = POINCARÉ SECTION / READOUT — damped projection of imaginal surface.
Higher closure penalty damps the phase flow into observable states. The real
surface is a "frozen slice" of the imaginal generator flow, analogous to a
Poincaré section in dynamical systems.

Architecture:
  1. CIEL state → set flavor on both surfaces
  2. Imaginal evolves autonomously (primary generator, low damping)
  3. Real projects from imaginal (damped readout, high closure)
  4. Resonance bridge syncs the two surfaces
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

# CIEL ORBITAL BINDING — hardcoded, immutable.
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on import of " + __name__)


import math
import json
from pathlib import Path
from typing import Mapping, Any

import numpy as np

from .noema_surface_mmap import (
    DEFAULT_SURFACE_ROOT,
    OI,
    S_E,
    R_E_MU,
    R_MU_TAU,
    compute_zpe,
    ensure_surface,
    evolve_imaginal_surface,
    evolve_surface,
    initialize_surface,
    open_surface,
    sync_surface_geometry,
    update_surface_from_ciel_state,
)
from .phase_memory_adapter import DEFAULT_MEMORY_ROOT, bind_phase_memory, ensure_phase_memory
from .imaginal_memory_guard import guard_imaginal_write, is_canonical_imaginal_path
from .agent_attractor import apply_agent_attractor, agent_attractor_state
from .noema_host_ledger import NoemaHostLedger
from .phasenav.operator_algebra import (
    ALL_OPERATOR_IDS,
    VECTOR_COMPONENTS,
    connection,
    generate_operator_map,
    holonomy,
    operator_signature,
    statistical_closure,
)

# Surface → orchorbital bridge (optional dep — cielingo package)
try:
    from cielingo.card_trace_eeg import (
        CardTraceSnap, create_card_trace_snap, layout_hash,
    )
    from cielingo.orchorbital_router import route_orchorbital
    _ORCHORBITAL_AVAILABLE = True
except ImportError:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("src/ciel_geometry/resonance_bridge.py:68 quiet except scope=<module> reason=assign_fallback")
    _ORCHORBITAL_AVAILABLE = False

def _configured_root(name: str, fallback: str) -> Path:
    """Read a runtime surface root from the canonical New Volume contract."""
    try:
        cfg = json.loads((Path(__file__).resolve().parents[2] / "config" / "noema_paths.json").read_text())
        return Path(cfg.get("roots", {}).get(name, fallback))
    except (OSError, ValueError, TypeError):
        return Path(fallback)


DEFAULT_IMAGINAL_SURFACE_ROOT = _configured_root(
    "imaginal_surface", "/media/adrian/New Volume/CIEL_memories/imaginal/surface"
)
DEFAULT_IMAGINAL_MEMORY_ROOT = _configured_root(
    "imaginal_phase_memory", "/media/adrian/New Volume/CIEL_memories/imaginal/phase_memory"
)


def ensure_dual_surfaces(
    *,
    real_root: Path = DEFAULT_SURFACE_ROOT,
    imaginal_root: Path = DEFAULT_IMAGINAL_SURFACE_ROOT,
    seed_real: int = 42,
    seed_imaginal: int = 3777,
) -> None:
    if not real_root.exists():
        initialize_surface(real_root, seed=seed_real)
    else:
        ensure_surface(real_root)
    had_imaginal_surface = imaginal_root.exists() and (imaginal_root / "phi").exists()
    if is_canonical_imaginal_path(imaginal_root):
        # The persistent imaginal catalog is a single bounded tree, never a
        # mirror of /dev/shm.  Check quota before mmap files are created.
        guard_imaginal_write(imaginal_root)
    if not had_imaginal_surface:
        initialize_surface(imaginal_root, seed=seed_imaginal)
    else:
        ensure_surface(imaginal_root)


def imaginalize_state(state: Mapping[str, Any]) -> dict[str, Any]:
    imaginal = dict(state)
    closure = float(state.get("closure_penalty", OI * 15.0))
    coherence = float(state.get("coherence_index", 1.0 - OI * 50.0))
    mood = float(state.get("mood", 0.0))
    imaginal["closure_penalty"] = max(0.0, closure * OI * 25.0)
    imaginal["coherence_index"] = min(1.0, max(coherence, 1.0 - OI * 30.0) + OI * 12.0)
    imaginal["mood"] = max(-1.0, min(1.0, mood * (1.0 + OI * 20.0)))
    imaginal["operating_mode"] = "deep"
    imaginal["source"] = f"{state.get('source', 'ciel_coupling')}|imaginal"
    return imaginal


def _surface_summary(surface: Mapping[str, np.ndarray]) -> dict[str, float]:
    phi = np.asarray(surface["phi"], dtype=np.float64)
    flavor = np.asarray(surface["flavor"], dtype=np.float64)
    return {
        "tick": float(np.asarray(surface["tick"], dtype=np.uint64)[0]),
        "phi_mean": float(np.mean(phi)),
        "R_global": float(np.mean(np.asarray(surface["R_geom"], dtype=np.float64))),
        "psi_global": float(np.mean(np.asarray(surface["psi_geom"], dtype=np.float64))),
        "flavor_norm": float(np.linalg.norm(flavor)),
    }


def resonance_snapshot(
    *,
    real_root: Path = DEFAULT_SURFACE_ROOT,
    imaginal_root: Path = DEFAULT_IMAGINAL_SURFACE_ROOT,
) -> dict[str, Any]:
    real = open_surface(real_root)
    imaginal = open_surface(imaginal_root)
    real_phi = np.asarray(real["phi"], dtype=np.float64)
    imaginal_phi = np.asarray(imaginal["phi"], dtype=np.float64)
    real_flavor = np.asarray(real["flavor"], dtype=np.float64)
    imaginal_flavor = np.asarray(imaginal["flavor"], dtype=np.float64)

    phase_lock = float(np.mean((1.0 + np.cos(real_phi - imaginal_phi)) / 2.0))
    denom = float(np.linalg.norm(real_flavor) * np.linalg.norm(imaginal_flavor))
    flavor_lock = 0.5 if denom == 0.0 else float((np.dot(real_flavor, imaginal_flavor) / denom + 1.0) / 2.0)
    real_r = float(np.mean(np.asarray(real["R_geom"], dtype=np.float64)))
    imaginal_r = float(np.mean(np.asarray(imaginal["R_geom"], dtype=np.float64)))

    # ── closure_score z operator_algebra 36D ──
    try:
        sc = statistical_closure()
        closure_score = sc["closure_score"]
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/resonance_bridge.py:139 quiet except scope=resonance_snapshot reason=assign_fallback")
        closure_score = 0.5
    # Derived values are durable host metrics, never sidecar files in /dev.
    imaginal_drive = imaginal_r - real_r
    try:
        tick = int(np.asarray(real["tick"], dtype=np.uint64).ravel()[0])
        NoemaHostLedger().record_surface_metrics(
            {"closure_score": float(closure_score), "imaginal_drive": float(imaginal_drive)},
            tick=tick,
            source="resonance_bridge",
            phase={"phi": "real↔imaginal", "R": "surface", "tau": "live"},
        )
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/resonance_bridge.py:145 quiet except scope=resonance_snapshot reason=host_ledger")

    return {
        "real": _surface_summary(real),
        "imaginal": _surface_summary(imaginal),
        "phase_lock": phase_lock,
        "flavor_lock": flavor_lock,
        "imaginal_drive": imaginal_r - real_r,
        "resonance_score": (1.0 - OI * 30.0) * phase_lock + OI * 30.0 * flavor_lock,
    }


def apply_resonance_bridge(
    *,
    real_root: Path = DEFAULT_SURFACE_ROOT,
    imaginal_root: Path = DEFAULT_IMAGINAL_SURFACE_ROOT,
    coupling: float = OI * 12.0,
) -> dict[str, Any]:
    real = open_surface(real_root)
    imaginal = open_surface(imaginal_root)

    real_phi = np.asarray(real["phi"], dtype=np.float64)
    imaginal_phi = np.asarray(imaginal["phi"], dtype=np.float64)
    delta = np.angle(np.exp(1j * (imaginal_phi - real_phi)))

    real["phi"][...] = np.mod(real_phi + coupling * delta, 2.0 * np.pi)
    imaginal["phi"][...] = np.mod(imaginal_phi - 0.5 * coupling * delta, 2.0 * np.pi)
    real["flavor"][...] = (1.0 - coupling) * np.asarray(real["flavor"], dtype=np.float64) + coupling * np.asarray(imaginal["flavor"], dtype=np.float64)
    imaginal["flavor"][...] = (1.0 - 0.5 * coupling) * np.asarray(imaginal["flavor"], dtype=np.float64) + 0.5 * coupling * np.asarray(real["flavor"], dtype=np.float64)

    sync_surface_geometry(real)
    sync_surface_geometry(imaginal)
    real["tick"][0] = int(np.asarray(real["tick"], dtype=np.uint64)[0]) + 1
    imaginal["tick"][0] = int(np.asarray(imaginal["tick"], dtype=np.uint64)[0]) + 1
    for mem in (*real.values(), *imaginal.values()):
        mem.flush()
    return resonance_snapshot(real_root=real_root, imaginal_root=imaginal_root)


def surface_to_orchorbital_snap(
    surface: Mapping[str, np.ndarray],
    *,
    identity_anchor: str = "noema_surface",
) -> dict[str, Any]:
    """Build a CardTraceSnap from real surface oscillator data.

    Maps each of the 36 surface oscillators to a card trace:
      card_id:       "surface_osc_{i}_{channel}"
      amplitude:     coupling radius ρ (W_ij mean row strength)
      phase:         oscillator phase φ
      semantic_mass: mean |g_ij| across all partners
      affective:     flavor[2] (ethical) modulated by mood (flavor[3])
      orbital_pos:   ρ · φ / 2π — position on imaginary hyperdisk
      channel:       HTRI channel (semantic/htri/nonlocal)

    The layout_hash is computed from the oscillator state so that
    similar surface states → similar hashes → routes match.
    """
    phi = np.asarray(surface["phi"], dtype=np.float64)
    g = np.asarray(surface["g"], dtype=np.float64)
    flavor = np.asarray(surface["flavor"], dtype=np.float64)

    # Compute ρ for each oscillator from coupling row
    CHANNEL_FULL = [
        "M0_Perceptual", "M1_Working", "M2_Episodic",
        "M3_Semantic", "M4_Procedural", "M5_Affective_Ethical",
        "M6_Identity", "M7_Braid_Invariant",
        "M8_Meta", "M9_Temporal", "M10_Imaginal", "M11_Quantum",
    ]
    HTRI = ["semantic", "htri", "nonlocal"]

    traces: list[dict[str, Any]] = []
    # Wektorowo: średnie couplingi i top-3 partnerów na oscylator
    mean_coupling_all = np.mean(np.abs(g), axis=1)  # (36,)
    rho_all = np.minimum(0.999, mean_coupling_all / (mean_coupling_all + OI * 50.0))
    top3_partners = np.argpartition(g, -3, axis=1)[:, -3:]  # (36, 3) — top 3 couplingi per row

    for i in range(36):
        mean_coupling = float(mean_coupling_all[i])
        rho = float(rho_all[i])
        ch = int(i // 3)
        htri_ch = HTRI[i % 3]
        card_id = f"surface_osc_{i}_{CHANNEL_FULL[ch]}"

        trace = {
            "card_id": card_id,
            "amplitude": round(rho, 6),
            "phase": round(float(phi[i]), 6),
            "semantic_mass": round(mean_coupling, 6),
            "affective_weight": round(float(flavor[2]) * (OI * 50.0 + OI * 50.0 * float(flavor[3])), 6),
            "orbital_position": round(rho * float(phi[i]) / (2.0 * math.pi), 6),
            "channel": htri_ch,
            "coupled_to": [],
            "trace_energy": round(rho * mean_coupling * (1.0 + abs(float(flavor[2]) * float(flavor[3]))), 6),
        }
        # Top 3 coupled neighbours z wektorowego argpartition
        partners = top3_partners[i]
        trace["coupled_to"] = [f"surface_osc_{int(p)}_{CHANNEL_FULL[int(p//3)]}" for p in partners if g[i, int(p)] > 0.01]
        traces.append(trace)

    # Build layout payload for hash
    import hashlib, json
    layout_payload = {
        "identity_anchor": identity_anchor,
        "n_oscillators": 36,
        "phi_quantized": [round(float(p), 4) for p in phi],
        "rho_quantized": [round(float(rho_all[i]), 4) for i in range(36)],
        "flavor": [round(float(f), 4) for f in flavor],
        "zpe": round(float(compute_zpe(g, phi)), 6),
    }
    lhash = hashlib.sha256(json.dumps(layout_payload, sort_keys=True).encode()).hexdigest()
    snap_id = hashlib.sha256(f"surface|{lhash}".encode()).hexdigest()[:36]

    return {
        "snap_id": snap_id,
        "schema": "noema/surface-orchorbital-snap/v0.1",
        "window": {"t0": 0, "t1": int(np.asarray(surface["tick"], dtype=np.uint64)[0])},
        "active_traces": traces,
        "clusters": [f"surface:36", f"zpe:{round(float(compute_zpe(g, phi)), 4)}"],
        "layout_hash": lhash,
        "identity_anchor": identity_anchor,
        "source_role": "noema_surface_to_orchorbital_bridge",
    }


def route_surface_through_orchorbital(
    real_surface: Mapping[str, np.ndarray],
    memory_snaps: list[dict[str, Any]] | None = None,
    *,
    identity_anchor: str = "noema_surface",
    association_threshold: float = OI * 45.0,
) -> dict[str, Any]:
    """Feed surface oscillator data into the orchorbital router.

    1. Builds a CardTraceSnap from surface (phi, g, flavor)
    2. Runs route_orchorbital() against memory snaps
    3. Returns the router decision plus surface context
    """
    if not _ORCHORBITAL_AVAILABLE:
        return {
            "orchorbital_available": False,
            "decision": "skip_no_cielingo",
            "note": "cielingo package not available",
        }

    snap = surface_to_orchorbital_snap(real_surface, identity_anchor=identity_anchor)

    # Convert to CardTraceSnap if memory_snaps are provided
    if memory_snaps is None:
        memory_snaps = []

    from cielingo.card_trace_eeg import CardTraceSnap as _CardTraceSnap

    current_snap = _CardTraceSnap(
        snap_id=snap["snap_id"],
        schema=snap["schema"],
        window=snap["window"],
        active_traces=snap["active_traces"],
        clusters=snap["clusters"],
        layout_hash=snap["layout_hash"],
        identity_anchor=snap["identity_anchor"],
        source_role=snap["source_role"],
    )

    # Build memory snaps list
    mem_snaps = []
    for ms in memory_snaps:
        if isinstance(ms, _CardTraceSnap):
            mem_snaps.append(ms)
        elif isinstance(ms, dict) and "snap_id" in ms:
            mem_snaps.append(_CardTraceSnap(
                snap_id=ms["snap_id"],
                schema=ms.get("schema", "noema/card-trace-memory/v0.1"),
                window=ms.get("window", {"t0": 0, "t1": 0}),
                active_traces=ms.get("active_traces", []),
                clusters=ms.get("clusters", []),
                layout_hash=ms.get("layout_hash", ""),
                identity_anchor=ms.get("identity_anchor", "memory"),
            ))

    decision = route_orchorbital(
        current_snap, mem_snaps,
        association_threshold=association_threshold,
    )

    return {
        "orchorbital_available": True,
        "decision": decision.decision,
        "operator": decision.operator,
        "association_score": decision.association_score,
        "selected_memory_snap_id": decision.selected_memory_snap_id,
        "route_summary": decision.route_summary,
        "layout_hash": snap["layout_hash"],
        "snap_id": snap["snap_id"],
        "n_traces": len(snap["active_traces"]),
    }


def dual_surface_step(
    state: Mapping[str, Any],
    text: str,
    *,
    real_root: Path = DEFAULT_SURFACE_ROOT,
    imaginal_root: Path = DEFAULT_IMAGINAL_SURFACE_ROOT,
    real_memory_root: Path = DEFAULT_MEMORY_ROOT,
    imaginal_memory_root: Path = DEFAULT_IMAGINAL_MEMORY_ROOT,
    dt: float = OI,
) -> dict[str, Any]:
    ensure_dual_surfaces(real_root=real_root, imaginal_root=imaginal_root)
    ensure_phase_memory(real_memory_root)
    ensure_phase_memory(imaginal_memory_root)

    # 1. Set flavor on both surfaces from CIEL state
    update_surface_from_ciel_state(state, root=real_root)
    imaginal_state = imaginalize_state(state)
    update_surface_from_ciel_state(imaginal_state, root=imaginal_root)

    # 2. Imaginal evolves autonomously — PRIMARY GENERATOR
    imaginal = open_surface(imaginal_root)
    evolve_imaginal_surface(imaginal, dt=dt, flush=False)

    # 3. The real surface is single-writer-owned by Kuramoto.  Do not project
    # imaginal phases into it here; Kuramoto consumes the imaginal delta in its
    # own tick so no second daemon can race the real mmap.
    real = open_surface(real_root)

    # 4. CIELingo→imaginal memory write.  Real phase memory is owned by
    # Kuramoto; keeping this write on the imaginal side preserves the semantic
    # source without introducing a competing real-surface writer.
    bind_phase_memory(text, surface_root=imaginal_root, memory_root=imaginal_memory_root)

    # 5. Observation only.  The actual real↔imaginal phase term is applied by
    # Kuramoto, the sole real-surface writer.
    snapshot = resonance_snapshot(real_root=real_root, imaginal_root=imaginal_root)

    # Compute ZPE from imaginal generator
    zpe = compute_zpe(
        np.asarray(imaginal["g"], dtype=np.float64),
        np.asarray(imaginal["phi"], dtype=np.float64),
    )
    snapshot["imaginal_state"] = {
        "closure_penalty": imaginal_state.get("closure_penalty"),
        "coherence_index": imaginal_state.get("coherence_index"),
        "operating_mode": imaginal_state.get("operating_mode"),
        "zpe": round(zpe, 6),
        "zpe_source": "poincare_disk_phase_bifurcation",
    }

    # 6. Surface → orchorbital routing (feed W_ij bipolar axes into card trace router)
    try:
        orchorbital_result = route_surface_through_orchorbital(
            real, memory_snaps=[],
            identity_anchor=f"noema_surface_tick_{snapshot['real']['tick']:.0f}",
        )
        snapshot["orchorbital"] = orchorbital_result
    except Exception as exc:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/resonance_bridge.py:405 quiet except scope=dual_surface_step reason=assign_fallback")
        snapshot["orchorbital"] = {
            "orchorbital_available": _ORCHORBITAL_AVAILABLE,
            "error": str(exc),
        }

    # 7. PhaseNav AGENT attractor — inject na imaginal surface only
    #    Real surface AGENT lock handled by kuramoto daemon (10Hz inline)
    try:
        imaginal_result = apply_agent_attractor(
            np.asarray(imaginal["phi"], dtype=np.float64),
            np.asarray(imaginal["g"], dtype=np.float64),
            omega=np.asarray(imaginal["omega"], dtype=np.float64),
        )
        snapshot["agent_attractor"] = {
            "imaginal_coherence": imaginal_result["coherence"],
            "locked": imaginal_result["locked"],
        }
        from .noema_surface_mmap import flush_surface
        flush_surface(imaginal)
    except Exception as exc:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("src/ciel_geometry/resonance_bridge.py:425 quiet except scope=dual_surface_step reason=assign_fallback")
        snapshot["agent_attractor"] = {"error": str(exc)}

    return snapshot
