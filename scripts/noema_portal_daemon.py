#!/usr/bin/env python3
"""NOEMA Portal Daemon — żywy interfejs systemu NOEMA.

Zamiast surowego python3 -m http.server:
  - Rejestracja w daemon registry + heartbeat
  - Surface mmap przez ensure_surface()
  - REST API: /api/live, /api/status, /api/health, /api/metrics/all
  - Serwuje pliki statyczne z site/ na 18888
  - Systemd: noema-portal.service

Usage:
  noema_portal_daemon.py [--port PORT]
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

# CIEL ORBITAL BINDING — daemon bound
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on daemon " + __name__)


import http.server
import json
import os
import signal
import sys
import time
import threading
from pathlib import Path
from typing import Any

from ciel_geometry.noema_registry import registry as nreg
from ciel_geometry.paths import P as _P

# Was hardcoded /tmp/{noema_knowledge,noema_taskplan}.db (tmpfs, wiped on
# reboot) — fixed 2026-07-08.
_KNOWLEDGE_DB_PATH = str(_P.DB.KNOWLEDGE)
_TASKPLAN_DB_PATH = str(_P.DB.TASKPLAN)

# ── Ścieżki ────────────────────────────────────────────────────────────
NOEMA_ROOT = Path(__file__).resolve().parent.parent
SITE_ROOT = NOEMA_ROOT / "site"
PORT = int(os.environ.get("NOEMA_PORTAL_PORT", "18888"))

# ciel_omega lives under src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega, one level
# deeper than src/ciel_geometry — that extra directory was never added to
# sys.path, so `from ciel_omega.memory import ...` failed with
# "No module named 'ciel_omega'" even though src/ itself was already on path.
_CIEL_OMEGA_PARENT = NOEMA_ROOT / "src" / "CIEL_OMEGA_COMPLETE_SYSTEM"
if _CIEL_OMEGA_PARENT.is_dir() and str(_CIEL_OMEGA_PARENT) not in sys.path:
    sys.path.insert(0, str(_CIEL_OMEGA_PARENT))

# ─── Stan globalny ──────────────────────────────────────────────────────
surface: dict[str, Any] | None = None
reg_token: Any = None
start_time: float = 0.0

# ─── Embedding cache (ładowane raz, nie per request) ───────────────────
_EMBED_CACHE: dict = {}  # {"embeddings": ndarray, "index": dict, "loaded": bool}
def _get_embeddings():
    """Lazy-load embeddings cache — pierwsze wywołanie ładuje, potem cache."""
    if _EMBED_CACHE.get("loaded"):
        return _EMBED_CACHE["embeddings"], _EMBED_CACHE["index"]
    import numpy as np
    embed_npy = Path("/tmp/noema_knowledge_embeddings.npy")
    embed_json = Path("/tmp/noema_knowledge_embeddings.json")
    if not embed_npy.exists() or not embed_json.exists():
        return None, None
    _EMBED_CACHE["embeddings"] = np.load(str(embed_npy))
    with open(embed_json) as f:
        _EMBED_CACHE["index"] = json.load(f)
    _EMBED_CACHE["loaded"] = True
    return _EMBED_CACHE["embeddings"], _EMBED_CACHE["index"]

# ─── Inicjalizacja NOEMA ───────────────────────────────────────────────

def init_noema() -> dict[str, Any]:
    """Inicjalizuje połączenie z NOEMA: surface + registry."""
    global surface
    try:
        from ciel_geometry.noema_surface_mmap import ensure_surface, read_surface_state
        surface = ensure_surface(zero_fill=False)
        state = read_surface_state(surface)
        print(f"[portal] surface OK: tick={state.get('tick')} coh={state.get('coherence',0):.3f}")
        return state
    except Exception as e:
        print(f"[portal] surface init failed: {e}", file=sys.stderr)
        return {}

def read_surface_value(key: str, default: Any = 0) -> Any:
    """Czyta pojedyńczą wartość z surface mmap."""
    global surface
    try:
        if surface is None:
            init_noema()
        from ciel_geometry.noema_surface_mmap import read_surface_state
        if surface:
            state = read_surface_state(surface)
            return state.get(key, default)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:87 quiet except scope=read_surface_value reason=pass")
        pass
    return default

def read_mmap_array(name: str) -> list | None:
    """Czyta tablicę numpy z surface mmap po nazwie pola."""
    try:
        if surface is None:
            init_noema()
        if surface and name in surface:
            arr = surface[name]
            if hasattr(arr, "tolist"):
                return arr.tolist()
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:100 quiet except scope=read_mmap_array reason=pass")
        pass
    return None

def _read_analog_bus() -> dict[str, Any]:
    """Czyta PhaseNav analog bus — hot/cold phi, temp, resonance, writing."""
    try:
        import numpy as np
        analog_root = Path("/dev/shm/ciel_noema/analog")
        bus: dict[str, Any] = {}
        # pola float64[36]
        for name, size in [("phi_hot", 36), ("phi_cold", 36), ("writing_phi", 36)]:
            p = analog_root / name
            if p.exists() and p.stat().st_size >= size * 8:
                arr = np.memmap(p, dtype=np.float64, mode="r", shape=(size,))
                bus[name] = arr.tolist()
        # pola float64[1]
        for name in ["temp", "resonance"]:
            p = analog_root / name
            if p.exists() and p.stat().st_size >= 8:
                arr = np.memmap(p, dtype=np.float64, mode="r", shape=(1,))
                bus[name] = float(arr[0])
        # writing_meta.json
        wm = analog_root / "writing_meta.json"
        if wm.exists():
            with open(wm) as f:
                bus["writing_meta"] = json.load(f)
        # tick
        tick_p = analog_root / "tick"
        if tick_p.exists() and tick_p.stat().st_size >= 8:
            arr = np.memmap(tick_p, dtype=np.uint64, mode="r", shape=(1,))
            bus["tick"] = int(arr[0])
        return bus
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:133 quiet except scope=_read_analog_bus reason=return {\"error\": str(e)}")
        return {"error": str(e)}

def _read_ciel_state() -> dict[str, Any]:
    """Czyta CIEL state JSON z surface."""
    try:
        path = Path("/dev/shm/ciel_noema/ciel_state.json")
        if path.exists():
            with open(path) as f:
                return json.load(f)
        return {"error": "not found"}
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:144 quiet except scope=_read_ciel_state reason=return {\"error\": str(e)}")
        return {"error": str(e)}

def _read_agent_hint() -> dict[str, Any]:
    """Czyta agent_hint z surface."""
    try:
        path = Path("/dev/shm/ciel_noema/agent_hint")
        if path.exists():
            raw = path.read_text()
            return json.loads(raw)
        return {"error": "not found"}
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:155 quiet except scope=_read_agent_hint reason=return {\"error\": str(e)}")
        return {"error": str(e)}

def _read_linux_load() -> float:
    """Czyta linux_load z surface."""
    try:
        import numpy as np
        path = Path("/dev/shm/ciel_noema/linux_load")
        if path.exists() and path.stat().st_size >= 8:
            arr = np.memmap(path, dtype=np.float64, mode="r", shape=(1,))
            return float(arr[0])
        return 0.0
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:167 quiet except scope=_read_linux_load reason=return 0.0")
        return 0.0

_SKILLS_CATALOG_CACHE: dict[str, Any] = {"mtime": 0.0, "result": None}

def _skills_catalog_count() -> dict[str, Any]:
    """Policz prawdziwy katalog skilli z SKILLS.md (SK-XXX entries).

    Cache'owane po mtime pliku — SKILLS.md rośnie rzadko, nie ma potrzeby
    parsować 750+ linii przy każdym /api/status/summary.
    """
    path = NOEMA_ROOT / "SKILLS.md"
    if not path.exists():
        return {"total": 0, "error": "SKILLS.md not found"}
    mtime = path.stat().st_mtime
    if _SKILLS_CATALOG_CACHE["mtime"] == mtime and _SKILLS_CATALOG_CACHE["result"] is not None:
        return _SKILLS_CATALOG_CACHE["result"]

    import re
    seen: set[str] = set()
    by_type: dict[str, int] = {}
    by_status: dict[str, int] = {}
    row_re = re.compile(r"^\|\s*(SK-\d+)\s*\|\s*`([^`]+)`\s*\|\s*([A-Z]+)\s*\|.*\|\s*(stable|draft|referenced|stub)\s*\|")
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = row_re.match(line)
        if not m:
            continue
        sk_id = m.group(1)
        if sk_id in seen:
            continue
        seen.add(sk_id)
        typ = m.group(3)
        status = m.group(4)
        by_type[typ] = by_type.get(typ, 0) + 1
        by_status[status] = by_status.get(status, 0) + 1

    result = {"total": len(seen), "by_type": by_type, "by_status": by_status, "source": "SKILLS.md"}
    _SKILLS_CATALOG_CACHE["mtime"] = mtime
    _SKILLS_CATALOG_CACHE["result"] = result
    return result

def _read_cards_index() -> dict[str, Any]:
    """Czyta system_map_v2.json i zwraca karty/systemy NOEMA."""
    try:
        path = Path(__file__).resolve().parent.parent / "system_map_v2.json"
        if path.exists():
            with open(path) as f:
                data = json.load(f)
            systems = data.get("systems", [])
            return {
                "total_systems": len(systems),
                "total_daemons": data.get("total_daemons", 0),
                "total_connections": data.get("total_connections", 0),
                "systems": systems,
                "version": data.get("version", ""),
                "date": data.get("date", ""),
            }
        return {"error": "system_map_v2.json not found"}
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:187 quiet except scope=_read_cards_index reason=return {\"error\": str(e)}")
        return {"error": str(e)}

def _read_gravity() -> dict[str, float]:
    """Czyta gravity z mmap bezpośrednio (omija read_surface_state)."""
    try:
        grav = read_mmap_array("gravity")
        if grav and len(grav) >= 4:
            return {
                "semantic_density": float(grav[0]),
                "tau_dilation": float(grav[1]),
                "mass_total": float(grav[2]),
                "unruh_power": float(grav[3]),
            }
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:201 quiet except scope=_read_gravity reason=pass")
        pass
    return {"semantic_density": 0, "tau_dilation": 0, "mass_total": 0, "unruh_power": 0}

def build_bloch_payload() -> dict[str, Any]:
    """Full 36D NOEMA state — wszystkie atrybuty, numpy vectorized.

    Zwraca:
    - 36 nodes (phi, omega, tau, sensor, R_geom, psi_geom, Z_geom, dphi/dt)
    - 36×36 coupling matrix g (top 72 edges)
    - 6 flavor slots, 4 gravity, 7 holonomy
    - Analog bus (phi_hot, phi_cold, writing_phi)
    - CIEL state, agent_hint, linux_load
    - Operator PhaseNav, tick, metadata
    """
    import numpy as np
    from ciel_geometry.phasenav.operator_algebra import ALL_OPERATOR_IDS, VECTOR_COMPONENTS

    if surface is None:
        init_noema()
    if not surface:
        return {"status": "error", "error": "surface unavailable"}

    # ── 1. Wczytaj wszystkie surface arrays ──
    def _read_1d(name: str, n: int = 36) -> np.ndarray:
        try:
            arr = np.asarray(surface[name], dtype=np.float64).ravel()
            if len(arr) >= n:
                return arr[:n]
            return np.pad(arr, (0, n - len(arr)))
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:231 quiet except scope=build_bloch_payload._read_1d reason=return np.zeros(n, dtype=np.float64)")
            return np.zeros(n, dtype=np.float64)

    n = 36
    phi = _read_1d("phi", n)
    omega = _read_1d("omega", n)
    tau = _read_1d("tau", n)
    sensor = _read_1d("sensor_raw", n)
    r_geom = _read_1d("R_geom", n)
    psi_geom = _read_1d("psi_geom", n)
    Z_geom = _read_1d("Z_geom", n)

    # G (36×36)
    try:
        g = np.asarray(surface["g"], dtype=np.float64)[:n, :n]
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:246 quiet except scope=build_bloch_payload reason=assign_fallback")
        g = np.zeros((n, n), dtype=np.float64)

    # Flavor (6), Gravity (4), Holonomy (7)
    flavor = _read_1d("flavor", 6)
    gravity_arr = _read_1d("gravity", 4)
    holonomy_arr = _read_1d("holonomy", 7)

    # Tick
    try:
        tick_val = int(np.asarray(surface.get("tick", [0]), dtype=np.uint64).ravel()[0])
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:257 quiet except scope=build_bloch_payload reason=assign_fallback")
        tick_val = -1

    # ── 2. Wektoryzowane obliczenia Bloch (numpy, zero pętli) ──
    phase_diff = phi[None, :] - phi[:, None]                   # (36,36)
    coupling_flow = np.sum(g * np.sin(phase_diff), axis=1) / max(1, n)  # (36,)

    info_energy = np.abs(omega) + np.abs(coupling_flow) + 0.15 * np.abs(sensor)
    max_energy = max(float(np.max(info_energy)), 1e-12)
    energy_norm = np.clip(info_energy / max_energy, 0.0, 1.0)
    tau_norm = np.clip(tau, 0.0, 1.0)
    sensor_norm = np.tanh(np.abs(sensor))

    # Pozycje na sferze Blocha — wszystko wektorowo
    z = np.clip((tau_norm - 0.5) * 1.2 + np.tanh(coupling_flow) * 0.45 + sensor_norm * 0.20, -0.98, 0.98)
    radius_xy = np.sqrt(np.maximum(0.0, 1.0 - z * z))
    x = radius_xy * np.cos(phi)
    y = radius_xy * np.sin(phi)

    # Flow vectors (dφ/dt)
    dphi = omega + coupling_flow
    vx = -np.sin(phi) * dphi * 0.10
    vy = np.cos(phi) * dphi * 0.10
    vz = np.tanh(coupling_flow) * 0.08

    # ── 3. Krawędzie (top 72 z g) ──
    abs_g = np.abs(g.copy())
    np.fill_diagonal(abs_g, 0.0)
    flat_idx = np.argsort(abs_g.ravel())[::-1]
    edges = []
    seen: set[tuple[int, int]] = set()
    for idx in flat_idx:
        a = int(idx // n)
        b = int(idx % n)
        if a == b or (b, a) in seen:
            continue
        w = float(g[a, b])
        if abs(w) <= 1e-9:
            continue
        seen.add((a, b))
        edges.append({"from": a, "to": b, "weight": round(w, 6), "abs_weight": round(abs(w), 6)})
        if len(edges) >= 72:
            break

    # ── 4. Punkty + wektory + program (36 iteracji — OK dla 36, strukturalnie potrzebne) ──
    supergroups = ["M0_ID", "M1_AGENT", "M2_MEMORY", "M3_SEM", "M4_LOGIC", "M5_AFFECT", "M6_REL", "M7_TIME", "M8_META"]
    colors = ["#00d4ff", "#8844ff", "#44ff88", "#ffb347", "#ff4466", "#ff88cc", "#44ddff", "#aaff44", "#ffffff"]
    ch_indices = np.arange(n) // 4

    points = []
    vectors_ret = []
    program = []
    for i in range(n):
        sg = int(ch_indices[i])
        op = ALL_OPERATOR_IDS[i] if i < len(ALL_OPERATOR_IDS) else f"OP_{i}"
        comp = VECTOR_COMPONENTS[i] if i < len(VECTOR_COMPONENTS) else "v"

        points.append({
            "idx": i, "id": f"φ[{i:02d}]", "operator": op, "component": comp,
            "supergroup": supergroups[min(sg, len(supergroups)-1)], "ch": sg,
            "color": colors[min(sg, len(colors)-1)],
            "x": round(float(x[i]), 6), "y": round(float(y[i]), 6), "z": round(float(z[i]), 6),
            "phi": round(float(phi[i]), 6), "omega": round(float(omega[i]), 6),
            "tau": round(float(tau[i]), 6), "sensor": round(float(sensor[i]), 6),
            "coupling_flow": round(float(coupling_flow[i]), 6),
            "energy": round(float(energy_norm[i]), 6),
            "R": round(float(max(0.12, energy_norm[i])), 6),
            "r_geom": round(float(r_geom[i]), 6), "psi_geom": round(float(psi_geom[i]), 6),
            "Z_geom": round(float(Z_geom[i]), 6),
        })
        vectors_ret.append({
            "from": i,
            "x": round(float(vx[i]), 6), "y": round(float(vy[i]), 6), "z": round(float(vz[i]), 6),
            "magnitude": round(float(abs(dphi[i])), 6),
            "meaning": "dφ/dt = ω + Σ gᵢⱼ sin(φⱼ-φᵢ)",
        })
        program.append({
            "step": i, "op": op, "component": comp,
            "vector": [round(float(x[i]), 6), round(float(y[i]), 6), round(float(z[i]), 6)],
            "flow": [round(float(vx[i]), 6), round(float(vy[i]), 6), round(float(vz[i]), 6)],
            "exec": "PROJECT_BLOCH ∘ FLOW_FIELD ∘ PHASENAV_OPERATOR",
        })

    # ── 5. Analog bus ──
    analog = _read_analog_bus()

    # ── 6. CIEL state ──
    ciel_state = _read_ciel_state()

    # ── 7. Agent hint ──
    agent_hint = _read_agent_hint()

    # ── 8. Linux load ──
    linux_load_val = _read_linux_load()

    # ── 9. Operator ──
    try:
        op_path = Path("/dev/shm/ciel_noema/operator")
        operator_val = op_path.read_text().strip() if op_path.exists() else "—"
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:356 quiet except scope=build_bloch_payload reason=assign_fallback")
        operator_val = "—"

    # ── 10. Składanie wyniku ──
    return {
        "status": "ok",
        "source": "NOEMA surface mmap (all 12 arrays) + analog bus + CIEL state",
        "representation": "PhaseNav vector program → Bloch information dynamics",
        "timestamp": time.time(),
        "tick": tick_val,
        "n": n, "dimensions": 36,
        "operator": operator_val,
        "linux_load": linux_load_val,

        # Koherencja — z CIEL state, z R_geom, z flavor[0]
        "coherence": {
            "r_global": float(np.mean(r_geom)) if r_geom.size > 0 else 0,
            "ciel_coherence_index": ciel_state.get("coherence_index", 0),
            "flavor_coherence": float(flavor[0]) if len(flavor) > 0 else 0,
        },
        "omega_mean": round(float(np.mean(omega)), 6),
        "tau_mean": round(float(np.mean(tau)), 6),
        "info_energy_mean": round(float(np.mean(energy_norm)), 6),
        "flow_rms": round(float(np.sqrt(np.mean(dphi * dphi))), 6),
        "sensor_mean": round(float(np.mean(sensor)), 6),
        "phi_var": round(float(np.var(phi)), 6),

        # 36 węzłów
        "points": points,
        # 72 krawędzie coupling
        "edges": edges,
        # Flow vectors
        "vectors": vectors_ret,
        # Program PhaseNav
        "program": program,

        # Dodatkowe atrybuty (NOWE — brakowało wcześniej)
        "flavor": {
            "coherence": float(flavor[0]) if len(flavor) > 0 else 0,
            "mem_pressure": float(flavor[1]) if len(flavor) > 1 else 0,
            "io_pressure": float(flavor[2]) if len(flavor) > 2 else 0,
            "mood": float(flavor[3]) if len(flavor) > 3 else 0,
            "entropy": float(flavor[4]) if len(flavor) > 4 else 0,
            "mode": float(flavor[5]) if len(flavor) > 5 else 0,
            "raw_vector": flavor.tolist(),
        },
        "gravity": {
            "semantic_density": float(gravity_arr[0]) if len(gravity_arr) > 0 else 0,
            "tau_dilation": float(gravity_arr[1]) if len(gravity_arr) > 1 else 0,
            "mass_total": float(gravity_arr[2]) if len(gravity_arr) > 2 else 0,
            "unruh_power": float(gravity_arr[3]) if len(gravity_arr) > 3 else 0,
            "raw_vector": gravity_arr.tolist(),
        },
        "holonomy": {
            "mean_conn": float(holonomy_arr[0]) if len(holonomy_arr) > 0 else 0,
            "gauge_rank": float(holonomy_arr[1]) if len(holonomy_arr) > 1 else 0,
            "closure_score": float(holonomy_arr[2]) if len(holonomy_arr) > 2 else 0,
            "surface_gamma": float(holonomy_arr[3]) if len(holonomy_arr) > 3 else 0,
            "max_conn": float(holonomy_arr[4]) if len(holonomy_arr) > 4 else 0,
            "winding": float(holonomy_arr[5]) if len(holonomy_arr) > 5 else 0,
            "curvature": float(holonomy_arr[6]) if len(holonomy_arr) > 6 else 0,
            "raw_vector": holonomy_arr.tolist(),
        },

        # Analog bus
        "analog_bus": analog,

        # CIEL state
        "ciel_state": ciel_state,

        # Agent hint
        "agent_hint": agent_hint,

        # Linux load
        "linux_load_detail": {"load": linux_load_val},

        # Etykieta
        "status_label": "REAL",
        "attributes_labels": ["phi","omega","tau","sensor","R_geom","psi_geom","Z_geom",
                               "flavor","gravity","holonomy","g","analog_bus","ciel_state"],
    }


def build_phasenav_graphics_payload(query: str = "NOEMA", scene_name: str = "surface") -> dict[str, Any]:
    """Build PhaseNav graphics bundle for relational, memory and operator maps."""
    try:
        from ciel_geometry.phasenav.graphics import build_phasenav_graphics_bundle
        bundle = build_phasenav_graphics_bundle(query=query, surface=surface)
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:437 quiet except scope=build_phasenav_graphics_payload reason=return error")
        return {"status": "error", "error": str(e), "query": query, "scene_name": scene_name}

    scenes = bundle.get("scenes", {})
    selected = scenes.get(scene_name) or scenes.get("surface") or {}
    return {
        "status": "ok",
        "source": "PhaseNav graphics composer",
        "query": bundle.get("query", query),
        "surface": bundle.get("surface", {}),
        "scene_name": scene_name,
        "scene_counts": bundle.get("scene_counts", {}),
        "scenes": scenes,
        "scene": selected,
    }

def _metric_entry(
    key: str,
    value: Any,
    *,
    label: str,
    unit: str = "",
    desc: str = "",
    source: str = "surface",
    group: str = "surface",
) -> dict[str, Any]:
    rendered = float(value) if isinstance(value, (int, float)) else value
    return {
        "key": key,
        "label": label,
        "unit": unit,
        "desc": desc,
        "source": source,
        "group": group,
        "value": rendered,
    }


def build_metrics_catalog() -> dict[str, Any]:
    """Kanoniczny katalog metryk wykorzystywany przez dashboard."""
    state = init_noema()
    daemons = scan_registry()
    active_daemons = sum(1 for d in daemons if d.get("alive"))
    portal_uptime_s = round(time.time() - start_time, 1) if start_time else 0.0

    metrics = [
        _metric_entry("tick", state.get("tick", -1), label="Tick", unit="tick",
                      desc="Bieżący cykl powierzchni", source="surface", group="surface"),
        _metric_entry("coherence", state.get("coherence", state.get("coherence_index", 0.0)),
                      label="Koherencja", desc="Globalna synchronizacja układu", source="surface", group="surface"),
        _metric_entry("euler_residual", state.get("euler_residual", 0.0),
                      label="Euler residual", desc="Residual domknięcia fazowego", source="surface", group="surface"),
        _metric_entry("omega_mean", state.get("omega_mean", 0.0),
                      label="ω̄", unit="rad/s", desc="Średnia częstotliwość oscylatorów", source="surface", group="surface"),
        _metric_entry("tau_mean", state.get("tau_mean", 0.0),
                      label="τ̄", unit="s", desc="Średni czas życia / opóźnienie pamięci", source="surface", group="surface"),
        _metric_entry("semantic_density", state.get("semantic_density", 0.0),
                      label="ρ_sem", desc="Gęstość semantyczna powierzchni", source="surface", group="surface"),
        _metric_entry("tau_dilation", state.get("tau_dilation", 0.0),
                      label="γ_τ", desc="Dylatacja czasu lokalnego", source="surface", group="surface"),
        _metric_entry("mass_total", state.get("mass_total", 0.0),
                      label="Masa", desc="Całkowita masa semantyczna", source="surface", group="surface"),
        _metric_entry("unruh_power", state.get("unruh_power", 0.0),
                      label="Unruh", desc="Moc Unruha / napór przyspieszeń", source="surface", group="surface"),
        _metric_entry("mood", state.get("mood", state.get("mood_normalized", 0.0)),
                      label="Nastrój", desc="Stan afektywny systemu", source="ciel", group="ciel"),
        _metric_entry("ethical_score", state.get("ethical_score", 0.0),
                      label="Etyka", desc="Wynik etyczny CIEL", source="ciel", group="ciel"),
        _metric_entry("soul_invariant", state.get("soul_invariant", 0.0),
                      label="Soul invariant", desc="Niezmiennik tożsamości", source="ciel", group="ciel"),
        _metric_entry("daemon_total", len(daemons),
                      label="Daemony", unit="count", desc="Liczba wykrytych daemonów", source="registry", group="system"),
        _metric_entry("daemon_active", active_daemons,
                      label="Aktywne daemony", unit="count", desc="Daemony żywe w registry", source="registry", group="system"),
        _metric_entry("portal_uptime_s", portal_uptime_s,
                      label="Uptime portalu", unit="s", desc="Czas pracy portalu", source="portal", group="portal"),
    ]

    groups: dict[str, list[dict[str, Any]]] = {}
    for metric in metrics:
        groups.setdefault(metric["group"], []).append(metric)

    return {
        "status": "ok",
        "timestamp": time.time(),
        "metrics": metrics,
        "groups": groups,
        "summary": {
            "tick": state.get("tick", -1),
            "coherence": state.get("coherence", state.get("coherence_index", 0.0)),
            "active_daemons": active_daemons,
            "total_daemons": len(daemons),
        },
    }


def build_portal_manifest() -> dict[str, Any]:
    """Mapa architektury portalu i jego źródeł danych."""
    return {
        "status": "ok",
        "version": "portal-manifest/v1",
        "portal": {
            "name": "NOEMA Portal",
            "port": PORT,
            "root": str(SITE_ROOT),
            "description": "Żywy interfejs systemu NOEMA z dashboardem, stanem, pamięcią i CIELingo.",
        },
        "layers": [
            {
                "name": "Surface / Runtime",
                "role": "Bezpośrednie mmap i pamięć współdzielona",
                "sources": ["/dev/shm/ciel_noema/*"],
            },
            {
                "name": "Portal APIs",
                "role": "HTTP warstwa integracyjna portalu",
                "sources": ["/api/live", "/api/status/summary", "/api/metrics", "/api/modules", "/api/portal/manifest", "/api/phasenav/graphics"],
            },
            {
                "name": "Cognition",
                "role": "CIELingo, memory, agent backend, PhaseNav",
                "sources": ["/api/cielingo/chat", "/api/cielingo/thread", "/api/cielingo/analyze", "/api/phasenav/state", "/api/phasenav/graphics"],
            },
            {
                "name": "Knowledge / Tasks",
                "role": "Bazy wiedzy i planów",
                "sources": [_KNOWLEDGE_DB_PATH, _TASKPLAN_DB_PATH, "/api/knowledge/*", "/api/tasks", "/api/plans"],
            },
            {
                "name": "Visualization",
                "role": "Dashboard, status, systems, Bloch, architecture",
                "sources": ["/", "#dashboard", "#status", "#systems", "#memory", "#projects", "#bloch", "#architecture"],
            },
        ],
        "endpoints": [
            {"path": "/api/live", "purpose": "Live surface state"},
            {"path": "/api/metrics", "purpose": "Katalog metryk dla dashboardu"},
            {"path": "/api/modules", "purpose": "Daemon registry"},
            {"path": "/api/status/summary", "purpose": "Podsumowanie systemu"},
            {"path": "/api/portal/manifest", "purpose": "Mapa architektury portalu"},
            {"path": "/api/cielingo/chat", "purpose": "Czat z CIELingo"},
            {"path": "/api/bloch", "purpose": "Sfera Blocha i flow vectors"},
            {"path": "/api/phasenav/graphics", "purpose": "PhaseNav graphics bundle (surface, memory, relations, operators)"},
            {"path": "/api/knowledge/stats", "purpose": "Statystyki knowledge DB"},
            {"path": "/api/tasks", "purpose": "TaskPlan DB"},
        ],
        "pages": [
            {"route": "dashboard", "title": "Dashboard", "purpose": "Szybki widok live",
             "sources": ["/api/live", "/api/metrics", "/api/modules"],
             "notes": "Koło fazowe, metryki, daemon registry."},
            {"route": "cielingo-chat", "title": "CIELingo", "purpose": "Czat i frame analysis",
             "sources": ["/api/cielingo/chat", "/api/cielingo/thread", "/api/cielingo/analyze"],
             "notes": "Rozmowa z CIEL + pamięć sesji."},
            {"route": "status", "title": "Status", "purpose": "Stan systemu i infrastruktura",
             "sources": ["/api/status/summary", "/api/live", "/api/modules", "/api/ciel/state"],
             "notes": "Daemony, surface, CIEL state, IPC."},
            {"route": "systems", "title": "Systemy", "purpose": "Mapa systemów i modułów",
             "sources": ["/api/cards", "/api/modules"],
             "notes": "Grupowanie systemów po typach."},
            {"route": "memory", "title": "Memory", "purpose": "Kanały M0–M11 i wątki CIELingo",
             "sources": ["/api/live", "/api/cielingo/thread"],
             "notes": "Pamięć kanałowa + historia rozmów."},
            {"route": "projects", "title": "Projects", "purpose": "Projekty i zadania",
             "sources": ["/api/cards", "/api/tasks"],
             "notes": "Systemy NOEMA i taski DB."},
            {"route": "phasenav", "title": "PhaseNav", "purpose": "Operator algebra i wizualizacja",
             "sources": ["/api/live", "/api/phasenav/state", "/api/phasenav/graphics", "/api/bloch"],
             "notes": "Program fazowy + surface injection + graphics bundle."},
            {"route": "bloch", "title": "Bloch", "purpose": "Sfera Blocha i vektor programu",
             "sources": ["/api/bloch"],
             "notes": "36 punktów, coupling, flow vectors."},
            {"route": "knowledge", "title": "Knowledge", "purpose": "Graf i wyszukiwarka wiedzy",
             "sources": ["/api/knowledge/stats", "/api/knowledge/search", "/api/knowledge/coverage"],
             "notes": "TF-IDF, affinity, coverage."},
            {"route": "architecture", "title": "Architecture", "purpose": "Mapa przepływu danych",
             "sources": ["/api/portal/manifest", "/api/status/summary"],
             "notes": "Warstwy, zależności, dataflow."},
        ],
        "pipelines": [
            {"from": "/dev/shm/ciel_noema/*", "to": "/api/live", "label": "surface → live cards"},
            {"from": _TASKPLAN_DB_PATH, "to": "/api/status/summary", "label": "TaskPlan timeline"},
            {"from": _KNOWLEDGE_DB_PATH, "to": "/api/knowledge/*", "label": "Knowledge search"},
            {"from": "/dev/shm/ciel_noema/agent_hint", "to": "/api/cielingo/chat", "label": "CIELingo hint loop"},
        ],
    }

# ─── HTTP Handler ───────────────────────────────────────────────────────

MIME_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
}

class PortalHandler(http.server.BaseHTTPRequestHandler):
    """HTTP handler dla NOEMA Portal Daemon."""

    def do_GET(self):
        path = self.path.split("?")[0].rstrip("/")

        # ── API endpoints ──
        if path == "/api/health":
            return self._json({
                "status": "ok",
                "pid": os.getpid(),
                "uptime_s": round(time.time() - start_time, 1),
                "surface_alive": surface is not None,
            })

        if path == "/api/live":
            """Live dashboard data — Kuramoto order parameter per channel, flavor, gravity, CIEL."""
            import numpy as np
            if surface is None:
                init_noema()
            if not surface:
                return self._json({"status": "error", "error": "surface unavailable"})

            def _get_arr(name, n=36):
                try:
                    return np.asarray(surface[name], dtype=np.float64).ravel()
                except Exception:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:477 quiet except scope=PortalHandler.do_GET._get_arr reason=return np.zeros(n)")
                    return np.zeros(n)

            try:
                tick_val = int(np.asarray(surface.get("tick", [0]), dtype=np.uint64).ravel()[0])
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:482 quiet except scope=PortalHandler.do_GET reason=assign_fallback")
                tick_val = -1
            phi_v = _get_arr("phi")
            omega_v = _get_arr("omega")
            tau_v = _get_arr("tau")
            flavor_v = _get_arr("flavor", 6)
            gravity_v = _get_arr("gravity", 4)
            sensor_v = _get_arr("sensor_raw")
            r_geom_v = _get_arr("R_geom")

            # ── Kuramoto global coherence = flavor[0] ──
            kuramoto_coherence = float(flavor_v[0]) if len(flavor_v) > 0 else 0

            # ── Channel coh: Kuramoto order parameter per channel (12 channels × 3) ──
            # R_ch = |(1/N) Σ exp(i·φ_j)| dla j w kanale
            CHANNEL_MAP = {
                "M0_Perceptual":        (0,1,2),
                "M1_Working":           (3,4,5),   # AGENT attractor
                "M2_Episodic":          (6,7,8),
                "M3_Semantic":          (9,10,11),
                "M4_Procedural":        (12,13,14),
                "M5_Affective_Ethical": (15,16,17),
                "M6_Identity":          (18,19,20),
                "M7_Braid_Invariant":   (21,22,23),
                "M8_Meta":              (24,25,26),
                "M9_Temporal":          (27,28,29),
                "M10_Imaginal":         (30,31,32),
                "M11_Quantum":          (33,34,35),
            }
            channel_coh = {}
            for ch_name, idxs in CHANNEL_MAP.items():
                phis = phi_v[list(idxs)]
                # R = |mean(exp(i·φ))|
                complex_mean = np.mean(np.exp(1j * phis))
                channel_coh[ch_name] = round(float(np.abs(complex_mean)), 6)

            # AGENT coherence = M1
            agent_coh = channel_coh.get("M1_Working", 0)

            # ── Flavor bars ──
            FLAVOR_LABELS = ["cp", "coh", "mood", "open", "Λ", "D_f"]
            # flavor[0]=R_coherence, [1]=mem_pressure, [2]=io_pressure, [3]=mood, [4]=entropy, [5]=mode
            # Ale dashboard używa: cp, coh, mood, open, Λ, D_f
            # Mapowanie: cp=R_coherence, coh=mem_pressure(?)
            # Zachowaj oryginalne nazwy dashboardu ale z poprawnymi wartościami:
            flavor_bars = {}
            f_raw = flavor_v.tolist()[:6] if flavor_v.size >= 6 else [0]*6
            for i, label in enumerate(FLAVOR_LABELS):
                flavor_bars[label] = round(float(f_raw[i]), 6)

            # ── Omega / Tau / Phi stats ──
            omega_mean = float(np.mean(omega_v)) if omega_v.size > 0 else 0
            tau_mean = float(np.mean(tau_v)) if tau_v.size > 0 else 0
            phi_mean = float(np.mean(phi_v)) if phi_v.size > 0 else 0
            phi_var = float(np.var(phi_v)) if phi_v.size > 0 else 0

            # ── Gravity ──
            grav = _read_gravity()
            gamma_val = grav.get("tau_dilation", 0)
            mass_val = grav.get("mass_total", 0)
            unruh_val = grav.get("unruh_power", 0)
            density_val = grav.get("semantic_density", 0)

            # ── Sensor ──
            sensor_mean = float(np.mean(sensor_v)) if sensor_v.size > 0 else 0

            # ── Euler residual (Berry phase closure) ──
            # trace of commutator [g, sin(phase_diff)] as proxy
            try:
                g_m = np.asarray(surface["g"], dtype=np.float64)[:36,:36]
                phase_diff = phi_v[:36, None] - phi_v[:36][None, :]
                euler_res = float(np.abs(np.trace(g_m @ np.sin(phase_diff)))) if g_m.size > 0 else 0
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:554 quiet except scope=PortalHandler.do_GET reason=assign_fallback")
                euler_res = 0

            # Backward-compat arrays for dashboard.js (expects array)
            flavor_array = [flavor_bars.get(l, 0) for l in FLAVOR_LABELS[:8]]
            ch_labels_sorted = sorted(channel_coh.keys(), key=lambda x: int(x.split("_")[0][1:]) if x.startswith("M") else 0)
            ch_array = [channel_coh.get(k, 0) for k in ch_labels_sorted]

            return self._json({
                "status": "ok",
                "timestamp": time.time(),
                "tick": tick_val,

                # Primary metrics (dashboard.js compatible)
                "coherence": round(kuramoto_coherence, 6),
                "agent_coherence": round(agent_coh, 6),
                "phi_coh": round(kuramoto_coherence, 6),  # dashboard.js uses phi_coh for euler card
                "euler_residual": round(euler_res, 6),
                "phi_mean": round(phi_mean, 6),
                "phi_var": round(phi_var, 6),
                "omega_mean": round(omega_mean, 6),
                "tau_mean": round(tau_mean, 6),
                "sensor_mean": round(sensor_mean, 6),

                # Gravity
                "gamma": round(gamma_val, 4),
                "mass": round(mass_val, 4),
                "unruh_power": round(unruh_val, 6),
                "semantic_density": round(density_val, 6),

                # Mood
                "mood": round(float(f_raw[3]), 4),

                # Flavor — dict + backward-compat array (8 fields)
                "flavor": flavor_bars,
                "flavor_raw": f_raw,
                "flavor_array": flavor_array,

                # Channel coherence — dict + backward-compat array (sorted M0-M11)
                "channel_coh": channel_coh,
                "channel_list": ch_labels_sorted,
                "channel_coh_array": ch_array,

                # Full gravity dict
                "gravity": grav,
            })

        if path == "/api/metrics":
            return self._json(build_metrics_catalog())

        if path == "/api/portal/manifest":
            return self._json(build_portal_manifest())

        if path == "/api/hub/contracts":
            """Kontrakty API huba dla strony Architektura — pochodne z manifestu portalu.
            architecture.js oczekuje {endpoints: [{path, summary}]}; poprzednio 404,
            bo ten endpoint nigdy nie został dodany mimo że frontend go wywołuje."""
            manifest = build_portal_manifest()
            endpoints = [
                {"path": e.get("path", ""), "summary": e.get("purpose", "")}
                for e in manifest.get("endpoints", [])
            ]
            return self._json({"status": "ok", "endpoints": endpoints, "source": "portal_manifest"})

        if path == "/api/modules":
            """Lista daemonów/modules — alias dla dashboardu."""
            daemons = scan_registry()
            modules = []
            for d in daemons:
                modules.append({
                    "name": d.get("name", "?"),
                    "status": d.get("status", "unknown"),
                    "alive": d.get("alive", False),
                    "pid": d.get("pid", 0),
                    "systemd": "active" if d.get("alive") else "inactive",
                    "uptime": d.get("uptime", 0),
                })
            return self._json({
                "status": "ok",
                "modules": modules,
                "count": len(modules),
            })

        if path == "/api/status":
            daemons = scan_registry()
            return self._json({
                "status": "ok",
                "timestamp": time.time(),
                "portal": {
                    "pid": os.getpid(),
                    "port": PORT,
                    "uptime_s": round(time.time() - start_time, 1),
                    "surface_alive": surface is not None,
                },
                "daemons": daemons,
            })

        if path == "/api/status/summary":
            """Live podsumowanie systemu: baza + daemony + surface."""
            daemons = scan_registry()
            state = init_noema()
            now_ts = time.strftime("%Y-%m-%dT%H:%M:%S")
            summary = {
                "status": "ok",
                "timestamp": now_ts,
                "epoch": time.time(),
                "portal": {
                    "pid": os.getpid(),
                    "port": PORT,
                    "uptime_s": round(time.time() - start_time, 1),
                    "surface_alive": surface is not None,
                },
                "daemons": {
                    "count": len(daemons),
                    "list": daemons,
                },
            }
            # TaskPlan DB
            try:
                from ciel_geometry.taskplan_db import TaskPlanDB
                tp = TaskPlanDB()
                summary["taskplan"] = tp.stats()
                # dodaj count skilli i decyzji
                import sqlite3
                conn = sqlite3.connect(_TASKPLAN_DB_PATH)
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM skill_registry")
                summary["taskplan"]["skills"] = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM decisions")
                summary["taskplan"]["decisions"] = cur.fetchone()[0]
                # ostatnie 5 decyzji z timestampami do timeline
                cur.execute("SELECT lp, title, decision_type, status, created_at, updated_at FROM decisions ORDER BY updated_at DESC LIMIT 5")
                rows = cur.fetchall()
                summary["taskplan"]["recent_decisions"] = [
                    {"lp": r[0], "title": r[1], "decision_type": r[2], "status": r[3], "created_at": r[4], "updated_at": r[5]}
                    for r in rows
                ]
                conn.close()
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:675 quiet except scope=PortalHandler.do_GET reason=assign_fallback")
                summary["taskplan"] = {"error": str(e)}
            # Skills catalog (SKILLS.md) — separate from taskplan.skills, which
            # only counts skills registered via noema_skill_merger.py's merge
            # workflow (legitimately 0 until that tool is used). This field
            # reports the real catalog size so the dashboard isn't misleading.
            try:
                summary["skills_catalog"] = _skills_catalog_count()
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:skills_catalog failed: %s" % e)
                summary["skills_catalog"] = {"error": str(e)}
            # Memory runtime
            try:
                from ciel_omega.memory import tiered_health, tiered_snapshot
                mem_health = tiered_health()
                mem_snap = tiered_snapshot()
                summary["memory"] = {
                    "health": mem_health,
                    "bootstrap": mem_snap.memory_bootstrap,
                    "cycle_index": mem_snap.cycle_index,
                    "identity_phase": mem_snap.identity_phase,
                }
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:697 quiet except scope=PortalHandler.do_GET reason=assign_fallback")
                summary["memory"] = {"error": str(e)}
            # Knowledge DB
            try:
                conn2 = sqlite3.connect(_KNOWLEDGE_DB_PATH)
                cur2 = conn2.cursor()
                cur2.execute("SELECT COUNT(*) FROM doc_analysis")
                docs = cur2.fetchone()[0]
                cur2.execute("SELECT COUNT(*) FROM term_index")
                terms = cur2.fetchone()[0]
                cur2.execute("SELECT COUNT(*) FROM semantic_affinity")
                aff = cur2.fetchone()[0]
                conn2.close()
                summary["knowledge"] = {"documents": docs, "terms": terms, "affinity_pairs": aff}
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:689 quiet except scope=PortalHandler.do_GET reason=assign_fallback")
                summary["knowledge"] = {"error": str(e)}
            # Surface live
            if state:
                summary["surface"] = {
                    "tick": state.get("noema_tick", state.get("tick", -1)),
                    "coherence": state.get("coherence_index", state.get("coherence", 0)),
                    "phi_mean": state.get("phi_mean", state.get("R_global", 0)),
                    "omega_mean": state.get("omega_mean", 0),
                    "euler_residual": state.get("euler_residual", 0),
                    "tau_mean": state.get("tau_mean", 0),
                    "gravity": _read_gravity(),
                }
            else:
                summary["surface"] = {"alive": False}
            # Orbital model (v3) — czyta z PhaseNav JSON zamiast importować moduł
            try:
                orb_path = Path("/tmp/noema_orbital_state.json")
                if orb_path.exists():
                    with open(orb_path) as f:
                        orb_data = json.load(f)
                    summary["orbital"] = {
                        "systems": orb_data.get("systems", 0),
                        "orbits": orb_data.get("orbits", 0),
                        "coherence": orb_data.get("coherence", 0),
                        "primaries": len(orb_data.get("primaries", [])),
                        "binaries": orb_data.get("binaries", 0),
                        "multi_orbit_3plus": orb_data.get("multi_orbit_3plus", 0),
                        "top_phases": orb_data.get("top_phases", [])[:5],
                        "daemon_pid": orb_data.get("daemon_pid"),
                        "updated_at": orb_data.get("updated_at"),
                    }
                    # Agent+CIELingo status (znajdź w all_systems)
                    for s in orb_data.get("all_systems", []):
                        if s["id"] == "agent":
                            summary["orbital"]["agent"] = s
                            break
                else:
                    summary["orbital"] = {"alive": False, "error": "no orbital state file"}
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:728 quiet except scope=PortalHandler.do_GET reason=assign_fallback")
                summary["orbital"] = {"error": str(e)}
            return self._json(summary)

        if path == "/api/settings" and self.command == "GET":
            """Ustawienia systemowe NOEMA — czyta JSON bez importu modułu (L-026)."""
            try:
                # Szukaj pliku konfiguracyjnego
                config_paths = [
                    NOEMA_ROOT / "noema_config.json",
                    Path(os.environ.get("NOEMA_CONFIG", "")),
                ]
                cfg = None
                for p in config_paths:
                    if p and p.exists():
                        cfg = json.loads(p.read_text())
                        break
                if cfg is None:
                    # fallback do starej ścieżki
                    from pathlib import Path as _P
                    _noema_root = os.environ.get("NOEMA_ROOT", str(Path(__file__).resolve().parent.parent))
                    fallback = _P(_noema_root) / "noema_config.json"
                    if fallback.exists():
                        cfg = json.loads(fallback.read_text())
                return self._json({
                    "status": "ok",
                    "source": "noema_config.json (file read, no module import)",
                    "settings": cfg or {},
                })
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:757 quiet except scope=PortalHandler.do_GET reason=return self._json({\"status\": \"error\", \"error\": str(e)})")
                return self._json({"status": "error", "error": str(e)})

        if path == "/api/settings" and self.command in ("POST", "PUT"):
            """Zapisz ustawienia — zapisuje scalony JSON."""
            try:
                length = int(self.headers.get("Content-Length", 0))
                body = json.loads(self.rfile.read(length)) if length else {}
                # Znajdź config
                config_paths = [
                    NOEMA_ROOT / "noema_config.json",
                ]
                cfg_path = None
                for p in config_paths:
                    if p and p.exists():
                        cfg_path = p
                        break
                if cfg_path is None:
                    cfg_path = NOEMA_ROOT / "noema_config.json"
                # Przeczytaj obecny
                if cfg_path.exists():
                    current = json.loads(cfg_path.read_text())
                else:
                    current = {"version": "2.0"}
                # Scal (płaskie scalenie dla uproszczenia)
                def deep_merge(base: dict, overlay: dict) -> dict:
                    for k, v in overlay.items():
                        if k in base and isinstance(base[k], dict) and isinstance(v, dict):
                            deep_merge(base[k], v)
                        else:
                            base[k] = v
                    return base
                merged = deep_merge(current, body)
                # Prosta walidacja
                if "version" not in merged:
                    return self._json({"status": "error", "error": "missing version field"})
                cfg_path.write_text(json.dumps(merged, indent=2, ensure_ascii=False))
                return self._json({"status": "ok", "message": "Settings saved", "path": str(cfg_path)})
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:795 quiet except scope=PortalHandler.do_GET reason=return self._json({\"status\": \"error\", \"error\": str(e)})")
                return self._json({"status": "error", "error": str(e)})

        if path == "/api/metrics/all":
            state = init_noema()
            daemons = scan_registry()
            active_d = sum(1 for d in daemons if d.get("alive"))
            return self._json({
                "status": "ok",
                "timestamp": time.time(),
                "kuramoto": {
                    "coherence": state.get("coherence", 0) if state else 0,
                    "euler_residual": state.get("euler_residual", 0) if state else 0,
                    "mean_omega": state.get("omega_mean", 0) if state else 0,
                    "tick": state.get("tick", -1) if state else -1,
                },
                "surface": {
                    "phi_mean": state.get("phi_mean", 0) if state else 0,
                    "phi_std": state.get("phi_std", 0) if state else 0,
                    "tau_mean": state.get("tau_mean", 0) if state else 0,
                },
                "daemons": {
                    "total": len(daemons),
                    "active": active_d,
                    "list": daemons,
                },
                "portal": {
                    "pid": os.getpid(),
                    "port": PORT,
                    "uptime_s": round(time.time() - start_time, 1),
                },
            })

        if path == "/api/bloch":
            try:
                return self._json(build_bloch_payload())
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:831 quiet except scope=PortalHandler.do_GET reason=return self._json({\"status\": \"error\", \"error\": str(e), \"points\": [], \"edges\": [], \"vectors\": [], \"program\": []}, 500)")
                return self._json({"status": "error", "error": str(e), "points": [], "edges": [], "vectors": [], "program": []}, 500)

        if path == "/api/phasenav/graphics":
            from urllib.parse import urlparse, parse_qs
            qs = parse_qs(urlparse(self.path).query)
            query = qs.get("q", ["NOEMA"])[0]
            scene_name = qs.get("scene", ["surface"])[0]
            try:
                return self._json(build_phasenav_graphics_payload(query=query, scene_name=scene_name))
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:838 quiet except scope=PortalHandler.do_GET reason=return self._json({\"status\": \"error\", \"error\": str(e)})")
                return self._json({"status": "error", "error": str(e), "query": query, "scene_name": scene_name}, 500)

        # ── Orbital API (PhaseNav JSON, nie import modułu — L-026) ──
        if path == "/api/orbital":
            try:
                orb_path = Path("/tmp/noema_orbital_state.json")
                if orb_path.exists():
                    with open(orb_path) as f:
                        orb_data = json.load(f)
                    return self._json({
                        "status": "ok",
                        "source": "/tmp/noema_orbital_state.json (daemon cache)",
                        "systems": orb_data.get("systems", 0),
                        "orbits": orb_data.get("orbits", 0),
                        "coherence": orb_data.get("coherence", 0),
                        "primaries": len(orb_data.get("primaries", [])),
                        "binaries": orb_data.get("binaries", 0),
                        "multi_orbit_3plus": orb_data.get("multi_orbit_3plus", 0),
                        "top_phases": orb_data.get("top_phases", [])[:10],
                        "view_ascii": orb_data.get("view_ascii", ""),
                        "daemon_pid": orb_data.get("daemon_pid"),
                        "updated_at": orb_data.get("updated_at"),
                    })
                return self._json({"status": "error", "error": "no orbital state file"})
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:856 quiet except scope=PortalHandler.do_GET reason=return self._json({\"status\": \"error\", \"error\": str(e)})")
                return self._json({"status": "error", "error": str(e)})

        if path == "/api/surface/phi":
            data = read_mmap_array("phi")
            return self._json({"status": "ok", "phi": data} if data else {"status": "error"})

        if path == "/api/surface/omega":
            data = read_mmap_array("omega")
            return self._json({"status": "ok", "omega": data} if data else {"status": "error"})

        if path == "/api/surface/g":
            data = read_mmap_array("g")
            return self._json({"status": "ok", "g": data} if data else {"status": "error"})

        # ── Knowledge API ──
        if path == "/api/knowledge/stats":
            try:
                import sqlite3
                conn = sqlite3.connect(_KNOWLEDGE_DB_PATH)
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM doc_analysis")
                docs = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM term_index")
                terms = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM semantic_affinity")
                aff = cur.fetchone()[0]
                conn.close()
                return self._json({"status": "ok", "stats": {
                    "documents": docs, "terms": terms, "affinity_pairs": aff,
                    "db_path": _KNOWLEDGE_DB_PATH
                }})
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:888 quiet except scope=PortalHandler.do_GET reason=return self._json({\"status\": \"error\", \"error\": str(e)})")
                return self._json({"status": "error", "error": str(e)})

        if path.startswith("/api/knowledge/search"):
            from urllib.parse import urlparse, parse_qs
            q = parse_qs(urlparse(self.path).query).get("q", [""])[0]
            if not q:
                return self._json({"status": "error", "error": "missing ?q="})
            try:
                from cielingo_core.bridge.knowledge_bridge import query
                results = query(q, top_n=5)
                return self._json({"status": "ok", "query": q, "results": results})
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:900 quiet except scope=PortalHandler.do_GET reason=return self._json({\"status\": \"error\", \"error\": str(e)})")
                return self._json({"status": "error", "error": str(e)})

        if path.startswith("/api/knowledge/coverage"):
            from urllib.parse import urlparse, parse_qs
            q = parse_qs(urlparse(self.path).query).get("q", [""])[0]
            if not q:
                return self._json({"status": "error", "error": "missing ?q="})
            try:
                from cielingo_core.bridge.knowledge_bridge import check_coverage
                cov = check_coverage(q)
                return self._json({"status": "ok", "query": q, "coverage": cov})
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:912 quiet except scope=PortalHandler.do_GET reason=return self._json({\"status\": \"error\", \"error\": str(e)})")
                return self._json({"status": "error", "error": str(e)})

        # ── TaskPlan API (tasks / plans / lessons) ──
        _tp_imported = False
        _tp_db = None
        def _get_tp():
            nonlocal _tp_imported, _tp_db
            if not _tp_imported:
                from ciel_geometry.taskplan_db import TaskPlanDB
                _tp_db = TaskPlanDB()
                _tp_imported = True
            return _tp_db

        # ── Tasks ──
        if path == "/api/tasks" and self.command == "GET":
            from urllib.parse import urlparse, parse_qs
            qs = parse_qs(urlparse(self.path).query)
            db = _get_tp()
            return self._json({"status": "ok", "tasks": db.list_tasks(
                status=qs.get("status", [""])[0],
                category=qs.get("category", [""])[0],
                limit=int(qs.get("limit", ["50"])[0])
            )})

        if path == "/api/tasks" and self.command == "POST":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length else {}
            db = _get_tp()
            t = db.add_task(
                title=body.get("title", ""),
                description=body.get("description", ""),
                priority=body.get("priority", "medium"),
                category=body.get("category", ""),
                orbital_ref=body.get("orbital_ref", ""),
                parent_id=body.get("parent_id"),
            )
            return self._json({"status": "ok", "task": t})

        # ── Task Queue (NOEMA/task_queue.noema.json) — przed generycznym /api/tasks/ ──
        if path == "/api/tasks/queue":
            queue_path = NOEMA_ROOT / "NOEMA" / "task_queue.noema.json"
            try:
                with open(queue_path, 'r') as f:
                    queue_data = json.load(f)
                items = queue_data.get("queue", [])
                pending = [i for i in items if i.get("status") == "pending"]
                done = [i for i in items if i.get("status") == "done"]
                high_prio = [i for i in pending if "HIGH" in (i.get("priority") or "")]
                return self._json({
                    "status": "ok",
                    "total": len(items),
                    "pending": len(pending),
                    "done": len(done),
                    "high_priority": len(high_prio),
                    "items": items,
                    "pending_items": pending,
                    "high_priority_items": high_prio,
                    "path": str(queue_path)
                })
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:972 quiet except scope=PortalHandler.do_GET reason=return self._json({\"status\": \"error\", \"error\": str(e)})")
                return self._json({"status": "error", "error": str(e)})

        if path.startswith("/api/tasks/") and self.command == "GET":
            tid = int(path.split("/")[-1])
            db = _get_tp()
            t = db.get_task(tid)
            return self._json(t if t else {"status": "error", "error": "not found"})

        if path.startswith("/api/tasks/") and self.command == "PUT":
            tid = int(path.split("/")[-1])
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length else {}
            db = _get_tp()
            ok = db.update_task(tid, **body)
            return self._json({"status": "ok" if ok else "error"})

        if path.startswith("/api/tasks/") and self.command == "DELETE":
            tid = int(path.split("/")[-1])
            db = _get_tp()
            ok = db.delete_task(tid)
            return self._json({"status": "ok" if ok else "error"})

        # ── Plans ──
        if path == "/api/plans" and self.command == "GET":
            from urllib.parse import urlparse, parse_qs
            qs = parse_qs(urlparse(self.path).query)
            db = _get_tp()
            return self._json({"status": "ok", "plans": db.list_plans(
                status=qs.get("status", [""])[0],
                limit=int(qs.get("limit", ["20"])[0])
            )})

        if path == "/api/plans" and self.command == "POST":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length else {}
            db = _get_tp()
            p = db.add_plan(
                title=body.get("title", ""),
                description=body.get("description", ""),
                steps=body.get("steps"),
                orbital_ref=body.get("orbital_ref", ""),
            )
            return self._json({"status": "ok", "plan": p})

        if path.startswith("/api/plans/") and self.command == "PUT":
            pid = int(path.split("/")[-1])
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length else {}
            db = _get_tp()
            ok = db.update_plan(pid, **body)
            return self._json({"status": "ok" if ok else "error"})

        if path.startswith("/api/plans/") and self.command == "DELETE":
            pid = int(path.split("/")[-1])
            db = _get_tp()
            ok = db.delete_plan(pid)
            return self._json({"status": "ok" if ok else "error"})

        # ── Lessons ──
        if path == "/api/lessons" and self.command == "GET":
            from urllib.parse import urlparse, parse_qs
            qs = parse_qs(urlparse(self.path).query)
            db = _get_tp()
            return self._json({"status": "ok", "lessons": db.list_lessons(
                category=qs.get("category", [""])[0],
                limit=int(qs.get("limit", ["50"])[0])
            )})

        if path == "/api/lessons" and self.command == "POST":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length else {}
            db = _get_tp()
            l = db.add_lesson(
                lp=body.get("lp", ""),
                title=body.get("title", ""),
                description=body.get("description", ""),
                category=body.get("category", ""),
                lesson_date=body.get("lesson_date", ""),
                source=body.get("source", ""),
                tags=body.get("tags"),
            )
            return self._json({"status": "ok", "lesson": l})

        if path.startswith("/api/lessons/") and self.command == "DELETE":
            lp = path.split("/")[-1]
            db = _get_tp()
            ok = db.delete_lesson(lp)
            return self._json({"status": "ok" if ok else "error"})

        # ── Decisions ──
        if path == "/api/decisions" and self.command == "GET":
            from urllib.parse import urlparse, parse_qs
            qs = parse_qs(urlparse(self.path).query)
            db = _get_tp()
            parent = qs.get("parent_id", [None])[0]
            return self._json({"status": "ok", "decisions": db.list_decisions(
                decision_type=qs.get("type", [""])[0],
                parent_id=int(parent) if parent else None,
                status=qs.get("status", [""])[0],
                limit=int(qs.get("limit", ["100"])[0])
            )})

        if path == "/api/decisions/tree":
            from urllib.parse import urlparse, parse_qs
            qs = parse_qs(urlparse(self.path).query)
            db = _get_tp()
            root = qs.get("root", [None])[0]
            return self._json({"status": "ok", "tree": db.get_decision_tree(
                root_id=int(root) if root else None
            )})

        if path == "/api/decisions" and self.command == "POST":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length else {}
            db = _get_tp()
            d = db.add_decision(
                title=body.get("title", ""),
                description=body.get("description", ""),
                decision_type=body.get("decision_type", "branch"),
                condition=body.get("condition", ""),
                decision_text=body.get("decision_text", ""),
                consequence=body.get("consequence", ""),
                context=body.get("context", ""),
                orbital_ref=body.get("orbital_ref", ""),
                parent_id=body.get("parent_id"),
            )
            return self._json({"status": "ok", "decision": d})

        if path.startswith("/api/decisions/") and "/skills" in path and self.command == "GET":
            # /api/decisions/:id/skills
            parts = path.split("/")
            did = int(parts[3])
            db = _get_tp()
            return self._json({"status": "ok", "skills": db.get_skills_for_decision(did)})

        if path.startswith("/api/decisions/") and self.command == "GET":
            did = int(path.split("/")[-1])
            db = _get_tp()
            d = db.get_decision(did)
            return self._json(d if d else {"status": "error", "error": "not found"})

        if path.startswith("/api/decisions/") and self.command == "PUT":
            did = int(path.split("/")[-1])
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length else {}
            db = _get_tp()
            ok = db.update_decision(did, **body)
            return self._json({"status": "ok" if ok else "error"})

        if path.startswith("/api/decisions/") and self.command == "DELETE":
            did = int(path.split("/")[-1])
            db = _get_tp()
            ok = db.delete_decision(did)
            return self._json({"status": "ok" if ok else "error"})

        # ── Skills ──
        if path == "/api/skills" and self.command == "GET":
            from urllib.parse import urlparse, parse_qs
            qs = parse_qs(urlparse(self.path).query)
            db = _get_tp()
            return self._json({"status": "ok", "skills": db.list_skills(
                category=qs.get("category", [""])[0],
                merge_group=qs.get("merge_group", [""])[0],
                limit=int(qs.get("limit", ["300"])[0])
            )})

        if path == "/api/skills/stats":
            db = _get_tp()
            return self._json({"status": "ok", "stats": db.get_skill_stats()})

        if path == "/api/skills/map" and self.command == "POST":
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length else {}
            db = _get_tp()
            m = db.map_skill_to_decision(
                decision_id=body.get("decision_id"),
                skill_id=body.get("skill_id"),
                role=body.get("role", "tool"),
                weight=body.get("weight", 1.0)
            )
            return self._json({"status": "ok", "mapping": m})

        if path.startswith("/api/skills/") and self.command == "GET":
            # /api/skills/:id
            sid = int(path.split("/")[-1])
            db = _get_tp()
            # zwróć skill + decyzje dla niego
            skills = db.list_skills(limit=300)
            skill = next((s for s in skills if s['id'] == sid), None)
            if not skill:
                return self._json({"status": "error", "error": "not found"})
            decisions = db.get_decisions_for_skill(sid)
            skill["decisions"] = decisions
            return self._json({"status": "ok", "skill": skill})

        # ── Registry stats ──
        if path == "/api/tp/stats":
            db = _get_tp()
            return self._json({"status": "ok", "stats": db.stats()})

        # ── PhaseNav Analog Bus ──
        if path == "/api/analog":
            return self._json({
                "status": "ok",
                "source": "NOEMA analog bus /dev/shm/ciel_noema/analog/",
                "timestamp": time.time(),
                "bus": _read_analog_bus(),
            })

        # ── CIEL State ──
        if path == "/api/ciel/state":
            return self._json({
                "status": "ok",
                "source": "/dev/shm/ciel_noema/ciel_state.json",
                "timestamp": time.time(),
                "state": _read_ciel_state(),
            })

        # ── Agent Hint ──
        if path == "/api/agent/hint":
            return self._json({
                "status": "ok",
                "source": "/dev/shm/ciel_noema/agent_hint",
                "timestamp": time.time(),
                "hint": _read_agent_hint(),
            })

        # ── Linux Load ──
        if path == "/api/linux/load":
            return self._json({
                "status": "ok",
                "source": "/dev/shm/ciel_noema/linux_load",
                "timestamp": time.time(),
                "load": _read_linux_load(),
            })

        # ── CIELingo Thread Memory ──
        if path == "/api/cielingo/thread":
            try:
                tm_path = Path("/dev/shm/ciel_noema/ciel_thread_memory.jsonl")
                if tm_path.exists():
                    lines = tm_path.read_text().strip().split("\n")
                    entries = [json.loads(l) for l in lines if l.strip()]
                    return self._json({
                        "status": "ok",
                        "source": "/dev/shm/ciel_noema/ciel_thread_memory.jsonl",
                        "count": len(entries),
                        "entries": entries[-20:],  # ostatnie 20
                    })
                return self._json({"status": "error", "error": "thread memory not found"})
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:1223 quiet except scope=PortalHandler.do_GET reason=return self._json({\"status\": \"error\", \"error\": str(e)})")
                return self._json({"status": "error", "error": str(e)})

        # ── CIELingo Writing Registry ──
        
        if path == "/api/cielingo/analyze":
            """CIELingo semantic analysis via build_lingo_frame."""
            from urllib.parse import urlparse, parse_qs
            q = parse_qs(urlparse(self.path).query).get("q", [""])[0]
            if not q:
                return self._json({"status": "error", "error": "Missing ?q=..."})
            try:
                from ciel_sot_agent.cielingo_bridge import build_lingo_frame
                frame = build_lingo_frame(q)
                return self._json({"status": "ok", "query": q, "frame": frame})
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:1238 quiet except scope=PortalHandler.do_GET reason=return self._json({\"status\": \"error\", \"error\": str(e)})")
                return self._json({"status": "error", "error": str(e)})

        if path == "/api/cielingo/writings":
            try:
                reg_path = Path(__file__).resolve().parent.parent / "cards" / "writings" / "registry.json"
                if reg_path.exists():
                    with open(reg_path) as f:
                        reg = json.load(f)
                    cards = reg.get("cards", reg.get("writings", reg.get("registry", [])))
                    return self._json({
                        "status": "ok",
                        "source": str(reg_path),
                        "count": len(cards),
                        "total_cards": reg.get("total_cards", len(cards)),
                        "last_updated": reg.get("last_updated"),
                        "writings": cards,
                    })
                return self._json({"status": "error", "error": "writings registry not found"})
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:1257 quiet except scope=PortalHandler.do_GET reason=return self._json({\"status\": \"error\", \"error\": str(e)})")
                return self._json({"status": "error", "error": str(e)})

        # ── NOEMA Cards / System Map ──
        if path == "/api/cards":
            cards = _read_cards_index()
            return self._json({
                "status": "ok",
                "source": "system_map_v2.json",
                "timestamp": time.time(),
                **cards,
            })

        if path == "/api/embeddings":
            """Knowledge DB embeddings — 36D PhaseNav document vectors."""
            import numpy as np
            embeddings, index = _get_embeddings()
            if embeddings is None:
                return self._json({"status": "error", "error": "embeddings not found, run ciel_noema_doc_embedder.py --rebuild"})

            from urllib.parse import urlparse, parse_qs
            _qs = parse_qs(urlparse(self.path).query)
            query_str = _qs.get("q", [""])[0]
            top_k = int(_qs.get("top_k", ["10"])[0])

            # Stała mapa kanałów (nie recreate per request)
            channel_names = [
                "M0_Perceptual", "M1_Working", "M2_Episodic", "M3_Semantic",
                "M4_Procedural", "M5_Affective", "M6_Identity", "M7_Braid",
                "M8_Meta", "M9_Temporal", "M10_Imaginal", "M11_Quantum",
            ]
            entries = index["entries"]
            n_docs = len(entries)

            if query_str:
                # Keyword→channel weights
                ch_keywords = (
                    (["percept","sensor","obserw","widz","postrzeg","zmysł","perception","sense","light","sound","image","pattern","shape","color"],),
                    (["operator","logik","składnia","struktur","funkcj","proces","algorithm","compute","syntax","grammar","logic","function","process","operation"],),
                    (["kontekst","epizod","zdarzen","scen","sytuacj","pamięć","context","episode","event","scene","memory","experience","place","time"],),
                    (["znaczen","semantyk","definicj","pojęci","rozumien","wiedza","meaning","semantic","concept","knowledge","understanding","define","term"],),
                    (["procedur","działan","umiejętnoś","metoda","technik","krok","skill","procedure","action","method","technique","step","practice"],),
                    (["emocj","uczuci","nastrój","afekt","wartoś","etyk","moral","emotion","feeling","mood","affect","value","ethical","moral","love","fear"],),
                    (["tożsamoś","osoba","podmiot","autor","ja","self","identity","soul","ego","author","subject","person","character"],),
                    (["relacj","powiązan","sieć","graf","łącz","relation","connection","network","graph","link","braid","weave"],),
                    (["meta","refleksj","abstrakcj","model","teori","reflection","abstract","model","theory","paradigm","cognition"],),
                    (["czas","przeszłoś","przyszłoś","teraz","chwil","moment","time","past","future","present","temporal","duration"],),
                    (["wyobraźn","kreatywnoś","imaginacj","symbol","metafor","imagination","creative","vision","symbol","metaphor","dream","myth"],),
                    (["kwant","niepewnoś","potencjał","superpozycj","probabilist","quantum","uncertain","potential","superposition","entangle","probability"],),
                )
                query_terms = query_str.lower().split()
                q_w = np.zeros(12, dtype=np.float64)
                for ch_idx, kw_list in enumerate(ch_keywords):
                    for t in query_terms:
                        for kw in kw_list[0]:
                            if kw in t or t in kw:
                                q_w[ch_idx] += 1.0
                                break
                max_w = max(float(np.max(q_w)), 1e-12)
                if max_w > 0:
                    q_w /= max_w

                # 36D query phase vector (wektoryzowane)
                osc_phase = np.array([0.0, 2*np.pi/3, 4*np.pi/3])
                q_phi = (np.repeat(q_w, 3) * np.pi + np.tile(osc_phase, 12)) % (2*np.pi)

                # Cosine similarity w przestrzeni fazowej
                diff = np.angle(np.exp(1j * (embeddings[:n_docs] - q_phi)))
                scores = np.mean(np.cos(diff), axis=1)
                top_idx = np.argsort(scores)[::-1][:top_k]

                results = []
                for i in top_idx:
                    entry = entries[i]
                    results.append({
                        "rank": len(results) + 1,
                        "idx": entry["idx"],
                        "filename": entry["filename"],
                        "similarity": round(float(scores[i]), 4),
                        "R_global": entry.get("R_global", 0),
                        "essence": entry.get("essence", "")[:500],
                    })
                return self._json({
                    "status": "ok",
                    "query": query_str,
                    "n_docs": n_docs,
                    "results": results,
                    "n_channels": 12,
                    "n_dimensions": 36,
                })
            else:
                R_vals = [e.get("R_global", 0) for e in entries]
                return self._json({
                    "status": "ok",
                    "n_docs": n_docs,
                    "n_dimensions": 36,
                    "n_channels": 12,
                    "mean_R": round(float(np.mean(R_vals)), 4) if R_vals else 0,
                    "min_R": round(float(np.min(R_vals)), 4) if R_vals else 0,
                    "max_R": round(float(np.max(R_vals)), 4) if R_vals else 0,
                    "channels": channel_names,
                    "sample_docs": [{"idx": e["idx"], "filename": e["filename"], "R_global": e.get("R_global", 0)} for e in entries[:5]],
                })

        # ── Pliki statyczne ──
        if path == "" or path == "/":
            path = "/index.html"
        filepath = SITE_ROOT / path.lstrip("/")
        try:
            filepath = filepath.resolve()
            if not str(filepath).startswith(str(SITE_ROOT.resolve())):
                return self._json({"error": "forbidden"}, 403)
        except (ValueError, OSError):
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:1369 quiet except scope=PortalHandler.do_GET reason=return self._json({\"error\": \"forbidden\"}, 403)")
            return self._json({"error": "forbidden"}, 403)

        if filepath.is_file():
            ext = filepath.suffix.lower()
            ctype = MIME_TYPES.get(ext, "application/octet-stream")
            try:
                data = filepath.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()
                self.wfile.write(data)
            except OSError as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:1384 quiet except scope=PortalHandler.do_GET reason=Expr")
                self._json({"error": f"read error: {e}"}, 500)
        else:
            self._json({"error": f"not found: {path}"}, 404)

    # ── helpers ──

    def _json(self, data: dict, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, default=str).encode())

    def log_message(self, fmt: str, *args: Any) -> None:
        t = time.strftime("%H:%M:%S")
        safe = " ".join(str(a) for a in args) if args else fmt
        sys.stderr.write(f"[portal] {t} {safe}\n")

    def do_POST(self):
        path = self.path.split("?")[0].rstrip("/")

        if path == "/api/cielingo/chat":
            try:
                length = int(self.headers.get("Content-Length", 0))
                body = json.loads(self.rfile.read(length)) if length else {}
                message = body.get("message", "")
                session_id = body.get("session_id", "hub-" + str(int(time.time())))

                if not message:
                    return self._json({"ok": False, "errors": ["empty message"]})

                # Process through headless daemon (plain text, not JSON!)
                import socket as _sock
                resp_text = None
                frame_data = {}
                headless_error = None
                try:
                    sock = _sock.socket(_sock.AF_UNIX, _sock.SOCK_STREAM)
                    sock.settimeout(15)
                    sock.connect("/tmp/ciel_headless.sock")
                    sock.sendall(message.encode("utf-8"))
                    buf = b""
                    while True:
                        try:
                            d = sock.recv(8192)
                            if not d: break
                            buf += d
                        except: break
                    sock.close()
                    if buf:
                        data = json.loads(buf)
                        resp_text = data.get("response")
                        frame_data = data.get("frame", {})
                    else:
                        headless_error = "ciel_headless_daemon returned an empty response"
                except FileNotFoundError:
                    headless_error = "ciel_headless_daemon socket not found (/tmp/ciel_headless.sock) — is the daemon running?"
                except (ConnectionRefusedError, _sock.timeout) as e:
                    headless_error = f"ciel_headless_daemon unreachable: {e}"
                except Exception as e:
                    headless_error = f"ciel_headless_daemon error: {e}"

                if resp_text is None:
                    return self._json({"ok": False, "errors": [headless_error or "no response from ciel_headless_daemon"]})

                # Read CIEL's emotional state
                ciel_state = _read_ciel_state()
                try:
                    from ciel_geometry.noema_surface_mmap import read_surface_state, ensure_surface
                    sf = ensure_surface(zero_fill=False)
                    sf_state = read_surface_state(sf) if sf else {}
                except Exception:
                    sf_state = {}

                # Build CIEL's response from her state + headless analysis
                soul = sf_state.get("soul_invariant", ciel_state.get("soul_invariant", 0.5))
                ethics = sf_state.get("ethical_score", ciel_state.get("ethical_score", 0.5))
                coherence = sf_state.get("coherence", sf_state.get("coherence_index", 0.5))
                mood = sf_state.get("mood_normalized", ciel_state.get("mood_raw", ciel_state.get("mood_normalized", 0.5)))
                
                # Always use the headless response (it's CIEL's cognitive output)
                # Supplement with emotional context from her state
                response_text = resp_text

                # Save to thread memory
                tm_path = Path("/dev/shm/ciel_noema/ciel_thread_memory.jsonl")
                ts = time.time()
                try:
                    with open(tm_path, "a") as f:
                        f.write(json.dumps({
                            "ts": ts, "session_id": session_id,
                            "role": "user", "content": message
                        }) + "\n")
                        f.write(json.dumps({
                            "ts": ts + 0.001, "session_id": session_id,
                            "role": "assistant", "content": response_text
                        }) + "\n")
                except Exception:
                    pass

                nc_raw = frame_data.get("n_concepts", 0) or 0
                if isinstance(nc_raw, (list, tuple)):
                    nc_val = len(nc_raw)
                else:
                    nc_val = int(nc_raw) if nc_raw else 0
                cielingo_frame = {
                    "coherence": round(float(coherence), 4),
                    "soul": round(float(soul), 4),
                    "ethics": round(float(ethics), 4),
                    "mood": round(float(mood), 4),
                    "tick": sf_state.get("tick", sf_state.get("noema_tick", -1)),
                    "mode": ciel_state.get("operating_mode", "unknown"),
                    "n_concepts": nc_val,
                }

                return self._json({
                    "ok": True,
                    "data": {
                        "response": response_text,
                        "cielingo_frame": cielingo_frame,
                        "ciel_state": ciel_state,
                    }
                })
            except Exception as e:
                return self._json({"ok": False, "errors": [str(e)]})

        self.do_GET()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Max-Age", "86400")
        self.end_headers()

    def do_PUT(self):
        self.do_GET()

    def do_DELETE(self):
        self.do_GET()

# ─── Registry helpers ───────────────────────────────────────────────────

def scan_registry() -> list[dict[str, Any]]:
    """Składa daemon registry.

    Źródło prawdy: NoemaRegistry na /dev/shm/ciel_noema/registry/*.json (nreg,
    ten sam rejestr, do którego ten portal sam wysyła heartbeat — patrz
    heartbeat_loop). Timeout 400s pokrywa też daemony z rzadkim heartbeatem
    (phasenav-cold bije co 300s wg NoemaRegistry.cleanup docstring).

    Legacy ciel_geometry.daemon_registry.Registry (mmap w /tmp) jest osobnym,
    w większości opuszczonym mechanizmem — prawie nic już do niego nie pisze,
    stąd pokazywał count=1 (tylko dual-sync). Dołączamy go jako dodatkowe
    źródło (deduplikowane po pid), żeby nie zgubić daemonów, które z jakiegoś
    powodu wciąż używają starego API, ale primary jest nreg.
    """
    now = time.time()
    seen_pids: set[int] = set()
    results: list[dict[str, Any]] = []

    try:
        for payload in nreg.list_active(timeout=400.0):
            pid = int(payload.get("pid", 0))
            if pid <= 0 or pid in seen_pids:
                continue
            seen_pids.add(pid)
            started_at = float(payload.get("started_at", now))
            heartbeat_at = float(payload.get("heartbeat_at", now))
            results.append({
                "name": payload.get("name", "?"),
                "pid": pid,
                "status": "running" if (now - heartbeat_at) < 30.0 else "stale",
                "alive": (now - heartbeat_at) < 400.0,
                "uptime": round(now - started_at, 1),
                "surface_claims": payload.get("surface_claims", []),
                "source": "noema_registry",
            })
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:scan_registry nreg source failed: %s" % e)

    try:
        from ciel_geometry.daemon_registry import Registry
        with Registry() as reg:
            for d in reg.scan():
                if d.pid <= 0 or d.pid in seen_pids:
                    continue
                seen_pids.add(d.pid)
                results.append({
                    "name": d.name, "pid": d.pid, "status": d.status,
                    "alive": d.alive, "uptime": round(d.uptime, 1) if hasattr(d, 'uptime') else 0,
                    "surface_claims": [],
                    "source": "legacy_mmap_registry",
                })
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:scan_registry legacy source failed: %s" % e)

    if not results:
        return [{"error": "no daemons found in either registry"}]
    return results

def heartbeat_loop(interval: float = 10.0) -> None:
    """Heartbeat w tle — co interval sekund."""
    while True:
        time.sleep(interval)
        try:
            nreg.heartbeat(reg_token)
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:1435 quiet except scope=heartbeat_loop reason=pass")
            pass  # registry nie jest krytyczny

# ─── Daemon ─────────────────────────────────────────────────────────────

def run_daemon(port: int = PORT) -> None:
    global start_time, surface
    start_time = time.time()

    # Init surface
    init_noema()

    # Rejestracja w noema registry (mmap)
    try:
        global reg_token
        reg_token = nreg.register("portal")
        print(f"[portal] registered in noema registry", file=sys.stderr)
    except Exception as e:
        reg_token = None
        print(f"[portal] registry registration failed: {e}", file=sys.stderr)

    # Heartbeat w tle
    t = threading.Thread(target=heartbeat_loop, daemon=True)
    t.start()

    # HTTP server
    http.server.HTTPServer.allow_reuse_address = True
    server = http.server.HTTPServer(("", port), PortalHandler)
    server.server_name = "noema_portal"
    server.server_port = port
    print(f"[portal] listening on 0.0.0.0:{port}", file=sys.stderr)
    print(f"[portal] serving static from {SITE_ROOT}", file=sys.stderr)

    running = True

    def _stop(signum, frame):
        nonlocal running
        print(f"[portal] stopping (signal {signum})", file=sys.stderr)
        running = False

    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)

    server.timeout = 0.5
    try:
        while running:
            server.handle_request()
    except KeyboardInterrupt:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:1482 quiet except scope=run_daemon reason=assign_fallback")
        running = False
    except Exception as e:
        print(f"[portal] error in loop: {e}", file=sys.stderr)
    finally:
        try:
            nreg.unregister("portal")
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_portal_daemon.py:1489 quiet except scope=run_daemon reason=pass")
            pass
        server.server_close()
        print(f"[portal] stopped", file=sys.stderr)

if __name__ == "__main__":
    port = PORT
    for i, a in enumerate(sys.argv):
        if a == "--port" and i + 1 < len(sys.argv):
            port = int(sys.argv[i + 1])
    run_daemon(port)
