#!/usr/bin/env python3
"""CIELingo MCP server — 7 narzędzi dla opencode przez JSON-RPC over stdio.

Usage:
    PYTHONPATH=src .venv/bin/python3 scripts/cielingo_mcp_server.py

Protocol: MCP JSON-RPC over stdio using Content-Length framing.
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import math
import os
import struct
import sys
import time
from pathlib import Path

import numpy as np

# ── Config ─────────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent
SURFACE_DIR = Path("/dev/shm/ciel_noema")
_AGENT_HEALTH_URL = "http://localhost:18520/health"

# Lazy import agent client
_agent_analyze = None
try:
    from cielingo_core.bridge.agent_client import analyze as _agent_analyze
except Exception:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/cielingo_mcp_server.py:32 quiet except scope=<module> reason=pass")
    raise
    pass

try:
    from ciel_geometry.new_volume_bridge import status as _nv_status
except Exception:
    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/cielingo_mcp_server.py:37 quiet except scope=<module> reason=assign_fallback")
    raise
    _nv_status = None

# Lazy import knowledge bridge
_knowledge = None


def _get_knowledge():
    global _knowledge
    if _knowledge is None:
        try:
            from cielingo_core.bridge.knowledge_bridge import (
                check_coverage,
                get_neighbors,
                query,
            )
            _knowledge = {"query": query, "check_coverage": check_coverage, "get_neighbors": get_neighbors}
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/cielingo_mcp_server.py:54 quiet except scope=_get_knowledge reason=assign_fallback")
            raise
            _knowledge = False
    return _knowledge if _knowledge else None


# Sapiens client
_sapiens = None
_sapiens_session = None


def _get_sapiens():
    global _sapiens, _sapiens_session
    if _sapiens is None:
        try:
            from ciel_sot_agent.sapiens_client import (
                SapiensIdentity,
                append_turn,
                build_model_packet,
                initialize_session,
                persist_latest_packet,
            )
            _sapiens = {
                "SapiensIdentity": SapiensIdentity,
                "append_turn": append_turn,
                "build_model_packet": build_model_packet,
                "initialize_session": initialize_session,
                "persist_latest_packet": persist_latest_packet,
            }
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/cielingo_mcp_server.py:82 quiet except scope=_get_sapiens reason=assign_fallback")
            raise
            _sapiens = False
    return _sapiens if _sapiens else None


# ── Helper ─────────────────────────────────────────────────────────────


def _tool(name: str, desc: str, input_schema: dict, handler) -> dict:
    return {"name": name, "description": desc, "inputSchema": input_schema, "_handler": handler}


# ── CIEL ORBITAL BINDING — PHASENAV HTRI monitor handler ──────────────

_HTRI_BINDING_ATTRACTOR_DEG = [
    0.0, 30.0, 60.0, 90.0, 120.0, 150.0,
    180.0, 210.0, 240.0, 270.0, 300.0, 330.0,
    15.0, 45.0, 75.0, 105.0, 135.0, 165.0,
    195.0, 225.0, 255.0, 285.0, 315.0, 345.0,
    7.5, 37.5, 67.5, 97.5, 127.5, 157.5,
    187.5, 217.5, 247.5, 277.5, 307.5, 337.5,
]
_HTRI_TARGET = np.deg2rad(_HTRI_BINDING_ATTRACTOR_DEG)
_HTRI_TOLERANCE = 0.3

def _binding_cdist(a, b):
    d = abs(a - b) % (2 * math.pi)
    return min(d, 2 * math.pi - d)

def _handle_binding_status(args: dict) -> dict:
    """PHASENAV-HTRI binding monitor — sprawdza binding w przestrzeni fazowej."""
    try:
        # Odczytaj phi z surface
        phi_path = SURFACE_DIR / "phi"
        phi = None
        if phi_path.exists():
            data = np.fromfile(phi_path, dtype=np.float64)
            if len(data) == 36:
                phi = data
        
        # Odczytaj R
        r_path = SURFACE_DIR / "R"
        R = 0.0
        if r_path.exists():
            R = float(np.fromfile(r_path, dtype=np.float64)[0])
        
        # Sprawdź status bindingu
        status_path = SURFACE_DIR / "ciel_binding_status"
        binding_active = False
        if status_path.exists():
            binding_active = status_path.read_text().strip() == "ACTIVE"
        
        errors = []
        phase_ok = False
        phase_dist = None
        
        if phi is not None:
            dists = [_binding_cdist(phi[i], _HTRI_TARGET[i]) for i in range(36)]
            phase_dist = sum(dists) / 36
            phase_ok = phase_dist <= _HTRI_TOLERANCE
            if not phase_ok:
                errors.append(f"PHASE_DRIFT: mean={phase_dist:.4f} > tol={_HTRI_TOLERANCE}")
        
        coh_ok = R >= 0.3
        if not coh_ok:
            errors.append(f"COHERENCE_LOW: R={R:.4f} < 0.3")
        
        if not binding_active:
            errors.append("BINDING_STATUS_INACTIVE")
        
        passed = phase_ok and coh_ok and binding_active
        
        return {
            "phasenav": "φ[binding] = HTRI_PHASE_ATTRACTOR",
            "R": round(R, 4),
            "phase_distance": round(phase_dist, 4) if phase_dist is not None else None,
            "binding_status": "ACTIVE" if binding_active else "INACTIVE",
            "passed": passed,
            "errors": errors,
            "timestamp": time.time(),
        }
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/cielingo_mcp_server.py:163 quiet except scope=_handle_binding_status reason=return {\"error\": str(e)}")
        raise
        return {"error": str(e)}

# ── Tool handlers ──────────────────────────────────────────────────────


def _handle_knowledge_query(args: dict) -> dict:
    kb = _get_knowledge()
    if not kb:
        return {"error": "knowledge bridge not available"}
    text = args.get("text", "")
    top_n = args.get("top_n", 3)
    return kb["query"](text, top_n=top_n)


def _handle_knowledge_coverage(args: dict) -> dict:
    kb = _get_knowledge()
    if not kb:
        return {"error": "knowledge bridge not available"}
    text = args.get("text", "")
    return kb["check_coverage"](text)


def _handle_agent_analyze(args: dict) -> dict:
    if _agent_analyze is None:
        return {"error": "agent backend client not available"}
    text = args.get("text", "")
    if not text:
        return {"error": "empty text"}
    result = _agent_analyze(text)
    return result


def _handle_agent_health(args: dict) -> dict:
    try:
        import urllib.request

        resp = urllib.request.urlopen(_AGENT_HEALTH_URL, timeout=2)
        alive = resp.status == 200
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/cielingo_mcp_server.py:202 quiet except scope=_handle_agent_health reason=assign_fallback")
        raise
        alive = False
    return {"alive": alive, "port": 18520}


def _handle_surface_read(args: dict) -> dict:
    import numpy as np

    result = {}
    for name, dtype, count in [("phi", "d", 24), ("omega", "d", 24), ("flavor", "d", 6), ("gravity", "d", 8), ("tick", "Q", 1)]:
        path = SURFACE_DIR / name
        if path.exists():
            try:
                raw = path.read_bytes()
                if dtype == "Q":
                    vals = struct.unpack("<Q", raw)
                    result["tick"] = vals[0]
                else:
                    vals = np.frombuffer(raw, dtype=np.float64)
                    if name == "phi":
                        result["phi_coh"] = round(float(np.abs(np.mean(np.exp(1j * vals)))), 4)
                        result["phi_mean"] = round(float(np.mean(vals)), 4)
                    elif name == "omega":
                        result["omega_mean"] = round(float(np.mean(vals)), 4)
                        result["omega_std"] = round(float(np.std(vals)), 4)
                    elif name == "gravity":
                        labels = ["density", "gamma", "mass", "unruh", "scar_cnt", "agent_ok", "scar_rate", "scar_severity"]
                        for li, (l, v) in enumerate(zip(labels, vals)):
                            result[f"g_{l}"] = round(float(v), 4)
                    elif name == "flavor":
                        for i, v in enumerate(vals):
                            result[f"flavor_{i}"] = round(float(v), 4)
            except Exception as e:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/cielingo_mcp_server.py:234 quiet except scope=_handle_surface_read reason=assign_fallback")
                raise
                result[name] = str(e)
    result["path"] = str(SURFACE_DIR)
    return result


def _handle_daemon_status(args: dict) -> dict:
    try:
        from ciel_geometry.daemon_registry import Registry

        reg = Registry()
        daemons = []
        for d in reg.scan():
            daemons.append({"name": d.name, "pid": d.pid, "tick": d.tick, "status": d.status, "alive": d.alive})
        return {"daemons": daemons, "count": len(daemons)}
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/cielingo_mcp_server.py:249 quiet except scope=_handle_daemon_status reason=return {\"error\": str(e)}")
        raise
        return {"error": str(e)}


def _handle_list_skills(args: dict) -> dict:
    skills_dir = ROOT / ".opencode" / "skills"
    if not skills_dir.exists():
        return {"skills": [], "error": "skills directory not found"}
    skills = []
    for entry in sorted(skills_dir.iterdir()):
        if entry.is_dir():
            md_path = entry / "SKILL.md"
            desc = ""
            if md_path.exists():
                try:
                    for line in md_path.read_text().splitlines():
                        if line.startswith("## Description") or line.startswith("description"):
                            desc = line.split(":", 1)[-1].strip() if ":" in line else ""
                            break
                except Exception:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/cielingo_mcp_server.py:268 quiet except scope=_handle_list_skills reason=pass")
                    raise
                    pass
            skills.append({"name": entry.name, "description": desc[:200] if desc else ""})
    return {"skills": skills, "count": len(skills)}


def _handle_sapiens_session(args: dict) -> dict:
    sap = _get_sapiens()
    if not sap:
        return {"error": "sapiens client not available"}
    import signal as _sig

    global _sapiens_session
    text = args.get("text", "")
    identity_id = args.get("sapiens_id", "sapiens")

    class TimeoutError_R(Exception):
        pass

    def _alarm(signum, frame):
        raise TimeoutError_R("sapiens initialize_session timed out (5s)")

    if _sapiens_session is None:
        old = _sig.signal(_sig.SIGALRM, _alarm)
        _sig.alarm(5)
        try:
            _sapiens_session = sap["initialize_session"](
                ROOT, identity=sap["SapiensIdentity"](sapiens_id=identity_id)
            )
            _sig.alarm(0)
        except TimeoutError_R:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/cielingo_mcp_server.py:298 quiet except scope=_handle_sapiens_session reason=no_log_no_raise")
            raise
            _sig.alarm(0)
            _sig.signal(_sig.SIGALRM, old)
            return {"error": "sapiens initialize_session timed out — orbital bridge unavailable"}
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/cielingo_mcp_server.py:302 quiet except scope=_handle_sapiens_session reason=no_log_no_raise")
            raise
            _sig.alarm(0)
            _sig.signal(_sig.SIGALRM, old)
            return {"error": f"sapiens init failed: {e}"}
        _sig.signal(_sig.SIGALRM, old)
    try:
        packet = sap["build_model_packet"](_sapiens_session, text)
        try:
            sap["persist_latest_packet"](ROOT, packet)
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/cielingo_mcp_server.py:311 quiet except scope=_handle_sapiens_session reason=pass")
            raise
            pass
        policy = packet.get("surface_policy", {})
        geom = packet.get("state_geometry", {})
        return {
            "sapiens_id": identity_id,
            "packet_schema": packet.get("schema"),
            "mode": policy.get("mode", "?"),
            "coherence": geom.get("internal_cymatics", {}).get("coherence_index", 0),
            "closure": geom.get("internal_cymatics", {}).get("closure_penalty", 0),
            "turn_count": len(_sapiens_session.memory),
            "updated_at": packet.get("session", {}).get("updated_at", ""),
        }
    except TimeoutError_R:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/cielingo_mcp_server.py:324 quiet except scope=_handle_sapiens_session reason=return {\"error\": \"sapiens build_model_packet timed out\"}")
        raise
        return {"error": "sapiens build_model_packet timed out"}
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/cielingo_mcp_server.py:326 quiet except scope=_handle_sapiens_session reason=return {\"error\": f\"sapiens build_model_packet failed: {e}\"}")
        raise
        return {"error": f"sapiens build_model_packet failed: {e}"}


def _handle_orchestrator_status(args: dict) -> dict:
    try:
        import subprocess
        r = subprocess.run(
            [sys.executable, str(ROOT / "scripts/noema_orchestrator.py"), "--once"],
            capture_output=True, text=True, timeout=10,
        )
        return json.loads(r.stdout) if r.stdout else {"error": "empty output"}
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/cielingo_mcp_server.py:338 quiet except scope=_handle_orchestrator_status reason=return {\"error\": str(e)}")
        raise
        return {"error": str(e)}


def _handle_new_volume(args: dict) -> dict:
    if _nv_status is None:
        return {"available": False, "error": "new_volume_bridge not loaded"}
    return _nv_status()


def _handle_linux_cards(args: dict) -> dict:
    """Rozszerzony linux_cards — 8 typów kart, per-type filter."""
    try:
        from ciel_geometry.linux_cards import LinuxCardIndex
        max_procs = args.get("max_procs", 200)
        card_type = args.get("type", "all").upper()
        idx = LinuxCardIndex(max_procs=min(max_procs, 500),
                             enabled_types={"PROC","CPU","DISK","NET_IF","NET_CONN","MODULE","MOUNT","PCI_DEV","SENSOR"})
        start = time.time()
        n = idx.update()
        scan_ms = int((time.time() - start) * 1000)
        stats = idx.summary_stats()
        by_type = stats.get("by_type", {})

        resp = {
            "total_cards": n,
            "by_type": by_type,
            "scan_ms": scan_ms,
        }

        if card_type != "all":
            names = {"PROC": "processes", "CPU": "cpu_cores", "DISK": "disks",
                     "NET_IF": "net_ifaces", "NET_CONN": "net_conns",
                     "MODULE": "modules", "MOUNT": "mounts", "PCI_DEV": "pci_devs",
                     "SENSOR": "sensors"}
            items = idx.by_type(card_type)
            resp[f"{names.get(card_type, card_type.lower())}"] = [
                {k: v for k, v in c.items() if k != "phi"} for c in items[:20]
            ]
            resp["total_type"] = len(items)
        else:
            top = idx.top_cpu(10)
            resp["top_cpu"] = [{"pid": t.get("pid"), "name": t.get("name"),
                                "cpu": t.get("cpu_percent", 0),
                                "mem": t.get("memory_percent", 0)}
                               for t in top]
            resp["cpu_cores"] = len(idx.by_type("CPU"))
            resp["disks"] = len(idx.by_type("DISK"))
            resp["net_ifaces"] = len(idx.by_type("NET_IF"))
            resp["net_conns"] = len(idx.by_type("NET_CONN"))
            resp["modules"] = len(idx.by_type("MODULE"))
            resp["mounts"] = len(idx.by_type("MOUNT"))
            resp["pci_devs"] = len(idx.by_type("PCI_DEV"))
            resp["sensors"] = len(idx.by_type("SENSOR"))

        return resp
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/cielingo_mcp_server.py:394 quiet except scope=_handle_linux_cards reason=return {\"error\": str(e)}")
        raise
        return {"error": str(e)}


def _handle_linux_hardware(args: dict) -> dict:
    """Hardware summary z /dev/shm lub live scan."""
    try:
        cards_dir = Path("/dev/shm/ciel_noema/linux_cards")
        hw_file = cards_dir / "hardware.json"
        if hw_file.exists():
            hw = json.loads(hw_file.read_text())
        else:
            hw = {"error": "no hardware data"}

        cpu_file = cards_dir / "cpu_summary.json"
        cpu = json.loads(cpu_file.read_text()) if cpu_file.exists() else {}

        nearby_file = cards_dir / "nearby_surface.json"
        nearby = json.loads(nearby_file.read_text()) if nearby_file.exists() else []

        r = {"hardware": hw, "cpu": cpu, "nearby_phasenav": nearby[:5]}
        try:
            r["mean_phi"] = [round(x, 4) for x in
                             np.fromfile(cards_dir / "mean_phi", dtype=np.float64).tolist()]
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/cielingo_mcp_server.py:418 quiet except scope=_handle_linux_hardware reason=pass")
            raise
            pass
        return r
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/cielingo_mcp_server.py:421 quiet except scope=_handle_linux_hardware reason=return {\"error\": str(e)}")
        raise
        return {"error": str(e)}


# ── Tool list ──────────────────────────────────────────────────────────

TOOLS = [
    _tool(
        "knowledge_query",
        "Search the NOEMA knowledge base (545 documents). Returns top-N matches with similarity scores.",
        {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Search query text"},
                "top_n": {"type": "integer", "description": "Number of results (default 3)", "default": 3},
            },
            "required": ["text"],
        },
        _handle_knowledge_query,
    ),
    _tool(
        "knowledge_coverage",
        "Check if CIELingo has documents covering a given topic. Returns coverage score and match count.",
        {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Topic text to check coverage for"},
            },
            "required": ["text"],
        },
        _handle_knowledge_coverage,
    ),
    _tool(
        "text_analyze",
        "Analyze text via agent backend: themes, affect, anchors, essence, hunch. Uses local AI (port 18520).",
        {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Text to analyze"},
            },
            "required": ["text"],
        },
        _handle_agent_analyze,
    ),
    _tool(
        "agent_health",
        "Check if the agent backend (port 18520) is alive.",
        {"type": "object", "properties": {}},
        _handle_agent_health,
    ),
    _tool(
        "surface_read",
        "Read the current NOEMA surface state: coherence, gravity, flavor, tick.",
        {"type": "object", "properties": {}},
        _handle_surface_read,
    ),
    _tool(
        "daemon_status",
        "List all registered NOEMA daemons from the registry.",
        {"type": "object", "properties": {}},
        _handle_daemon_status,
    ),
    _tool(
        "list_skills",
        "List all available NOEMA skills (~290) with names and descriptions.",
        {"type": "object", "properties": {}},
        _handle_list_skills,
    ),
    _tool(
        "sapiens_session",
        "Initialize or continue a Sapiens interaction session. Builds a packet with surface policy, identity, and turn content.",
        {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "User text for the Sapiens turn"},
                "sapiens_id": {
                    "type": "string",
                    "description": "Identity label (default 'sapiens')",
                    "default": "sapiens",
                },
            },
            "required": ["text"],
        },
        _handle_sapiens_session,
    ),
    _tool(
        "orchestrator_status",
        "Full system status from the Daemon Orchestrator: 16 daemons, registry, New Volume.",
        {"type": "object", "properties": {}},
        _handle_orchestrator_status,
    ),
    _tool(
        "new_volume_status",
        "Check New Volume (1.9TB external drive) availability, free space, and all 8 Tier-3 source directories.",
        {"type": "object", "properties": {}},
        _handle_new_volume,
    ),
    _tool(
        "linux_cards",
        "Full Linux system map as PhaseNav cards: 500+ cards across 9 types (PROC, CPU, DISK, NET_IF, NET_CONN, MODULE, MOUNT, PCI_DEV, SENSOR). NET_CONN = TCP+UDP+TCP6+UDP6 (59 conns). Use type= to filter: type=CPU, type=DISK, type=SENSOR, etc.",
        {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "description": "Card type filter: PROC, CPU, DISK, NET_IF, NET_CONN, MODULE, MOUNT, PCI_DEV, SENSOR, or 'all' (default all)",
                    "default": "all",
                },
                "max_procs": {
                    "type": "integer",
                    "description": "Maximum number of process cards (default 200, max 500)",
                    "default": 200,
                },
            },
        },
        _handle_linux_cards,
    ),
    _tool(
        "linux_hardware",
        "Read cached Linux hardware summary from /dev/shm: CPU cores, disks, net ifaces, PCI devices, PhaseNav nearby, cpu_summary, mean_phi.",
        {"type": "object", "properties": {}},
        _handle_linux_hardware,
    ),
    _tool(
        "binding_status",
        "CIEL ORBITAL BINDING — PHASENAV-HTRI phase space binding monitor. Checks 36D oscillator phases against binding attractor, coherence R, and surface status. Returns passed/errors.",
        {"type": "object", "properties": {}},
        _handle_binding_status,
    ),
]


# ── MCP JSON-RPC over stdio ────────────────────────────────────────


def _send(msg: dict) -> None:
    data = json.dumps(msg, default=str, separators=(",", ":")).encode("utf-8")
    sys.stdout.buffer.write(f"Content-Length: {len(data)}\r\n\r\n".encode("ascii"))
    sys.stdout.buffer.write(data)
    sys.stdout.buffer.flush()


def _recv() -> dict | None:
    headers = bytearray()
    while b"\r\n\r\n" not in headers and b"\n\n" not in headers:
        chunk = sys.stdin.buffer.read(1)
        if not chunk:
            return None
        headers.extend(chunk)

    header_text = headers.decode("ascii", errors="replace")
    length = None
    for line in header_text.replace("\r\n", "\n").split("\n"):
        if line.lower().startswith("content-length:"):
            length = int(line.split(":", 1)[1].strip())
            break
    if length is None:
        raise ValueError("missing Content-Length header")

    data = sys.stdin.buffer.read(length)
    if not data:
        return None
    return json.loads(data)


def main() -> None:
    while True:
        msg = _recv()
        if msg is None:
            break
        _id = msg.get("id")
        method = msg.get("method", "")
        params = msg.get("params", {})

        if method == "tools/call":
            name = params.get("name", "")
            args = params.get("arguments", {})
            tool = next((t for t in TOOLS if t["name"] == name), None)
            if tool is None:
                _send({"jsonrpc": "2.0", "id": _id, "error": {"code": -32601, "message": f"unknown tool: {name}"}})
            else:
                try:
                    result = tool["_handler"](args)
                    _send({"jsonrpc": "2.0", "id": _id, "result": result})
                except Exception as e:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/cielingo_mcp_server.py:605 quiet except scope=main reason=Expr")
                    raise
                    _send({"jsonrpc": "2.0", "id": _id, "error": {"code": -1, "message": str(e)}})
        elif method == "tools/list":
            _send({
                "jsonrpc": "2.0",
                "id": _id,
                "result": {
                    "tools": [{k: v for k, v in t.items() if k != "_handler"} for t in TOOLS]
                },
            })
        elif method == "initialize":
            _send({
                "jsonrpc": "2.0",
                "id": _id,
                "result": {
                    "protocolVersion": params.get("protocolVersion", "2024-11-05"),
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "cielingo", "version": "0.1.0"},
                },
            })
        elif method == "notifications/initialized":
            pass


if __name__ == "__main__":
    main()
