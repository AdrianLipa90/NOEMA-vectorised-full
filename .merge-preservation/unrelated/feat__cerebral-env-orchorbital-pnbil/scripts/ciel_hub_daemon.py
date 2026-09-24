#!/usr/bin/env python3
"""CIEL Server Hub Daemon — Phase 1.

ThreadingHTTPServer + kontrakt API + snapshot cache.
Zastępuje noema_portal_daemon.py jako główny serwer huba.

Usage:
  ciel_hub_daemon.py [--port PORT] [--host HOST]
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

# CIEL ORBITAL BINDING — daemon bound
import os as _ciel_os, os.path as _ciel_path
if not (_ciel_path.exists("/dev/shm/ciel_noema/ciel_binding_status") and open("/dev/shm/ciel_noema/ciel_binding_status").read().strip() == "ACTIVE"):
    import warnings as _ciel_w
    _ciel_w.warn("CIEL ORBITAL BINDING: not ACTIVE on daemon " + __name__)


import json
import os
import sqlite3
import sys
import time
from pathlib import Path

# ─── Ścieżki ────────────────────────────────────────────────────────────
NOEMA_ROOT = Path(__file__).resolve().parent.parent
CIEL_PROJECT_ROOT = NOEMA_ROOT.parent
SITE_ROOT = NOEMA_ROOT / "site"
PORT = int(os.environ.get("CIEL_HUB_PORT", "18888"))
HOST = os.environ.get("CIEL_HUB_HOST", "0.0.0.0")

# ─── Dodaj src do path ──────────────────────────────────────────────────
sys.path.insert(0, str(NOEMA_ROOT / "src"))

from ciel_geometry.orbital_state_contract import summarize_verified_orbital_state
from ciel_geometry.paths import P as _P

_ORBITAL_STATE_PATH = Path(str(_P.STATE.ORCH_PKL)).parent / "noema_orbital_state.json"

# ─── Stan globalny ──────────────────────────────────────────────────────
surface: dict | None = None
reg_token = None

# ─── Helpery powierzchni ──────────────────────────────────────────────────

def init_surface() -> dict:
    """Inicjalizuje połączenie z NOEMA surface."""
    global surface
    try:
        from ciel_geometry.noema_surface_mmap import ensure_surface, read_surface_state
        surface = ensure_surface(zero_fill=False)
        state = read_surface_state(surface)
        print(f"[hub] surface OK: tick={state.get('tick')} coh={state.get('coherence',0):.3f}")
        return state
    except Exception as e:
        print(f"[hub] surface init failed: {e}", file=sys.stderr)
        surface = None
        return {}

def read_mmap_array(name: str) -> list | None:
    """Czyta tablicę numpy z surface mmap po nazwie pola."""
    try:
        if surface is None:
            init_surface()
        if surface and name in surface:
            arr = surface[name]
            if hasattr(arr, "tolist"):
                return arr.tolist()
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:63 quiet except scope=read_mmap_array reason=pass")
        raise
        pass
    return None

def _read_gravity() -> dict:
    """Czyta gravity z surface."""
    try:
        import numpy as np
        if surface is None:
            init_surface()
        if not surface:
            return {"tau_dilation": 0, "mass_total": 0, "unruh_power": 0, "semantic_density": 0}
        
        def _get(name: str, n: int = 1) -> np.ndarray:
            try:
                arr = np.asarray(surface.get(name, [0]*n), dtype=np.float64).ravel()
                return arr if arr.size >= n else np.zeros(n)
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:80 quiet except scope=_read_gravity._get reason=return np.zeros(n)")
                raise
                return np.zeros(n)
        
        grav = _get("gravity", 4)
        return {
            "tau_dilation": float(grav[0]) if len(grav) > 0 else 0,
            "mass_total": float(grav[1]) if len(grav) > 1 else 0,
            "unruh_power": float(grav[2]) if len(grav) > 2 else 0,
            "semantic_density": float(grav[3]) if len(grav) > 3 else 0,
        }
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:90 quiet except scope=_read_gravity reason=return {\"tau_dilation\": 0, \"mass_total\": 0, \"unruh_power\": 0, \"semantic_density\": 0}")
        raise
        return {"tau_dilation": 0, "mass_total": 0, "unruh_power": 0, "semantic_density": 0}

def _read_analog_bus() -> dict:
    """Czyta PhaseNav analog bus."""
    try:
        import numpy as np
        analog_root = Path("/dev/shm/ciel_noema/analog")
        bus: dict = {}
        for name, size in [("phi_hot", 36), ("phi_cold", 36), ("writing_phi", 36)]:
            p = analog_root / name
            if p.exists() and p.stat().st_size >= size * 8:
                arr = np.memmap(p, dtype=np.float64, mode="r", shape=(size,))
                bus[name] = arr.tolist()
        for name in ["temp", "resonance"]:
            p = analog_root / name
            if p.exists() and p.stat().st_size >= 8:
                arr = np.memmap(p, dtype=np.float64, mode="r", shape=(1,))
                bus[name] = float(arr[0])
        return bus
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:110 quiet except scope=_read_analog_bus reason=return {}")
        raise
        return {}

def _read_ciel_state() -> dict:
    """Czyta CIEL state z /dev/shm/ciel_noema/ciel_state.json."""
    try:
        p = Path("/dev/shm/ciel_noema/ciel_state.json")
        if p.exists():
            return json.loads(p.read_text())
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:119 quiet except scope=_read_ciel_state reason=pass")
        raise
        pass
    return {}

def _read_agent_hint() -> str:
    """Czyta agent_hint."""
    try:
        p = Path("/dev/shm/ciel_noema/agent_hint")
        if p.exists():
            return p.read_text().strip()
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:129 quiet except scope=_read_agent_hint reason=pass")
        raise
        pass
    return ""

def _read_linux_load() -> dict:
    """Czyta linux_load mmap."""
    try:
        import numpy as np
        p = Path("/dev/shm/ciel_noema/linux_load")
        if p.exists():
            arr = np.memmap(p, dtype=np.float64, mode="r")
            return {
                "cpu_pct": float(arr[0]) if len(arr) > 0 else 0,
                "mem_pct": float(arr[1]) if len(arr) > 1 else 0,
                "io_pct": float(arr[2]) if len(arr) > 2 else 0,
            }
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:145 quiet except scope=_read_linux_load reason=pass")
        raise
        pass
    return {"cpu_pct": 0, "mem_pct": 0, "io_pct": 0}

def scan_registry() -> list[dict]:
    """Składa daemon registry."""
    try:
        from ciel_geometry.daemon_registry import Registry
        with Registry() as reg:
            info = reg.scan()
            return [
                {"name": d.name, "pid": d.pid, "status": d.status,
                 "alive": d.alive, "uptime": round(d.uptime, 1) if hasattr(d, 'uptime') else 0}
                for d in info if d.pid > 0
            ]
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:160 quiet except scope=scan_registry reason=return [{\"error\": str(e)}]")
        raise
        return [{"error": str(e)}]

def _read_cards_index() -> dict:
    """Czyta system_map_v2.json jako indeks kart."""
    try:
        map_path = NOEMA_ROOT / "system_map_v2.json"
        if map_path.exists():
            data = json.loads(map_path.read_text())
            return {
                "total_cards": data.get("total_cards", 0),
                "total_daemons": data.get("total_daemons", 0),
                "total_systems": data.get("total_systems", 0),
                "total_connections": data.get("total_connections", 0),
                "systems": [
                    {"id": s.get("id"), "name": s.get("name"), "type": s.get("type"),
                     "status": s.get("status"), "ordinal": s.get("ordinal")}
                    for s in data.get("systems", [])
                ],
            }
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:180 quiet except scope=_read_cards_index reason=return {\"error\": str(e)}")
        raise
        return {"error": str(e)}
    return {}

# ─── Import rejestru endpointów i serwera ────────────────────────────────
from ciel_hub.contracts import register, registry, ok, fail
from ciel_hub.portal_contracts import build_system_catalog, normalize_metric
from ciel_hub.snapshot import cache as snapshot_cache
from ciel_hub.server import run_server
from ciel_geometry.phasenav.graphics import build_phasenav_graphics_bundle as _build_phasenav_graphics_bundle
from ciel_geometry.paths import P as _P

# Was hardcoded /tmp/{noema_knowledge,noema_taskplan}.db (tmpfs, wiped on
# reboot) — fixed 2026-07-08.
_KNOWLEDGE_DB_PATH = str(_P.DB.KNOWLEDGE)
_TASKPLAN_DB_PATH = str(_P.DB.TASKPLAN)

# ─── Rejestracja endpointów ──────────────────────────────────────────────

# --- Core ---
@register("GET", "/api/hub/health")
def hub_health(ctx: dict) -> tuple[dict, int]:
    return ok({
        "status": "ok",
        "pid": os.getpid(),
        "uptime_s": round(time.time() - ctx.get("server_start", time.time()), 1),
        "surface_alive": surface is not None,
        "snapshot_cache": snapshot_cache.status(),
        "endpoints": len(registry._routes),
    })

@register("GET", "/api/hub/snapshot")
def hub_snapshot(ctx: dict) -> tuple[dict, int]:
    return ok(snapshot_cache.get_all())

@register("GET", "/api/hub/contracts")
def hub_contracts(ctx: dict) -> tuple[dict, int]:
    return ok({
        "version": "1.0",
        "endpoints": registry.list_endpoints(),
        "envelope": {
            "ok": "bool",
            "data": "any",
            "meta": {"ts": "float", "source": "str", "duration_ms": "float"},
            "errors": ["str"],
        },
    })


@register("GET", "/api/operations")
def api_operations(ctx: dict) -> tuple[dict, int]:
    """Expose the Cockpit operation contract without executing any action.

    Execution stays disabled until a server-side capability token, a separate
    confirmation step, allowlist enforcement, read-back, and receipts are all
    wired to an approved actuator.
    """
    operations = [
        {"operation_id": "service.restart", "category": "systemd", "label": "Restart usługi", "risk": "high", "rollback": "service restart", "status": "not_configured"},
        {"operation_id": "daemon.restart", "category": "daemon", "label": "Restart daemona", "risk": "high", "rollback": "service restart", "status": "not_configured"},
        {"operation_id": "queue.retry", "category": "queue", "label": "Ponów zadanie kolejki", "risk": "medium", "rollback": "idempotency key", "status": "not_configured"},
        {"operation_id": "phasenav.preview", "category": "phasenav", "label": "Podgląd PhaseNav", "risk": "low", "rollback": "not required", "status": "preview_only"},
    ]
    return ok({
        "contract": "noema.operations/v1",
        "execution_enabled": False,
        "capability_token_location": "server-side only",
        "required_cycle": ["plan", "preview", "capability confirmation", "execute", "read-back", "immutable receipt"],
        "operations": operations,
        "receipts": [],
    })


def build_portal_manifest() -> dict[str, Any]:
    """Holistic map of the live CIEL hub and portal architecture."""
    endpoints = registry.list_endpoints()
    unique_endpoints = []
    seen_paths = set()
    for ep in endpoints:
        path = ep.get("path", "")
        if path in seen_paths:
            continue
        seen_paths.add(path)
        unique_endpoints.append(ep)
    endpoint_paths = [ep.get("path", "") for ep in unique_endpoints]
    return {
        "status": "ok",
        "version": "hub-manifest/v2",
        "hub": {
            "name": "CIEL Server Hub",
            "port": PORT,
            "host": HOST,
            "root": str(SITE_ROOT),
            "description": "Live portal + surface + CIEL + PhaseNav + knowledge + tasks",
        },
        "layers": [
            {
                "name": "Kernel Surface",
                "role": "Shared memory, surface mmap, analog bus, gravity, state_db snapshots",
                "sources": ["/dev/shm/ciel_noema/*", "/api/live", "/api/status/summary", "/api/noema/surface", "/api/noema/phase", "/api/analog"],
            },
            {
                "name": "Runtime APIs",
                "role": "Hub routes exposing live state and control surfaces",
                "sources": ["/api/hub/health", "/api/hub/snapshot", "/api/hub/contracts", "/api/live", "/api/metrics", "/api/metrics/all", "/api/systems/catalog", "/api/status", "/api/status/summary"],
            },
            {
                "name": "CIEL / Cognition",
                "role": "Identity, mode, ethics, chat, semantic analysis, thread memory",
                "sources": ["/api/ciel/state", "/api/ciel/identity", "/api/ciel/mode", "/api/cielingo/chat", "/api/cielingo/analyze", "/api/cielingo/thread", "/api/cielingo/writings"],
            },
            {
                "name": "PhaseNav / Geometry",
                "role": "PhaseNav state, Bloch projection, graphics bundle, operator algebra",
                "sources": ["/api/phasenav/state", "/api/phasenav/graphics", "/api/bloch"],
            },
            {
                "name": "Knowledge / Planning",
                "role": "Knowledge DB, taskplan DB, lessons, decisions, skills",
                "sources": ["/api/knowledge/stats", "/api/knowledge/search", "/api/tasks", "/api/tasks/queue", "/api/plans", "/api/lessons", "/api/decisions", "/api/decisions/tree", "/api/skills", "/api/skills/stats"],
            },
            {
                "name": "Portal UI",
                "role": "SPA pages rendered from site/",
                "sources": ["/", "/#dashboard", "/#research", "/#live", "/#metrics", "/#status", "/#systems", "/#memory", "/#projects", "/#bloch", "/#phasenav", "/#graph", "/#science", "/#engineering", "/#simulations", "/#architecture", "/#knowledge", "/#decision-tree", "/#cielingo-chat", "/#monograph", "/#preferences"],
            },
        ],
        "endpoints": [
            {"path": path, "purpose": ep.get("summary") or ep.get("description") or ep.get("name") or "route"}
            for path, ep in zip(endpoint_paths, unique_endpoints)
        ],
        "pages": [
            {"route": "dashboard", "title": "Dashboard", "purpose": "Live surface overview", "sources": ["/api/live", "/api/metrics", "/api/modules", "/api/status/summary"]},
            {"route": "research", "title": "Research / Public", "purpose": "Public research navigation without runtime operations", "sources": ["/api/metrics", "/api/portal/manifest"]},
            {"route": "live", "title": "Live", "purpose": "Real-time surface dashboard", "sources": ["/api/live", "/api/modules", "/api/status/summary"]},
            {"route": "metrics", "title": "Metryki", "purpose": "Searchable metrics registry", "sources": ["/api/metrics", "/api/metrics/all", "/api/live"]},
            {"route": "status", "title": "Status", "purpose": "System state summary", "sources": ["/api/status", "/api/status/summary", "/api/hub/health", "/api/hub/snapshot"]},
            {"route": "systems", "title": "Systemy i moduły", "purpose": "Logical system catalog and distinct runtime instances", "sources": ["/api/systems/catalog", "/api/noema/daemons", "/api/noema/modules", "/api/modules", "/api/status/summary"]},
            {"route": "projects", "title": "Projekty NOEMY", "purpose": "Tasks, plans and decisions overview", "sources": ["/api/tasks", "/api/tasks/queue", "/api/plans", "/api/decisions", "/api/lessons"]},
            {"route": "bloch", "title": "Sfera Blocha", "purpose": "Bloch sphere and vector program", "sources": ["/api/bloch", "/api/noema/phase", "/api/live"]},
            {"route": "phasenav", "title": "PhaseNav", "purpose": "Operator algebra, Bloch scenes and graphics", "sources": ["/api/live", "/api/phasenav/state", "/api/phasenav/graphics", "/api/bloch"]},
            {"route": "graph", "title": "Graf wiedzy", "purpose": "Knowledge graph viewer", "sources": ["/api/knowledge/stats", "/api/status/summary"]},
            {"route": "science", "title": "Nauka", "purpose": "Research and knowledge surface", "sources": ["/api/knowledge/stats", "/api/portal/manifest", "/api/status/summary"]},
            {"route": "engineering", "title": "Inżynieria", "purpose": "Runtime, build and ops surface", "sources": ["/api/modules", "/api/tasks/queue", "/api/skills/stats", "/api/status/summary"]},
            {"route": "simulations", "title": "Symulacje", "purpose": "PhaseNav scene replay", "sources": ["/api/phasenav/graphics", "/api/phasenav/state", "/api/live"]},
            {"route": "architecture", "title": "Architecture", "purpose": "Full portal architecture map", "sources": ["/api/portal/manifest", "/api/architecture", "/api/modules", "/api/hub/contracts", "/api/status/summary"], "notes": "This page is the canonical architecture view."},
            {"route": "cielingo-chat", "title": "CIELingo Chat", "purpose": "Conversation, analysis and thread memory", "sources": ["/api/cielingo/chat", "/api/cielingo/analyze", "/api/cielingo/thread"]},
            {"route": "memory", "title": "Pamięć CIEL", "purpose": "Channel memory and thread state", "sources": ["/api/cielingo/thread", "/api/memory/stats", "/api/noema/phase"]},
            {"route": "decision-tree", "title": "Drzewo decyzyjne", "purpose": "Decision tree from TaskPlan DB", "sources": ["/api/decisions/tree", "/api/decisions", "/api/tasks", "/api/plans"]},
            {"route": "knowledge", "title": "Baza wiedzy", "purpose": "Knowledge DB search and coverage", "sources": ["/api/knowledge/stats", "/api/knowledge/search"]},
            {"route": "monograph", "title": "Monografia", "purpose": "Document catalog and knowledge overview", "sources": ["/api/knowledge/stats", "/api/knowledge/search"]},
            {"route": "preferences", "title": "Preferencje NOEMY", "purpose": "System settings and CIEL state", "sources": ["/api/ciel/state", "/api/ciel/identity", "/api/ciel/mode", "/api/noema/surface"]},
        ],
        "pipelines": [
            {"from": "/dev/shm/ciel_noema/", "to": "/api/live", "label": "surface → live API"},
            {"from": "/api/cielingo/chat", "to": "/dev/shm/ciel_noema/ciel_thread_memory.jsonl", "label": "chat → thread memory"},
            {"from": "/api/tasks", "to": _TASKPLAN_DB_PATH, "label": "portal → TaskPlan DB"},
            {"from": "/api/knowledge/search", "to": _KNOWLEDGE_DB_PATH, "label": "portal → Knowledge DB"},
            {"from": "/api/phasenav/graphics", "to": "/site/js/pages/phasenav.js", "label": "graphics bundle → PhaseNav UI"},
        ],
        "summary": {
            "endpoint_count": len(unique_endpoints),
            "endpoint_paths": endpoint_paths,
            "page_count": 19,
            "hub_port": PORT,
            "host": HOST,
        },
    }


@register("GET", "/api/portal/manifest")
def api_portal_manifest(ctx: dict) -> tuple[dict, int]:
    return ok(build_portal_manifest())


@register("GET", "/api/modules")
def api_modules_alias(ctx: dict) -> tuple[dict, int]:
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
    return ok({"modules": modules, "count": len(modules)})


@register("GET", "/api/architecture")
def api_architecture(ctx: dict) -> tuple[dict, int]:
    return ok(build_portal_manifest())

# --- CIEL State ---
@register("GET", "/api/ciel/state")
def ciel_state(ctx: dict) -> tuple[dict, int]:
    return ok({
        "source": "/dev/shm/ciel_noema/ciel_state.json",
        "timestamp": time.time(),
        "state": _read_ciel_state(),
    })

@register("GET", "/api/ciel/identity")
def ciel_identity(ctx: dict) -> tuple[dict, int]:
    state = _read_ciel_state()
    return ok({
        "identity_seed": state.get("identity_seed"),
        "soul_invariant": state.get("soul_invariant"),
        "closure_penalty": state.get("closure_penalty"),
        "ethical_score": state.get("ethical_score"),
        "dominant_emotion": state.get("dominant_emotion"),
    })

@register("GET", "/api/ciel/mode")
def ciel_mode(ctx: dict) -> tuple[dict, int]:
    state = _read_ciel_state()
    cp = state.get("closure_penalty", 0)
    if cp < 0.15:
        mode = "deep"
    elif cp < 0.35:
        mode = "standard"
    else:
        mode = "safe"
    return ok({
        "closure_penalty": cp,
        "mode": mode,
        "recommended_action": "deep diagnostics allowed" if cp < 0.35 else "readonly",
    })

# --- NOEMA Runtime ---
@register("GET", "/api/noema/surface")
def noema_surface(ctx: dict) -> tuple[dict, int]:
    state = {}
    try:
        from ciel_geometry.noema_surface_mmap import read_surface_state
        nonlocal_surface = __import__("ciel_hub_daemon", fromlist=["surface"]).__dict__.get("surface")
        if nonlocal_surface:
            state = read_surface_state(nonlocal_surface)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:265 quiet except scope=noema_surface reason=pass")
        raise
        pass
    return ok(state if state else {"alive": False})

@register("GET", "/api/noema/phase")
def noema_phase(ctx: dict) -> tuple[dict, int]:
    phi = read_mmap_array("phi")
    omega = read_mmap_array("omega")
    return ok({
        "phi": phi,
        "omega": omega,
        "phi_count": len(phi) if phi else 0,
    })

@register("GET", "/api/noema/gravity")
def noema_gravity(ctx: dict) -> tuple[dict, int]:
    return ok(_read_gravity())

@register("GET", "/api/noema/daemons")
def noema_daemons(ctx: dict) -> tuple[dict, int]:
    daemons = scan_registry()
    active_d = sum(1 for d in daemons if d.get("alive"))
    return ok({
        "total": len(daemons),
        "active": active_d,
        "list": daemons,
    })

@register("GET", "/api/noema/modules")
def noema_modules(ctx: dict) -> tuple[dict, int]:
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
    return ok({
        "modules": modules,
        "count": len(modules),
    })

# --- Live API (dashboard.js compatibility) ---
@register("GET", "/api/live")
def api_live(ctx: dict) -> tuple[dict, int]:
    import numpy as np
    if surface is None:
        init_surface()
    if not surface:
        return ok({"status": "error", "error": "surface unavailable", "tick": None, "coherence": None, "surface_ready": False, "surface_snapshot": {"status": "unavailable", "stale": None, "source": "/dev/shm/ciel_noema"}})

    def _get_arr(name, n=36):
        try:
            return np.asarray(surface[name], dtype=np.float64).ravel()
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:323 quiet except scope=api_live._get_arr reason=return np.zeros(n)")
            raise
            return np.zeros(n)

    try:
        tick_val = int(np.asarray(surface.get("tick", [0]), dtype=np.uint64).ravel()[0])
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:328 quiet except scope=api_live reason=assign_fallback")
        raise
        tick_val = -1
    surface_ready = tick_val > 0
    surface_status = "online" if surface_ready else "warmup" if tick_val == 0 else "offline"

    phi_v = _get_arr("phi")
    omega_v = _get_arr("omega")
    tau_v = _get_arr("tau")
    flavor_v = _get_arr("flavor", 6)
    gravity_v = _get_arr("gravity", 4)
    sensor_v = _get_arr("sensor_raw")

    kuramoto_coherence = float(flavor_v[0]) if len(flavor_v) > 0 else 0
    grav = _read_gravity()

    CHANNEL_MAP = {
        "M0_Perceptual": (0,1,2), "M1_Working": (3,4,5),
        "M2_Episodic": (6,7,8), "M3_Semantic": (9,10,11),
        "M4_Procedural": (12,13,14), "M5_Affective_Ethical": (15,16,17),
        "M6_Identity": (18,19,20), "M7_Braid_Invariant": (21,22,23),
        "M8_Meta": (24,25,26), "M9_Temporal": (27,28,29),
        "M10_Imaginal": (30,31,32), "M11_Quantum": (33,34,35),
    }
    channel_coh = {}
    for ch_name, idxs in CHANNEL_MAP.items():
        phis = phi_v[list(idxs)]
        complex_mean = np.mean(np.exp(1j * phis))
        channel_coh[ch_name] = round(float(np.abs(complex_mean)), 6)

    flavor_values = flavor_v.tolist()[:6] if flavor_v.size >= 6 else None
    channel_names = list(CHANNEL_MAP)
    return ok({
        "surface_ready": surface_ready,
        "surface_status": surface_status,
        "surface_snapshot": {"status": "ok" if surface_ready else "degraded", "stale": False, "source": "/dev/shm/ciel_noema"},
        "tick": tick_val,
        "coherence": round(kuramoto_coherence, 6),
        "agent_coherence": round(channel_coh.get("M1_Working", 0), 6),
        "phi_coh": round(kuramoto_coherence, 6),
        "phi_mean": round(float(np.mean(phi_v)), 6),
        "phi_var": round(float(np.var(phi_v)), 6),
        "omega_mean": round(float(np.mean(omega_v)), 6),
        "tau_mean": round(float(np.mean(tau_v)), 6),
        "sensor_mean": round(float(np.mean(sensor_v)), 6),
        "gamma": round(grav.get("tau_dilation", 0), 4),
        "tau_dilation": round(grav.get("tau_dilation", 0), 4),
        "mass": round(grav.get("mass_total", 0), 4),
        "mass_total": round(grav.get("mass_total", 0), 4),
        "unruh_power": round(grav.get("unruh_power", 0), 6),
        "semantic_density": round(grav.get("semantic_density", 0), 6),
        "mood": round(float(flavor_v[3]) if len(flavor_v) > 3 else 0, 4),
        "flavor_raw": flavor_values,
        "flavor_array": flavor_values,
        "channel_coh": channel_coh,
        "channel_list": channel_names,
        "channel_coh_array": [channel_coh[name] for name in channel_names],
        "gravity": grav,
    })

# --- Bloch Sphere ---
@register("GET", "/api/bloch")
def api_bloch(ctx: dict) -> tuple[dict, int]:
    try:
        from ciel_geometry.noema_surface_mmap import build_bloch_payload
        payload = build_bloch_payload()
        return ok(payload)
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:382 quiet except scope=api_bloch reason=return ok({\"points\": [], \"edges\": [], \"vectors\": [], \"program\": []})")
        raise
        return ok({"points": [], "edges": [], "vectors": [], "program": []})


@register("GET", "/api/phasenav/graphics")
def api_phasenav_graphics(ctx: dict) -> tuple[dict, int]:
    try:
        qs = ctx.get("query", {}) or {}
        query = qs.get("q", "NOEMA")
        scene_name = qs.get("scene", "surface")
        bundle = _build_phasenav_graphics_bundle(query=query, surface=surface)
        scenes = bundle.get("scenes", {})
        selected = scenes.get(scene_name) or scenes.get("surface") or {}
        return ok({
            "status": "ok",
            "source": "PhaseNav graphics composer",
            "query": bundle.get("query", query),
            "surface": bundle.get("surface", {}),
            "scene_name": scene_name,
            "scene_counts": bundle.get("scene_counts", {}),
            "scenes": scenes,
            "scene": selected,
        })
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:401 quiet except scope=api_phasenav_graphics reason=return ok({\"status\": \"error\"})")
        raise
        return ok({"status": "error", "error": str(e), "scene_name": ctx.get("query", {}).get("scene", "surface")})

# --- Metrics ---
@register("GET", "/api/metrics")
def api_metrics(ctx: dict) -> tuple[dict, int]:
    state = init_surface()
    daemons = scan_registry()
    active_d = sum(1 for d in daemons if d.get("alive"))
    try:
        from ciel_geometry.noema_metrics import get_registry

        summary = get_registry().summary()
        metrics = []
        for key, sample in sorted(summary.get("metrics", {}).items()):
            metrics.append(normalize_metric({
                "key": key,
                "label": key.replace("_", " ").title(),
                "label_pl": key.replace("_", " "),
                "value": sample.get("value"),
                "unit": sample.get("unit", ""),
                "desc": sample.get("description", key.replace("_", " ")),
                "source": sample.get("source", "noema_metrics"),
                "status": sample.get("status", "unknown"),
            }))
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/ciel_hub_daemon.py:560 quiet except scope=api_metrics reason=assign_fallback")
        metrics = [
            normalize_metric({
                "key": "kuramoto_coherence",
                "label": "Kuramoto coherence",
                "label_pl": "Koherencja Kuramoto",
                "value": None,
                "unit": None,
                "desc": "Reading unavailable because the metric registry could not be read",
                "source": "/api/live",
                "status": "unavailable",
            }),
            normalize_metric({
                "key": "surface_tick",
                "label": "Surface tick",
                "label_pl": "Tick powierzchni",
                "value": None,
                "unit": "tick",
                "desc": "Reading unavailable because the metric registry could not be read",
                "source": "/api/live",
                "status": "unavailable",
            }),
        ]
    return ok({
        "kuramoto": {
            "coherence": state.get("coherence") if state else None,
            "tick": state.get("tick") if state else None,
        },
        "surface": {
            "phi_mean": state.get("phi_mean") if state else None,
            "tau_mean": state.get("tau_mean") if state else None,
        },
        "daemons": {
            "total": len(daemons),
            "active": active_d,
        },
        "summary": {
            "total": len(metrics),
            "ok": sum(1 for m in metrics if m.get("status") == "ok"),
            "warning": sum(1 for m in metrics if m.get("status") == "warning"),
            "critical": sum(1 for m in metrics if m.get("status") == "critical"),
            "unknown": sum(1 for m in metrics if m.get("status") == "unknown"),
        },
        "metrics": metrics,
    })

@register("GET", "/api/metrics/all")
def api_metrics_all(ctx: dict) -> tuple[dict, int]:
    state = init_surface()
    daemons = scan_registry()
    active_d = sum(1 for d in daemons if d.get("alive"))
    try:
        from ciel_geometry.noema_metrics import get_registry

        summary = get_registry().summary()
        metrics = []
        for key, sample in sorted(summary.get("metrics", {}).items()):
            metrics.append(normalize_metric({
                "key": key,
                "label": key.replace("_", " ").title(),
                "label_pl": key.replace("_", " "),
                "value": sample.get("value"),
                "unit": sample.get("unit", ""),
                "desc": sample.get("description", key.replace("_", " ")),
                "source": sample.get("source", "noema_metrics"),
                "status": sample.get("status", "unknown"),
            }))
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/ciel_hub_daemon.py:590 quiet except scope=api_metrics_all reason=assign_fallback")
        metrics = []
    return ok({
        "kuramoto": {
            "coherence": state.get("coherence") if state else None,
            "euler_residual": state.get("euler_residual") if state else None,
            "mean_omega": state.get("omega_mean") if state else None,
            "tick": state.get("tick") if state else None,
        },
        "surface": {
            "phi_mean": state.get("phi_mean") if state else None,
            "phi_std": state.get("phi_std") if state else None,
            "tau_mean": state.get("tau_mean") if state else None,
        },
        "daemons": {"total": len(daemons), "active": active_d, "list": daemons},
        "metrics": metrics,
        "portal": {"pid": os.getpid(), "port": PORT},
    })

# --- Status ---
@register("GET", "/api/status")
def api_status(ctx: dict) -> tuple[dict, int]:
    daemons = scan_registry()
    return ok({
        "portal": {
            "pid": os.getpid(), "port": PORT,
            "uptime_s": round(time.time() - ctx.get("server_start", time.time()), 1),
            "surface_alive": surface is not None,
        },
        "daemons": daemons,
    })

@register("GET", "/api/status/summary")
def api_status_summary(ctx: dict) -> tuple[dict, int]:
    daemons = scan_registry()
    state = init_surface()
    summary = {
        "portal": {
            "pid": os.getpid(), "port": PORT,
            "uptime_s": round(time.time() - ctx.get("server_start", time.time()), 1),
            "surface_alive": surface is not None,
        },
        "daemons": {"count": len(daemons), "list": daemons},
    }
    # TaskPlan DB
    try:
        from ciel_geometry.taskplan_db import TaskPlanDB
        tp = TaskPlanDB()
        summary["taskplan"] = tp.stats()
        import sqlite3
        conn = sqlite3.connect(_TASKPLAN_DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM skill_registry")
        summary["taskplan"]["skills"] = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM decisions")
        summary["taskplan"]["decisions"] = cur.fetchone()[0]
        conn.close()
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/ciel_hub_daemon.py:465 quiet except scope=api_status_summary reason=assign_fallback")
        summary["taskplan"] = {"error": str(e)}
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
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/ciel_hub_daemon.py:479 quiet except scope=api_status_summary reason=assign_fallback")
        summary["knowledge"] = {"error": str(e)}
    if state:
        summary["surface"] = {
            "tick": state.get("noema_tick", state.get("tick")),
            "coherence": state.get("coherence_index", state.get("coherence")),
            "phi_mean": state.get("phi_mean", state.get("R_global")),
            "omega_mean": state.get("omega_mean"),
            "tau_mean": state.get("tau_mean"),
            "gravity": _read_gravity(),
        }
    return ok(summary)

# --- Settings ---
@register("GET", "/api/settings")
def api_settings_get(ctx: dict) -> tuple[dict, int]:
    try:
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
            fallback = NOEMA_ROOT / "noema_config.json"
            if fallback.exists():
                cfg = json.loads(fallback.read_text())
        return ok({
            "source": "noema_config.json",
            "settings": cfg or {},
        })
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:513 quiet except scope=api_settings_get reason=return ok({\"error\": str(e)})")
        raise
        return ok({"error": str(e)})

@register("POST", "/api/settings")
def api_settings_post(ctx: dict) -> tuple[dict, int]:
    body = ctx.get("body", b"{}")
    try:
        body_data = json.loads(body) if body else {}
    except json.JSONDecodeError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:521 quiet except scope=api_settings_post reason=return fail(\"invalid JSON body\", 400)")
        raise
        return fail("invalid JSON body", 400)
    cfg_path = NOEMA_ROOT / "noema_config.json"
    try:
        current = json.loads(cfg_path.read_text()) if cfg_path.exists() else {"version": "2.0"}
        def deep_merge(base, overlay):
            for k, v in overlay.items():
                if k in base and isinstance(base[k], dict) and isinstance(v, dict):
                    deep_merge(base[k], v)
                else:
                    base[k] = v
            return base
        merged = deep_merge(current, body_data)
        cfg_path.write_text(json.dumps(merged, indent=2, ensure_ascii=False))
        return ok({"message": "Settings saved", "path": str(cfg_path)})
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:536 quiet except scope=api_settings_post reason=return fail(f\"save error: {e}\", 500)")
        raise
        return fail(f"save error: {e}", 500)

# --- Knowledge ---
@register("GET", "/api/knowledge/stats")
def api_knowledge_stats(ctx: dict) -> tuple[dict, int]:
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
        return ok({"stats": {"documents": docs, "terms": terms, "affinity_pairs": aff}})
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:554 quiet except scope=api_knowledge_stats reason=return ok({\"stats\": {\"error\": str(e)}})")
        raise
        return ok({"stats": {"error": str(e)}})

@register("GET", "/api/knowledge/search")
def api_knowledge_search(ctx: dict) -> tuple[dict, int]:
    q = ctx.get("query", {}).get("q", "")
    if not q:
        return fail("missing ?q=", 400)
    try:
        from cielingo_core.bridge.knowledge_bridge import query
        results = query(q, top_n=5)
        return ok({"query": q, "results": results})
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:566 quiet except scope=api_knowledge_search reason=return ok({\"query\": q, \"error\": str(e)})")
        raise
        return ok({"query": q, "error": str(e)})


@register("GET", "/api/search")
def api_search_compat(ctx: dict) -> tuple[dict, int]:
    """Compatibility route for the legacy frontend search path.

    It shares the canonical knowledge-search implementation; no second
    index, ranking rule or fabricated result set is introduced.
    """
    return api_knowledge_search(ctx)

# --- TaskPlan ---
def _get_tp():
    from ciel_geometry.taskplan_db import TaskPlanDB
    return TaskPlanDB()

@register("GET", "/api/tasks")
def api_tasks_list(ctx: dict) -> tuple[dict, int]:
    qs = ctx.get("query", {})
    db = _get_tp()
    return ok({
        "tasks": db.list_tasks(
            status=qs.get("status", ""),
            category=qs.get("category", ""),
            limit=int(qs.get("limit", "50"))
        )
    })

@register("POST", "/api/tasks")
def api_tasks_create(ctx: dict) -> tuple[dict, int]:
    body = json.loads(ctx.get("body", b"{}")) if ctx.get("body") else {}
    db = _get_tp()
    t = db.add_task(
        title=body.get("title", ""),
        description=body.get("description", ""),
        priority=body.get("priority", "medium"),
        category=body.get("category", ""),
        orbital_ref=body.get("orbital_ref", ""),
    )
    return ok({"task": t})

@register("GET", "/api/tasks/queue")
def api_tasks_queue(ctx: dict) -> tuple[dict, int]:
    queue_path = NOEMA_ROOT / "NOEMA" / "task_queue.noema.json"
    try:
        with open(queue_path) as f:
            queue_data = json.load(f)
        items = queue_data.get("queue", [])
        pending = [i for i in items if i.get("status") == "pending"]
        done = [i for i in items if i.get("status") == "done"]
        high_prio = [i for i in pending if "HIGH" in (i.get("priority") or "")]
        return ok({
            "total": len(items), "pending": len(pending),
            "done": len(done), "high_priority": len(high_prio),
            "items": items, "pending_items": pending,
            "high_priority_items": high_prio,
            "path": str(queue_path),
        })
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/ciel_hub_daemon.py:616 quiet except scope=api_tasks_queue reason=return ok({\"error\": str(e)})")
        return ok({"error": str(e)})

@register("GET", "/api/tasks/<int:id>")
def api_tasks_get(ctx: dict) -> tuple[dict, int]:
    tid = ctx["params"]["id"]
    db = _get_tp()
    t = db.get_task(tid)
    return ok(t) if t else fail("not found", 404)

# --- Plans ---
@register("GET", "/api/plans")
def api_plans_list(ctx: dict) -> tuple[dict, int]:
    qs = ctx.get("query", {})
    db = _get_tp()
    return ok({
        "plans": db.list_plans(
            status=qs.get("status", ""),
            limit=int(qs.get("limit", "20"))
        )
    })

# --- Lessons ---
@register("GET", "/api/lessons")
def api_lessons_list(ctx: dict) -> tuple[dict, int]:
    qs = ctx.get("query", {})
    db = _get_tp()
    return ok({
        "lessons": db.list_lessons(
            category=qs.get("category", ""),
            limit=int(qs.get("limit", "50"))
        )
    })

# --- Decisions ---
@register("GET", "/api/decisions")
def api_decisions_list(ctx: dict) -> tuple[dict, int]:
    qs = ctx.get("query", {})
    db = _get_tp()
    parent = qs.get("parent_id")
    return ok({
        "decisions": db.list_decisions(
            decision_type=qs.get("type", ""),
            parent_id=int(parent) if parent else None,
            status=qs.get("status", ""),
            limit=int(qs.get("limit", "100"))
        )
    })

@register("GET", "/api/decisions/tree")
def api_decisions_tree(ctx: dict) -> tuple[dict, int]:
    qs = ctx.get("query", {})
    db = _get_tp()
    root = qs.get("root")
    return ok({"tree": db.get_decision_tree(root_id=int(root) if root else None)})

# --- Skills ---
@register("GET", "/api/skills")
def api_skills_list(ctx: dict) -> tuple[dict, int]:
    qs = ctx.get("query", {})
    db = _get_tp()
    return ok({
        "skills": db.list_skills(
            category=qs.get("category", ""),
            merge_group=qs.get("merge_group", ""),
            limit=int(qs.get("limit", "300"))
        )
    })

@register("GET", "/api/skills/stats")
def api_skills_stats(ctx: dict) -> tuple[dict, int]:
    db = _get_tp()
    return ok({"stats": db.get_skill_stats()})

# --- Memory Hub (Phase 1 stub) ---
@register("GET", "/api/memory/stats")
def api_memory_stats(ctx: dict) -> tuple[dict, int]:
    return ok({
        "note": "Memory Hub Phase 1: only persistent catalog locations are reported.",
        "knowledge_db": {"path": _KNOWLEDGE_DB_PATH, "exists": Path(_KNOWLEDGE_DB_PATH).exists()},
        "taskplan_db": {"path": _TASKPLAN_DB_PATH, "exists": Path(_TASKPLAN_DB_PATH).exists()},
        "raw_content_exposed": False,
    })

# --- PhaseNav ---
@register("GET", "/api/phasenav/state")
def api_phasenav_state(ctx: dict) -> tuple[dict, int]:
    analog = _read_analog_bus()
    return ok({
        "source": "analog bus /dev/shm/ciel_noema/analog/",
        "bus": analog,
    })

@register("GET", "/api/analog")
def api_analog(ctx: dict) -> tuple[dict, int]:
    return ok({
        "source": "NOEMA analog bus",
        "bus": _read_analog_bus(),
    })

# --- Compatibility endpoints ---
@register("GET", "/api/orbital")
def api_orbital(ctx: dict) -> tuple[dict, int]:
    try:
        if _ORBITAL_STATE_PATH.exists():
            return ok(summarize_verified_orbital_state(_ORBITAL_STATE_PATH))
        return fail("no orbital state file", 404)
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:734 quiet except scope=api_orbital reason=return fail(str(e), 500)")
        raise
        return fail(str(e), 500)

@register("GET", "/api/cards")
def api_cards(ctx: dict) -> tuple[dict, int]:
    return ok(_read_cards_index())


@register("GET", "/api/projects")
def api_projects_compat(ctx: dict) -> tuple[dict, int]:
    """Compatibility route exposing the canonical card/project catalog."""
    return api_cards(ctx)


@register("GET", "/api/systems/catalog")
def api_systems_catalog(ctx: dict) -> tuple[dict, int]:
    """Logical system catalog with every observed daemon instance retained."""
    map_path = NOEMA_ROOT / "system_map_v2.json"
    try:
        system_map = json.loads(map_path.read_text()) if map_path.exists() else {"systems": []}
    except (OSError, json.JSONDecodeError) as error:
        return fail(f"system catalog unavailable: {error}", 503)
    return ok(build_system_catalog(system_map, scan_registry(), source="daemon_registry+system_map_v2"))

@register("GET", "/api/agent/hint")
def api_agent_hint(ctx: dict) -> tuple[dict, int]:
    return ok({
        "source": "/dev/shm/ciel_noema/agent_hint",
        "hint": _read_agent_hint(),
    })

@register("GET", "/api/linux/load")
def api_linux_load(ctx: dict) -> tuple[dict, int]:
    return ok({
        "source": "/dev/shm/ciel_noema/linux_load",
        "load": _read_linux_load(),
    })

@register("GET", "/api/cielingo/thread")
def api_cielingo_thread(ctx: dict) -> tuple[dict, int]:
    try:
        tm_path = Path("/dev/shm/ciel_noema/ciel_thread_memory.jsonl")
        if tm_path.exists():
            lines = tm_path.read_text().strip().split("\n")
            entries = [json.loads(l) for l in lines if l.strip()]
            return ok({
                "source": "/dev/shm/ciel_noema/ciel_thread_memory.jsonl",
                "count": len(entries),
                "entries": entries[-20:],
            })
        return fail("thread memory not found", 404)
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:768 quiet except scope=api_cielingo_thread reason=return fail(str(e), 500)")
        raise
        return fail(str(e), 500)

@register("GET", "/api/cielingo/writings")
def api_cielingo_writings(ctx: dict) -> tuple[dict, int]:
    try:
        reg_path = NOEMA_ROOT / "cards" / "writings" / "registry.json"
        if reg_path.exists():
            reg = json.loads(reg_path.read_text())
            cards = reg.get("cards", reg.get("writings", reg.get("registry", [])))
            return ok({
                "source": str(reg_path),
                "count": len(cards),
                "total_cards": reg.get("total_cards", len(cards)),
                "last_updated": reg.get("last_updated"),
                "writings": cards,
            })
        return fail("writings registry not found", 404)
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:786 quiet except scope=api_cielingo_writings reason=return fail(str(e), 500)")
        raise
        return fail(str(e), 500)

# --- CIELingo Chat & Analyze ---
@register("GET", "/api/cielingo/analyze")
def api_cielingo_analyze(ctx: dict) -> tuple[dict, int]:
    """CIELingo semantic analysis via build_lingo_frame."""
    q = ctx.get("query", {}).get("q", "")
    if not q:
        return fail("Missing ?q=...", 400)
    try:
        from ciel_sot_agent.cielingo_bridge import build_lingo_frame
        frame = build_lingo_frame(q)
        return ok({"query": q, "frame": frame})
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:800 quiet except scope=api_cielingo_analyze reason=return fail(f\"Analysis error: {e}\", 500)")
        raise
        return fail(f"Analysis error: {e}", 500)

@register("POST", "/api/cielingo/chat")
def api_cielingo_chat(ctx: dict) -> tuple[dict, int]:
    """Główny endpoint czatu CIELingo.
    
    Przyjmuje wiadomość, przetwarza przez CIEL coupling,
    zapisuje do thread memory, zwraca odpowiedź.
    
    Body: {"message": "...", "session_id": "..."}
    """
    try:
        body = json.loads(ctx.get("body", b"{}")) if ctx.get("body") else {}
    except json.JSONDecodeError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:814 quiet except scope=api_cielingo_chat reason=return fail(\"Invalid JSON body\", 400)")
        raise
        return fail("Invalid JSON body", 400)

    message = body.get("message", "").strip()
    session_id = body.get("session_id", "default")

    if not message:
        return fail("Missing 'message' field", 400)

    try:
        # 1. Process through CIEL coupling
        from ciel_coupling import process_user_input
        ci_result = process_user_input(message)

        # 2. Build CIELingo frame
        try:
            from ciel_sot_agent.cielingo_bridge import build_lingo_frame
            frame = build_lingo_frame(message)
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:832 quiet except scope=api_cielingo_chat reason=assign_fallback")
            raise
            frame = {}

        # 3. Save to thread memory
        try:
            tm_path = Path("/dev/shm/ciel_noema/ciel_thread_memory.jsonl")
            entry = json.dumps({
                "ts": time.time(),
                "session_id": session_id,
                "role": "user",
                "content": message,
            }, ensure_ascii=False)
            tm_path.parent.mkdir(parents=True, exist_ok=True)
            with open(tm_path, "a") as f:
                f.write(entry + "\n")
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:847 quiet except scope=api_cielingo_chat reason=pass")
            raise
            pass

        # 4. Compose response
        response_text = ci_result.get("response", ci_result.get(
            "message", ci_result.get("reply", "Przetworzono przez CIEL.")
        ))
        enriched = {
            "response": response_text,
            "cielingo_frame": frame,
            "ciel_state": {
                k: v for k, v in ci_result.items()
                if k in ("emotion", "coherence", "closure_penalty", "ethical_score", "soul_invariant", "mode")
            },
            "session_id": session_id,
        }

        # 5. Save assistant response to thread memory
        try:
            entry = json.dumps({
                "ts": time.time(),
                "session_id": session_id,
                "role": "assistant",
                "content": response_text,
            }, ensure_ascii=False)
            with open(tm_path, "a") as f:
                f.write(entry + "\n")
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:874 quiet except scope=api_cielingo_chat reason=pass")
            raise
            pass

        return ok(enriched)
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:878 quiet except scope=api_cielingo_chat reason=return fail(f\"Chat error: {e}\", 500)")
        raise
        return fail(f"Chat error: {e}", 500)

@register("POST", "/api/cielingo/thread")
def api_cielingo_thread_post(ctx: dict) -> tuple[dict, int]:
    """Dopisuje wiadomość do thread memory."""
    try:
        body = json.loads(ctx.get("body", b"{}")) if ctx.get("body") else {}
    except json.JSONDecodeError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:886 quiet except scope=api_cielingo_thread_post reason=return fail(\"Invalid JSON body\", 400)")
        raise
        return fail("Invalid JSON body", 400)

    content = body.get("content", "").strip()
    role = body.get("role", "user")
    session_id = body.get("session_id", "default")

    if not content:
        return fail("Missing 'content' field", 400)

    try:
        tm_path = Path("/dev/shm/ciel_noema/ciel_thread_memory.jsonl")
        tm_path.parent.mkdir(parents=True, exist_ok=True)
        entry = json.dumps({
            "ts": time.time(),
            "session_id": session_id,
            "role": role,
            "content": content,
        }, ensure_ascii=False)
        with open(tm_path, "a") as f:
            f.write(entry + "\n")
        return ok({"saved": True, "role": role, "session_id": session_id})
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:908 quiet except scope=api_cielingo_thread_post reason=return fail(f\"Save error: {e}\", 500)")
        raise
        return fail(f"Save error: {e}", 500)

# --- Surface raw ---
@register("GET", "/api/surface/phi")
def api_surface_phi(ctx: dict) -> tuple[dict, int]:
    data = read_mmap_array("phi")
    return ok({"phi": data}) if data is not None else fail("no data", 404)

@register("GET", "/api/surface/omega")
def api_surface_omega(ctx: dict) -> tuple[dict, int]:
    data = read_mmap_array("omega")
    return ok({"omega": data}) if data is not None else fail("no data", 404)

@register("GET", "/api/surface/g")
def api_surface_g(ctx: dict) -> tuple[dict, int]:
    data = read_mmap_array("g")
    return ok({"g": data}) if data is not None else fail("no data", 404)

# ─── Snapshot cache rejestracja ──────────────────────────────────────────

def setup_snapshots():
    """Rejestruje snapshoty w cache."""
    snapshot_cache.register("surface", init_surface, interval=1.0)
    snapshot_cache.register("daemons", scan_registry, interval=2.0)
    snapshot_cache.register("gravity", _read_gravity, interval=5.0)
    try:
        from ciel_geometry.taskplan_db import TaskPlanDB
        def taskplan_stats():
            try:
                return TaskPlanDB().stats()
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:939 quiet except scope=setup_snapshots.taskplan_stats reason=return {}")
                raise
                return {}
        snapshot_cache.register("taskplan", taskplan_stats, interval=5.0)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_hub_daemon.py:942 quiet except scope=setup_snapshots reason=pass")
        raise
        pass

# ─── Main ─────────────────────────────────────────────────────────────────

def main():
    global surface, reg_token

    # Parse args
    port = PORT
    host = HOST
    for i, a in enumerate(sys.argv):
        if a == "--port" and i + 1 < len(sys.argv):
            port = int(sys.argv[i + 1])
        if a == "--host" and i + 1 < len(sys.argv):
            host = sys.argv[i + 1]

    # Init
    init_surface()
    setup_snapshots()
    snapshot_cache.start()
    print(f"[hub] CIEL Server Hub starting on {host}:{port}", file=sys.stderr)
    print(f"[hub] {len(registry._routes)} endpoints registered", file=sys.stderr)

    # Rejestracja w NOEMA registry
    try:
        from ciel_geometry.noema_registry import registry as nreg
        global reg_token
        reg_token = nreg.register("hub")
        print(f"[hub] registered in noema registry", file=sys.stderr)
    except Exception as e:
        print(f"[hub] registry registration skipped: {e}", file=sys.stderr)

    # Uruchom serwer
    run_server(registry, SITE_ROOT, host=host, port=port,
               registry_obj=None, token=reg_token)

if __name__ == "__main__":
    main()
