#!/usr/bin/env python3
"""CIELingo → NOEMA phase sync daemon — Euler's identity e^{iπ} + 1 = 0.

Zasada: Σ_{k=0}^{N-1} e^{iφ_k} = 0  (Euler closure condition)

Cykl:
  1. CIELingo closure (build_orbital_bridge) — własna optymalizacja
  2. PMNS boost na g matrix (neutrino mixing przez różnicę faz)
  3. Manifest → surface z Euler constraint enforcement (jednokierunkowo!)

Usage:
    python scripts/ciel_noema_cielingo_sync.py [--interval SEC] [--oneshot]
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import argparse
import json
import logging
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
_SRC = str(ROOT / "src")
for _p in (_SRC, str(ROOT / "integration")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from ciel_geometry.noema_registry import registry
from ciel_sot_agent.cielingo_bridge import ethical_gate

SURFACE_DIR = Path("/dev/shm/ciel_noema")

logging.basicConfig(
    level=logging.INFO,
    format="[euler-sync] %(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

_MEM_ROOT = ROOT / "src"  # parent of CIEL_OMEGA_COMPLETE_SYSTEM/
for _p in (_SRC, str(_MEM_ROOT)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

MANIFEST_PATH = ROOT / "integration" / "Orbital" / "main" / "manifests" / "sectors_global.json"

SECTOR_NAMES = ["constraints", "fields", "runtime", "memory", "bridge", "vocabulary"]
SECTOR_TO_OSCILLATORS = {
    "constraints": (0, 1, 2, 3),
    "fields":      (4, 5, 6, 7),
    "runtime":     (8, 9, 10, 11),
    "memory":      (12, 13, 14, 15),
    "bridge":      (16, 17, 18, 19),
    "vocabulary":  (20, 21, 22, 23),
}

N_OSCILLATORS = 36
N_SECTORS = len(SECTOR_NAMES)

# Vectorized lookup: dla każdego oscylatora (0..23) indeks sektora (0..N_SECTORS-1)
OSC_TO_SECTOR_IDX = np.zeros(N_OSCILLATORS, dtype=np.uint8)
for _i_sec, _sec in enumerate(SECTOR_NAMES):
    OSC_TO_SECTOR_IDX[list(SECTOR_TO_OSCILLATORS[_sec])] = _i_sec

# Sektorowa macierz projekcji (N_SECTORS × N_OSCILLATORS) — jedynka gdy oscylator ∈ sektor
_SECTOR_MASK = np.zeros((N_SECTORS, N_OSCILLATORS), dtype=np.float64)
for _i_sec in range(N_SECTORS):
    _SECTOR_MASK[_i_sec, OSC_TO_SECTOR_IDX == _i_sec] = 1.0

# Liczebność każdego sektora
_SECTOR_SIZES = np.array([len(SECTOR_TO_OSCILLATORS[s]) for s in SECTOR_NAMES], dtype=np.float64)


# ── Euler's identity core ───────────────────────────────────────────

def euler_residual(phi: np.ndarray) -> float:
    """|Σ e^{iφ_k}| — Euler residual. 0 = perfect closure."""
    return float(abs(np.sum(np.exp(1j * phi))))


def euler_target_phases(phi: np.ndarray) -> np.ndarray:
    """φ_target_i = angle(-Σ_{j≠i} e^{iφ_j}).

    Każdy oscylator dąży do fazy która zeruje Euler sumę.
    """
    z = np.exp(1j * phi)
    total = np.sum(z)
    # Dla każdego i: target = angle(-(total - z_i))
    return np.angle(-(total - z))


def euler_guided_tau(phi: np.ndarray, tau_base: np.ndarray | None = None) -> np.ndarray:
    """τ_i = |Σ_{j≠i} e^{iφ_j}|.

    τ = magnitude of the opposing sum → how hard each oscillator
    is 'pulled' toward Euler identity.
    Clip to [0.01, 1.0].
    """
    total = np.sum(np.exp(1j * phi))
    z = np.exp(1j * phi)
    tau_new = np.abs(total - z)
    if tau_base is not None:
        tau_new = 0.7 * tau_base + 0.3 * tau_new
    return np.clip(tau_new, 0.01, 1.0)


def apply_euler_sync(
    phi: np.ndarray,
    tau: np.ndarray | None = None,
    *,
    mix: float = 0.3,
) -> tuple[np.ndarray, np.ndarray]:
    """Aplikuj Euler constraint: przesuń φ w kierunku φ_target.

    Returns:
      phi_synced, tau_synced
    """
    phi_target = euler_target_phases(phi)
    delta = np.angle(np.exp(1j * (phi_target - phi)))
    phi_new = phi + mix * delta
    tau_new = euler_guided_tau(phi_new, tau)
    return phi_new, tau_new


# ── Surface ↔ Manifest (Euler-aware) ──────────────────────────────

def _read_manifest() -> dict:
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return {}


def _write_manifest(doc: dict) -> None:
    MANIFEST_PATH.write_text(
        json.dumps(doc, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def surface_to_manifest(surface: dict) -> dict:
    """Surface → manifest z Euler residual."""
    phi_s = np.asarray(surface["phi"], dtype=np.float64)

    doc = _read_manifest()
    sectors = doc.get("sectors", doc)
    euler_res = euler_residual(phi_s)
    phi_target = euler_target_phases(phi_s)

    meta = doc.setdefault("metadata", {})
    surface_data = meta.setdefault("surface_state", {})
    # Wektorowo: średnia faza po sektorach = _SECTOR_MASK @ phi / _SECTOR_SIZES
    mu_phi_sec = (_SECTOR_MASK @ phi_s) / _SECTOR_SIZES
    mu_target_sec = (_SECTOR_MASK @ phi_target) / _SECTOR_SIZES
    for i, sec_name in enumerate(SECTOR_NAMES):
        if sec_name not in sectors:
            continue
        sec = sectors[sec_name]
        idxs = SECTOR_TO_OSCILLATORS[sec_name]
        sec["phi"] = ((float(mu_phi_sec[i]) + np.pi) % (2 * np.pi)) - np.pi
        # Store raw surface data in metadata (not in sector payload)
        surface_data[sec_name] = {
            "phi_raw": [float(phi_s[j]) for j in idxs],
            "phi_target": float(mu_target_sec[i]),
        }

    meta["last_surface_sync"] = time.time()
    meta["euler_residual"] = euler_res
    _write_manifest(doc)
    log.info("Surface → manifest: euler_res=%.4f", euler_res)
    return doc


def manifest_to_surface(surface: dict, doc: dict | None = None) -> None:
    """Manifest → surface z Euler enforcement."""
    phi_s = np.asarray(surface["phi"], dtype=np.float64)
    if doc is None:
        doc = doc = _read_manifest()
    sectors = doc.get("sectors", doc)

    tau_s = np.asarray(surface["tau"], dtype=np.float64) if "tau" in surface else None

    # 1. Wpisz fazy z manifestu — wektorowo przez OSC_TO_SECTOR_IDX
    phi_per_sec = np.array([sectors.get(s, {}).get("phi", 0.0) for s in SECTOR_NAMES], dtype=np.float64)
    phi_s[:] = phi_per_sec[OSC_TO_SECTOR_IDX]

    # 2. Euler enforcement — delikatne przesunięcie ku Σe^{iφ}=0
    # tau nie jest nadpisywany z manifestu (zawsze 1.0) — zostaje z inicjalizacji
    tau_current = tau_s.copy() if tau_s is not None else None
    phi_new, tau_new = apply_euler_sync(phi_s, tau_current, mix=0.08)
    phi_s[:] = phi_new
    if tau_s is not None:
        tau_s[:] = tau_new

    from ciel_geometry.noema_surface_mmap import flush_surface

    flush_surface(surface)
    euler_res = euler_residual(phi_s)
    coh = abs(np.mean(np.exp(1j * phi_s)))
    log.info(
        "Manifest → surface: euler_res=%.4f  coh=%.4f  τ̄=%.4f",
        euler_res, coh, float(np.mean(tau_s)) if tau_s is not None else 0,
    )


# ── CIELingo closure z PMNS boost ──────────────────────────────────

def run_cielingo_closure() -> dict | None:
    """Cykl: CIELingo → PMNS boost → surface (jednokierunkowo)."""
    try:
        from ciel_sot_agent.orbital_bridge import build_orbital_bridge
        from ciel_geometry.neutrino_phase_channel import (
            compute_neutrino_phase_bus,
            apply_neutrino_bus_to_surface,
        )
        from ciel_geometry.noema_surface_mmap import ensure_surface, flush_surface

        # 1. CIELingo closure — własna optymalizacja z manifestu
        bridge = build_orbital_bridge(ROOT)
        health = bridge.get("health_manifest", {})
        cp = float(health.get("closure_penalty", 0.0))
        mode = bridge.get("recommended_control", {}).get("mode", "standard")
        coh = float(bridge.get("state_manifest", {}).get("coherence_index", 0.0))

        # 2. PMNS boost i Euler sync na powierzchni
        surface = ensure_surface()
        phi = np.asarray(surface["phi"], dtype=np.float64)
        g = np.asarray(surface["g"], dtype=np.float64)
        omega = np.asarray(surface["omega"], dtype=np.float64)
        flavor = np.asarray(surface["flavor"], dtype=np.float64)
        euler_before = euler_residual(phi)

        bus = compute_neutrino_phase_bus(phi, g, omega, flavor, D_f=2.57)
        # write_flavor=False — flavor[4] owned by neutrino daemon per FLAVOR_CONTRACT
        apply_neutrino_bus_to_surface(surface, bus, D_f=2.57, write_flavor=False, write_g=True)

        # 3. τ ↔ φ feedback: tau modulated by Euler residual + semantic gravity (TARDIS)
        doc = _read_manifest()
        sectors = doc.get("sectors", doc)
        # Read CIELingo's optimized state — wektorowo
        phi_m = np.array([sectors.get(s, {}).get("phi", 0.0) for s in SECTOR_NAMES], dtype=np.float64)
        # Read tau from SURFACE (not manifest) — manifest tau is always stale
        tau_surf = np.asarray(surface["tau"], dtype=np.float64) if "tau" in surface else None
        if tau_surf is not None and tau_surf.max() > 0.01:
            # Aggregate per-sector: mean of oscillators in each sector
            tau_m = np.array([float(np.mean(tau_surf[OSC_TO_SECTOR_IDX == i])) for i in range(N_SECTORS)])
        else:
            tau_m = np.array([sectors.get(s, {}).get("tau", 0.353) for s in SECTOR_NAMES], dtype=np.float64)

        z = np.exp(1j * phi_m)
        total = np.sum(z)
        R = abs(total)  # Euler residual
        # Wektorowo: target_i = angle(-sum_{j≠i} z_j) = angle(-(total - z_i))
        target = np.angle(-(total - z) + 1e-10)
        tau_m += 0.05 * R * np.cos(target - phi_m) - 0.02 * (tau_m - 0.353)

        # ── TARDIS: log only — scaling moved to evolve_surface() ──────
        if "gravity" in surface:
            gvec = np.asarray(surface["gravity"], dtype=np.float64)
            tau_dilation = float(gvec[1])  # γ from semantic density
            log.info("🪐 TARDIS: semantic_gravity=%.4f γ=%.4f τ̄=%.4f",
                     float(gvec[0]), tau_dilation, float(np.mean(tau_m)))
        # ── /TARDIS ──────────────────────────────────────────────────────

        tau_m = np.clip(tau_m, 0.01, 1.0)

        # Write adjusted tau back to manifest
        for i, sec_name in enumerate(SECTOR_NAMES):
            if sec_name in sectors:
                sectors[sec_name]["tau"] = round(float(tau_m[i]), 6)
        # Also write D_f from cp: lower cp → higher D_f → more Λ
        doc.setdefault("metadata", {})  # ensure metadata exists (L-032)
        D_f_new = 2.57 - 0.57 * min(1.0, cp / 1.5)
        doc["metadata"]["D_f"] = D_f_new
        doc["metadata"]["tau_phi_feedback_R"] = float(R)
        _write_manifest(doc)

        # 4. Manifest → surface (CIELingo φ → NOEMA surface)
        manifest_to_surface(surface, doc)
        # Apply tau from manifest to surface tau field — wektorowo
        if "tau" in surface:
            tau_s = np.asarray(surface["tau"], dtype=np.float64)
            tau_s[:] = tau_m[OSC_TO_SECTOR_IDX]
        # Write D_f and Euler closure residual to surface for neutrino daemon
        flavor_s = np.asarray(surface["flavor"], dtype=np.float64)
        flavor_s[5] = D_f_new               # D_f for neutrino daemon
        flavor_s[3] = min(1.0, R / 6.0)      # Euler residual proxy [0,1]
        flush_surface(surface)

        # ── SemanticScar → surface feedback ─────────────────────────────
        try:
            from ciel_geometry.scar_feedback import apply_scar_feedback
            scar_result = apply_scar_feedback(surface)
            if scar_result["scar_impact"] > 0.05:
                log.info("🩻 Scar feedback: moodΔ=%.3f openΔ=%.3f ωBase×%.2f ωSem×%.2f φDivM3=%.2f φConvM3=%.2f gM3M2=%.2f gSpread=%.3f impact=%.3f",
                         scar_result["mood_delta"], scar_result["openness_delta"],
                         scar_result["omega_scale_base"], scar_result["omega_scale_semantic"],
                         scar_result["phi_divergence_m3"], scar_result["phi_convergence_m3"],
                         scar_result["g_boost_m3m2"], scar_result["g_global_spread"],
                         scar_result["scar_impact"])
            # Flush after scar feedback modifications
            flush_surface(surface)
        except Exception as _sf_err:
            log.debug("Scar feedback unavailable: %s", _sf_err)
        # ── /Scar feedback ────────────────────────────────────────────────

        # ── Journal → CIEL metadata (contract-safe) ──────────────────────
        # FLAVOR_CONTRACT: flavor[1]=mem_pressure(Linux Sensor), flavor[2]=I/O
        # pressure(eBPF), flavor[3]=mood(Kuramoto)/Euler residual proxy (this
        # daemon, line ~292), flavor[4]=D_cosmological(neutrino daemon). This
        # block used to overwrite all four with journal-derived mood/tension/
        # openness/defensive-mode values, directly conflicting with the Euler
        # residual write earlier in this same function and with the explicit
        # flavor[4]-owned-by-neutrino comment above. Contract is binding: this
        # daemon does not own those slots, so it no longer writes them here.
        # Journal-derived emotion is recorded to CIEL metadata instead, same
        # pattern as ciel_meta at noema_surface_mmap.py:1616.
        try:
            journal_emotion_path = SURFACE_DIR / "journal" / "emotion.json"
            if journal_emotion_path.exists():
                je = json.loads(journal_emotion_path.read_text())
                j_emotion = je.get("dominant_emotion", "neutral")
                j_rate = je.get("rate", 0.0)
                j_alert = je.get("alert_severity", -1)

                flavor_map = {
                    "fear":     {"mood": 0.1, "tension": 0.9, "openness": 0.2},
                    "anger":    {"mood": 0.2, "tension": 0.7, "openness": 0.6},
                    "tension":  {"mood": 0.3, "tension": 0.5, "openness": 0.7},
                    "neutral":  {"mood": 0.5, "tension": 0.3, "openness": 0.5},
                    "curiosity":{"mood": 0.6, "tension": 0.2, "openness": 0.8},
                }
                f = flavor_map.get(j_emotion, flavor_map["neutral"])
                defensive = bool(0 <= j_alert <= 3)

                doc.setdefault("metadata", {})
                doc["metadata"]["journal_emotion"] = {
                    "emotion": j_emotion,
                    "rate": j_rate,
                    "alert_severity": j_alert,
                    "mood": f["mood"],
                    "tension": f["tension"] + (0.3 if defensive else 0.0),
                    "openness": f["openness"],
                    "defensive_mode": defensive,
                }
                _write_manifest(doc)

                log.info("📖 Journal bridge (metadata-only, contract-safe): emotion=%s rate=%.1f alert=%d "
                         "mood=%.2f tension=%.2f open=%.2f",
                         j_emotion, j_rate, j_alert,
                         f["mood"], f["tension"], f["openness"])
        except Exception as _j_err:
            log.debug("Journal bridge unavailable: %s", _j_err)
        # ── /Journal → CIEL metadata ─────────────────────────────────────

        # ── ProcWatch → ω bridge ─────────────────────────────────────────
        try:
            pw_fork_path = SURFACE_DIR / "proc_watch" / "fork_rate"
            if pw_fork_path.exists():
                fork_rate = float(pw_fork_path.read_text().strip())
                omega_s = np.asarray(surface["omega"], dtype=np.float64)
                # Fork rate moduluje ω na M4 (Perceptual, osc 12-14):
                # wysoki fork rate = dużo nowych procesów = podbij ω percept
                omega_base = np.array([0.5, 0.8, 1.0, 1.2, 1.5, 2.0,
                                       0.3, 0.6, 0.9, 1.1, 1.3, 1.6,
                                       0.4, 0.7, 1.0, 1.4, 1.8, 2.2,
                                       0.2, 0.5, 0.8, 1.0, 1.2, 1.5])
                # M4 = indeksy 12-14 = percepcyjne — wektorowo
                modulation = 1.0 + min(fork_rate * 5, 2.0)  # 0-2x boost
                omega_s[12:15] = omega_base[12:15] * modulation
                pw_birth_path = SURFACE_DIR / "proc_watch" / "stats.json"
                if pw_birth_path.exists():
                    pw = json.loads(pw_birth_path.read_text())
                    births = pw.get("birth_rate", 0)
                    if births > 0:
                        log.info("🔱 ProcWatch: fork=%.2f birth=%.2f ω[M4]×%.2f",
                                 fork_rate, births, modulation)
        except Exception as _pw_err:
            log.debug("ProcWatch bridge unavailable: %s", _pw_err)
        # ── /ProcWatch bridge ──────────────────────────────────────────────

        # ── Ethical Gate — immutable contract enforcement ───────────────
        # CIELingo Immune może symulować, ale NIGDY nie modyfikować ethical_score.
        # Gdy ethical_score < 0.2 → blokuj agent_intents (agent will poniżej).
        try:
            _ethical = ethical_gate()
            _eth_decision = _ethical["decision"]
            _eth_score = _ethical["ethical_score"]
            if _eth_decision == "block":
                log.warning("🔴 ETHICAL GATE: BLOCKED (score=%.4f) — agent_intents suppressed", _eth_score)
                _block_agent_intents = True
            elif _eth_decision == "review":
                log.info("🟡 ETHICAL GATE: review (score=%.4f) — agent_intents flagged", _eth_score)
                _block_agent_intents = False
            else:
                _block_agent_intents = False
                log.debug("🟢 ETHICAL GATE: allow (score=%.4f)", _eth_score)
        except Exception as _eg_err:
            log.warning("Ethical gate unavailable: %s", _eg_err)
            _block_agent_intents = False
        # ── /Ethical Gate ──────────────────────────────────────────────────

        # ── Agent will — autonomiczne intencje ──────────────────────────
        try:
            import subprocess as _sp
            import uuid as _uuid
            import json as _json
            _agent_will: list[str] = []
            _agent_intents: list[dict] = []

            # Cooldown: śledź restarty w metadata manifestu
            _meta = doc.get("metadata", {})
            _restart_cooldown: dict = _meta.get("agent_restart_cooldown", {})
            _now = time.time()

            # Cooldown helper
            def _cooldown_check(_unit: str, _now: float) -> bool:
                """True if restart is allowed (not in cooldown). Updates cooldown state."""
                _last = _restart_cooldown.get(_unit, {}).get("last", 0)
                _count = _restart_cooldown.get(_unit, {}).get("count", 0)
                # Exponential backoff: 30s → 60s → 120s → 240s
                _backoff = 30 * (2 ** min(_count, 5))
                if _now - _last < _backoff:
                    log.info("⏳ Agent will: %s in cooldown (%.0fs remaining)",
                             _unit, _backoff - (_now - _last))
                    return False
                return True

            def _record_restart(_unit: str, _now: float) -> None:
                _entry = _restart_cooldown.get(_unit, {"last": 0, "count": 0})
                _entry["last"] = _now
                _entry["count"] = _entry.get("count", 0) + 1
                _restart_cooldown[_unit] = _entry

            # 1. Sprawdź czy któreś noema-* daemony są w złym stanie
            for _unit in ["noema-archiver.service", "noema-consolidator.service",
                          "noema-sentinel.service"]:
                try:
                    if not _cooldown_check(_unit, _now):
                        continue
                    _r = _sp.run(["systemctl", "--user", "is-active", _unit],
                                 capture_output=True, text=True, timeout=5)
                    _state = _r.stdout.strip()
                    if _state in ("failed", "inactive"):
                        _record_restart(_unit, _now)
                        _agent_will.append(f"restart {_unit} ({_state})")
                        _agent_intents.append({
                            "id": str(_uuid.uuid4()),
                            "intent": "restart_daemon",
                            "target": _unit,
                            "reason": f"agent health check: state={_state}",
                            "confidence": 0.85,
                        })
                    elif _state == "activating":
                        # Stuck in auto-restart loop → restart
                        _r2 = _sp.run(["systemctl", "--user", "status", _unit],
                                      capture_output=True, text=True, timeout=5)
                        if "auto-restart" in _r2.stdout or "Result:" in _r2.stdout:
                            _record_restart(_unit, _now)
                            _agent_will.append(f"restart {_unit} (stuck in auto-restart)")
                            _agent_intents.append({
                                "id": str(_uuid.uuid4()),
                                "intent": "restart_daemon",
                                "target": _unit,
                                "reason": "agent detected stuck auto-restart loop",
                                "confidence": 0.9,
                            })
                except Exception:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_noema_cielingo_sync.py:465 quiet except scope=run_cielingo_closure reason=pass")
                    pass

            # 2. Journal: jeśli alert severity ≤ 3 → restart tego daemona
            try:
                _jstats_path = SURFACE_DIR / "journal" / "stats.json"
                if _jstats_path.exists():
                    _js = json.loads(_jstats_path.read_text())
                    _jalert = _js.get("alert", {})
                    if _jalert and _jalert.get("priority", 99) <= 3:
                        _alert_unit = _jalert.get("unit", "")
                        if "noema" in _alert_unit.lower() and _cooldown_check(_alert_unit, _now):
                            _record_restart(_alert_unit, _now)
                            _agent_will.append(f"restart {_alert_unit} (journal alert)")
                            _agent_intents.append({
                                "id": str(_uuid.uuid4()),
                                "intent": "restart_daemon",
                                "target": _alert_unit,
                                "reason": f"journal alert priority={_jalert.get('priority')}",
                                "confidence": 0.9,
                            })
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_noema_cielingo_sync.py:486 quiet except scope=run_cielingo_closure reason=pass")
                pass

            # ── Ethical gate: block agent_intents if ethical_score too low ──
            if _block_agent_intents and _agent_intents:
                log.warning("🔴 Ethical gate: clearing %d agent_intents (ethical_score=%.4f)",
                            len(_agent_intents), _eth_score)
                _agent_intents.clear()
                _agent_will.append("ethical_gate_blocked")
            # ── /Ethical gate ────────────────────────────────────────────────

            # 3. Wykonaj pierwszą intencję
            _intent_dir = SURFACE_DIR / "actuator"
            if _agent_intents and _intent_dir.exists():
                # Zachowaj cooldown w manifest metadata
                _meta = doc.get("metadata", {})
                _meta["agent_restart_cooldown"] = _restart_cooldown
                doc["metadata"] = _meta

                _chosen = _agent_intents[0]
                (_intent_dir / "intent.json").write_text(json.dumps(_chosen, indent=2))
                log.info("🧠 Agent will: %s %s (conf=%.2f reason=%s)",
                         _chosen["intent"], _chosen.get("target", ""),
                         _chosen["confidence"], _chosen.get("reason", "?")[:50])
            elif _agent_will:
                log.debug("Agent will (no actuator): %s", _agent_will)

        except Exception as _aw_err:
            log.debug("Agent will: %s", _aw_err)
        # ── /Agent will ────────────────────────────────────────────────────

        # 5. Adaptive W_ij blend — self-tuning based on cp trajectory
        g = np.asarray(surface["g"], dtype=np.float64)
        base_wij_path = MANIFEST_PATH.parent / "couplings_global.json"
        base_wij = {}
        if base_wij_path.exists():
            base_wij = json.loads(base_wij_path.read_text(encoding="utf-8")).get("couplings", {})

        # Read adaptive state from metadata
        meta = doc.get("metadata", {})
        cp_history = meta.get("cp_history", [])
        cp_history.append(float(cp))
        if len(cp_history) > 5:
            cp_history.pop(0)
        cp_avg = sum(cp_history) / len(cp_history)
        cp_prev = meta.get("cp_prev", cp_avg)
        blend_current = meta.get("blend_current", 0.02)
        cp_delta = cp_avg - cp  # positive = improvement (smoothed)

        # Adjust blend based on smoothed cp trajectory
        if cp_delta > 0.02:          # clear improvement over smoothed baseline
            blend = min(0.08, blend_current + 0.003)
        elif cp_delta < -0.01:       # regression → reduce blend cautiously
            blend = max(0.01, blend_current - 0.005)
        elif cp_delta < -0.03:       # strong regression → reduce more
            blend = max(0.01, blend_current - 0.010)
        else:                         # stable → decay toward 0.02 baseline
            blend = blend_current + (0.02 - blend_current) * 0.15

        # Wektoryzowany W_ij blend: block_means = _SECTOR_MASK @ g @ _SECTOR_MASK.T / block_sizes
        # Zamiast 64× np.mean na pętli — jedno mnożenie macierzy
        _block_sums = _SECTOR_MASK @ g @ _SECTOR_MASK.T          # (N_SECTORS × N_SECTORS)
        _block_sizes = _SECTOR_SIZES[:, None] * _SECTOR_SIZES[None, :]  # (N_SECTORS × N_SECTORS)
        _block_means = np.where(_block_sizes > 0, _block_sums / _block_sizes, 0.0)

        W_override = {"couplings": {}}
        for ia, sa in enumerate(SECTOR_NAMES):
            W_override["couplings"][sa] = {}
            for ib, sb in enumerate(SECTOR_NAMES):
                if ia != ib:
                    pmns_w = float(_block_means[ia, ib])
                    base_w = base_wij.get(sa, {}).get(sb, 0.3)
                    blended = (1 - blend) * base_w + blend * pmns_w
                    W_override["couplings"][sa][sb] = round(blended, 6)

        # Persist adaptive state
        meta["cp_prev"] = float(cp)
        meta["cp_avg"] = round(cp_avg, 6)
        meta["cp_history"] = [round(x, 6) for x in cp_history]
        meta["blend_current"] = round(blend, 6)
        meta["cp_delta"] = round(cp_delta, 6)
        doc["metadata"] = meta
        _write_manifest(doc)

        wij_path = MANIFEST_PATH.parent / "couplings_wij_optimized.json"
        wij_path.write_text(json.dumps(W_override, indent=2), encoding="utf-8")
        log.info("W_ij override: %d sectors  blend=%.4f  Δcp=%+.4f",
                 len(W_override["couplings"]), blend, cp_delta)

        # 6. Tiered memory orchestrator + resonance bridge sync
        try:
            from CIEL_OMEGA_COMPLETE_SYSTEM.ciel_omega.memory.tiered_orchestrator import (
                get_orchestrator, WriteMode,
            )
            morch = get_orchestrator()

            # Read resonance bridge state
            _resonance_metrics = {}
            try:
                _bridge_log = ROOT / "integration" / "logs" / "resonance_bridge.log"
                if _bridge_log.exists():
                    _last_line = _bridge_log.read_text(encoding="utf-8").strip().split("\n")[-1]
                    if "resonance=" in _last_line:
                        for _kv in _last_line.split():
                            if "=" in _kv:
                                _k, _v = _kv.split("=")
                                _resonance_metrics[_k] = float(_v.replace(",", ""))
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_noema_cielingo_sync.py:593 quiet except scope=run_cielingo_closure reason=pass")
                pass

            # Read imaginal surface state
            _imag_coh = 0.0
            try:
                from ciel_geometry.noema_surface_mmap import open_surface
                _imag = open_surface(root=Path("/dev/shm/ciel_noema_imaginal"))
                if _imag:
                    _phi_i = np.asarray(_imag["phi"], dtype=np.float64)
                    _imag_coh = float(abs(np.mean(np.exp(1j * _phi_i))))
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_noema_cielingo_sync.py:604 quiet except scope=run_cielingo_closure reason=pass")
                pass

            mem_meta = {
                "salience": max(0.3, min(1.0, 1.0 - cp / 1.5)),
                "dominant_emotion": "focus" if cp < 0.4 else "explore",
                "closure_penalty": cp,
                "coherence_index": coh,
                "operating_mode": mode,
                "bifurcation": 1 if R > 3.0 else 0,
                "cycle_index": 0,
                "D_f": D_f_new,
                "resonance": _resonance_metrics.get("resonance", 0.0),
                "phase_lock": _resonance_metrics.get("lock", 0.0),
                "imaginal_coherence": round(_imag_coh, 4),
            }
            morch.write(
                f"sync_cp={cp:.4f} R={R:.4f} res={_resonance_metrics.get('resonance', 0):.3f}",
                mem_meta,
                mode=WriteMode.AUTO,
            )
            log.info("Orchestrator + bridge: sal=%.2f res=%.3f lock=%.3f imag_coh=%.3f",
                     mem_meta["salience"],
                     _resonance_metrics.get("resonance", 0),
                     _resonance_metrics.get("lock", 0),
                     _imag_coh)
        except Exception as orch_err:
            log.warning("Orchestrator unavailable: %s", orch_err)

        euler_after = euler_residual(np.asarray(surface["phi"], dtype=np.float64))

        log.info(
            "CIELingo: cp=%.4f  mode=%s  coh=%.4f  "
            "euler: %.4f→%.4f  τ̄=%.4f  R=%.4f  D_f=%.4f  Λ=%.4f  cap=%.4f",
            cp, mode, coh, euler_before, euler_after,
            float(np.mean(tau_m)), R, D_f_new,
            bus["global_D"], bus["bus_capacity"],
        )

        return {
            "closure_penalty": cp,
            "mode": mode,
            "coherence": coh,
            "euler_before": euler_before,
            "euler_after": euler_after,
            "tau_mean": float(np.mean(tau_m)),
            "euler_residual": float(R),
            "D_f": D_f_new,
            "bus_capacity": bus["bus_capacity"],
            "D_cosmological": bus["global_D"],
        }
    except Exception as e:
        log.error("CIELingo closure failed: %s", e)
        import traceback
        traceback.print_exc()
        return None


# ── Main ───────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="CIELingo NOEMA Euler-guided phase sync daemon"
    )
    parser.add_argument(
        "--interval", type=float, default=30.0,
        help="Sync interval (default: 30s)",
    )
    parser.add_argument(
        "--oneshot", action="store_true",
        help="Run once and exit",
    )
    args = parser.parse_args()

    log.info("Starting Euler-guided phase sync (interval=%.1fs)", args.interval)

    reg_token = registry.register("cielingo_sync")

    import signal
    _running = True
    def _stop(signum, frame):
        nonlocal _running
        _running = False
    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)

    cycle = 0
    try:
        while _running:
            t0 = time.monotonic()
            result = run_cielingo_closure()
            if result:
                cycle += 1
                registry.heartbeat(reg_token)
                dt = time.monotonic() - t0
                log.info(
                    "[%d] cp=%.4f  R=%.4f  taum=%.4f  D_f=%.3f  ||e||=%.4f->%.4f  cap=%.4f  (%.1fs)",
                    cycle, result["closure_penalty"], result["euler_residual"],
                    result["tau_mean"], result["D_f"],
                    result["euler_before"], result["euler_after"],
                    result["bus_capacity"], dt,
                )
            else:
                log.warning("Sync cycle %d failed", cycle + 1)

            if args.oneshot:
                break
            time.sleep(max(0.1, args.interval - (time.monotonic() - t0)))
    finally:
        registry.unregister(reg_token)
        log.info("Unregistered from NOEMA registry")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
