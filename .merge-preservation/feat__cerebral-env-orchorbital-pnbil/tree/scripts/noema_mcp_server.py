#!/usr/bin/env python3
"""NOEMA MCP server — exposes NOEMA surface reads, portal queries, and
daemon control as native MCP tools, so Claude Code (or any MCP client)
never needs to shell out to python3 -c / curl / systemctl for routine
NOEMA operations.

This is the bridge Adrian asked for directly (2026-07-09): "masz mcp bez
skilli?!?! dodaj" — a native tool surface instead of ad-hoc Bash.

MANDATORY, NON-NEGOTIABLE POLICY (Adrian, stated repeatedly, 2026-07-18) --
read this before calling any tool below:

    Every task/plan/lesson from real work in a session MUST be recorded to
    NOEMA's own TaskPlan DB via `noema_taskplan_add`, IN REAL TIME as the
    work happens -- not batched, not "for later", not only at session end.
    Start a task -> record it. Finish or fix something -> record it, right
    then. This is not optional telemetry; it is how NOEMA's own memory
    persists work across sessions instead of that context living only in a
    conversation transcript that gets lost.

    Any agent that loads this MCP server's tools and does NOT follow this
    is violating an explicit, repeated, direct instruction from the
    project owner. Do not treat this as a suggestion.

Registration: add a `.mcp.json` at the Claude Code project root pointing
at this script (see the accompanying .mcp.json written alongside this
file's commit). Requires `pip install mcp` in the venv this runs under.

Usage (manual test, outside Claude Code):
    python3 scripts/noema_mcp_server.py
"""
from __future__ import annotations

import json
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from mcp.server.fastmcp import FastMCP  # noqa: E402
from ciel_geometry import noema_systemd_native as _systemd  # noqa: E402

mcp = FastMCP("noema")

SURFACE_DIR = Path("/dev/shm/ciel_noema")
PORTAL_BASE = "http://127.0.0.1:18888"

# Only these units may be restarted through this tool — an explicit
# allowlist, not "any systemctl command", so this stays a scoped
# operational tool rather than a general shell escape hatch.
_RESTARTABLE_UNITS = {
    "noema-cielingo-sync.service",
    "noema-analog-blend.service",
    "noema-kuramoto.service",
    "noema-headless.service",
    "noema-portal.service",
    "noema-resonance-bridge.service",
    "noema-orchestrator.service",
    "noema-repair-cycle.service",
    "noema-agent-lock.service",
    "noema-linux-sensor.service",
    "noema-web-research.service",
    "noema-orbital.service",
    "noema-self-model.service",
    "noema-trigger.service",
}


@mcp.tool()
def noema_surface_json(name: str) -> dict[str, Any]:
    """Read a JSON file from the NOEMA surface (/dev/shm/ciel_noema/).

    Common names: 'ciel_state.json', 'health', 'hub_snapshot.json'.
    Returns the parsed JSON, or an error dict if the file is missing/invalid.
    """
    path = SURFACE_DIR / name
    if not path.exists():
        return {"error": f"not found: {path}"}
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        return {"error": str(exc)}


@mcp.tool()
def noema_surface_array(name: str) -> dict[str, Any]:
    """Read a binary float64 numpy memmap array from the NOEMA surface.

    Valid names: phi, omega, g, flavor, sensor_raw, tau, R_geom, Z_geom,
    psi_geom, gravity, holonomy. 'g' is returned as a flat list (36x36
    flattened) since it's a coupling matrix; all others are 1D.
    """
    import numpy as np

    path = SURFACE_DIR / name
    if not path.exists():
        return {"error": f"not found: {path}"}
    try:
        arr = np.memmap(str(path), dtype=np.float64, mode="r")
        return {"name": name, "length": int(arr.size), "values": [round(float(x), 6) for x in arr]}
    except Exception as exc:
        return {"error": str(exc)}


@mcp.tool()
def noema_channel_coherence() -> dict[str, Any]:
    """Return per-M-channel (M0-M11) phase coherence, computed the same
    way the portal does: |mean(e^{i*phi})| over each channel's 3 oscillators.
    """
    import numpy as np

    phi_path = SURFACE_DIR / "phi"
    if not phi_path.exists():
        return {"error": "phi surface file not found"}
    phi = np.memmap(str(phi_path), dtype=np.float64, mode="r")
    channels = [
        "M0_Perceptual", "M1_Working", "M2_Episodic", "M3_Semantic",
        "M4_Procedural", "M5_Affective_Ethical", "M6_Identity",
        "M7_Braid_Invariant", "M8_Meta", "M9_Temporal", "M10_Imaginal", "M11_Quantum",
    ]
    result = {}
    for i, name in enumerate(channels):
        block = phi[i * 3:(i + 1) * 3]
        if len(block) == 0:
            continue
        result[name] = round(float(np.abs(np.mean(np.exp(1j * block)))), 6)
    return result


@mcp.tool()
def noema_portal_get(endpoint: str) -> dict[str, Any]:
    """GET a NOEMA portal API endpoint (e.g. '/api/live', '/api/status',
    '/api/ciel/state') and return the parsed JSON response.
    """
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint
    url = PORTAL_BASE + endpoint
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            return json.loads(resp.read())
    except (urllib.error.URLError, json.JSONDecodeError) as exc:
        return {"error": str(exc), "url": url}


@mcp.tool()
def noema_daemon_status(unit: str | None = None) -> dict[str, Any]:
    """Return systemd --user status for one noema-*.service unit, or a
    summary of all noema-*.service units if `unit` is omitted.

    Native D-Bus (org.freedesktop.systemd1), no systemctl subprocess.
    """
    if unit:
        return _systemd.get_unit_state(unit)
    return {"units": _systemd.list_noema_units()}


@mcp.tool()
def noema_daemon_restart(unit: str) -> dict[str, Any]:
    """Restart one NOEMA daemon by systemd unit name, to apply a code fix.

    Restricted to a fixed allowlist of NOEMA units — not a general shell
    escape hatch. Native D-Bus call (org.freedesktop.systemd1.Manager.
    RestartUnit), no systemctl subprocess. Returns the restart result and
    post-restart ActiveState.
    """
    if unit not in _RESTARTABLE_UNITS:
        return {"error": f"'{unit}' is not in the restart allowlist", "allowed": sorted(_RESTARTABLE_UNITS)}
    return _systemd.restart_unit(unit)


@mcp.tool()
def noema_daemon_stop(unit: str) -> dict[str, Any]:
    """Stop (not restart) one NOEMA daemon by systemd unit name — e.g. to
    silence a unit under active investigation, or to shed CPU/thermal load.

    Same allowlist as noema_daemon_restart(). Native D-Bus call, no
    systemctl subprocess. Note: noema-orchestrator.service independently
    monitors and re-launches NOEMA daemons on its own ~30s cycle, so a
    stopped unit may come back on its own unless orchestrator itself is
    also stopped or the unit is disabled — this tool only issues the stop,
    it does not fight the orchestrator.
    """
    if unit not in _RESTARTABLE_UNITS:
        return {"error": f"'{unit}' is not in the allowlist", "allowed": sorted(_RESTARTABLE_UNITS)}
    return _systemd.stop_unit(unit)


@mcp.tool()
def noema_daemon_enable_new(unit: str, unit_file_content: str) -> dict[str, Any]:
    """Write a NEW systemd --user unit file under ~/.config/systemd/user/,
    then daemon-reload + enable it — entirely via native D-Bus (Reload(),
    EnableUnitFiles()), no systemctl subprocess. Does NOT start it (call
    noema_daemon_restart or noema_daemon_status separately once it's in the
    allowlist) — this tool only handles definition + registration.

    unit must end in '.service' and start with 'noema-'. Refuses to
    overwrite an existing unit file (edit it directly and reload instead).
    """
    if not (unit.startswith("noema-") and unit.endswith(".service")):
        return {"error": "unit must look like 'noema-<name>.service'"}
    unit_dir = Path.home() / ".config/systemd/user"
    unit_path = unit_dir / unit
    if unit_path.exists():
        return {"error": f"{unit_path} already exists — edit it directly + reload, this tool is create-only"}
    unit_dir.mkdir(parents=True, exist_ok=True)
    unit_path.write_text(unit_file_content)
    reload_result = _systemd.reload_daemon()
    if not reload_result.get("ok"):
        return {"ok": False, "step": "reload", **reload_result}
    enable_result = _systemd.enable_unit_files([unit])
    return {"ok": enable_result.get("ok", False), "unit_path": str(unit_path),
             "reload": reload_result, "enable": enable_result}


@mcp.tool()
def noema_process_investigate(pid: int) -> dict[str, Any]:
    """Forensic /proc snapshot of one running process, with zero subprocess
    calls (no lsof/netstat/dpkg shelled out to) — pure Python /proc reads.

    Returns: exe path (symlink target), cmdline, cwd, uid/gid/state/rss,
    open file descriptor targets, TCP/UDP connections owned by this PID
    (cross-referenced from /proc/net/{tcp,udp}[6] by socket inode — the
    same data `lsof -p`/`netstat` would show), and direct child PIDs.
    """
    import os
    import socket as _socket
    import struct as _struct
    import time as _time

    base = f"/proc/{pid}"
    if not os.path.exists(base):
        return {"pid": pid, "error": "process not found"}

    def _read(path: str) -> str | None:
        try:
            with open(path, "rb") as f:
                return f.read().decode(errors="replace")
        except (FileNotFoundError, PermissionError):
            return None

    def _net_by_inode() -> dict[str, dict]:
        out: dict[str, dict] = {}
        for proto, path in [
            ("tcp", "/proc/net/tcp"), ("tcp6", "/proc/net/tcp6"),
            ("udp", "/proc/net/udp"), ("udp6", "/proc/net/udp6"),
        ]:
            raw = _read(path)
            if not raw:
                continue
            for line in raw.splitlines()[1:]:
                parts = line.split()
                if len(parts) < 10:
                    continue
                local, remote, state, inode = parts[1], parts[2], parts[3], parts[9]

                def fmt(hex_addr: str) -> str:
                    addr_hex, port_hex = hex_addr.split(":")
                    port = int(port_hex, 16)
                    if len(addr_hex) == 8:
                        addr = _socket.inet_ntoa(_struct.pack("<I", int(addr_hex, 16)))
                    else:
                        addr = "[ipv6]"
                    return f"{addr}:{port}"

                out[inode] = {"proto": proto, "local": fmt(local), "remote": fmt(remote), "state": state}
        return out

    report: dict[str, Any] = {"pid": pid, "collected_at": _time.strftime("%Y-%m-%dT%H:%M:%S")}
    try:
        report["exe"] = os.readlink(f"{base}/exe")
    except (FileNotFoundError, PermissionError) as e:
        report["exe"] = f"<unreadable: {e}>"
    report["cmdline"] = (_read(f"{base}/cmdline") or "").replace("\x00", " ").strip()
    try:
        report["cwd"] = os.readlink(f"{base}/cwd")
    except (FileNotFoundError, PermissionError) as e:
        report["cwd"] = f"<unreadable: {e}>"

    status = _read(f"{base}/status") or ""
    for line in status.splitlines():
        if line.startswith(("Uid:", "Gid:", "PPid:", "State:", "VmRSS:")):
            k, v = line.split(":", 1)
            report[f"status_{k}"] = v.strip()

    fds, net_inodes = [], []
    fd_dir = f"{base}/fd"
    try:
        for fd in os.listdir(fd_dir):
            try:
                target = os.readlink(f"{fd_dir}/{fd}")
            except (FileNotFoundError, PermissionError):
                continue
            fds.append(target)
            if target.startswith("socket:["):
                net_inodes.append(target[8:-1])
    except (FileNotFoundError, PermissionError) as e:
        fds = [f"<unreadable: {e}>"]
    report["open_fds_count"] = len(fds)
    report["open_fds_sample"] = fds[:100]
    net_map = _net_by_inode() if net_inodes else {}
    report["network_connections"] = [net_map[i] for i in net_inodes if i in net_map]

    children = []
    for p in os.listdir("/proc"):
        if not p.isdigit():
            continue
        stat_line = _read(f"/proc/{p}/stat")
        if stat_line and ") " in stat_line:
            ppid_field = stat_line.split(") ", 1)[1].split()[1]
            if ppid_field == str(pid):
                children.append(p)
    report["child_pids"] = children
    return report


@mcp.tool()
def noema_process_signal(pid: int, expected_name_substring: str, sig: str = "TERM") -> dict[str, Any]:
    """Send a signal (default SIGTERM) to one process, but ONLY if its live
    /proc/<pid>/cmdline still contains expected_name_substring — refuses
    otherwise, so a stale/reused PID can't silently signal the wrong
    process. No subprocess/shell involved (os.kill directly).

    Will return a PermissionError-shaped result (not raise) if the target
    process is owned by a different user (e.g. root) — this tool runs with
    whatever privilege the MCP server process itself has, it does not
    escalate.
    """
    import os
    import signal as _signal
    import time as _time

    sig_map = {"TERM": _signal.SIGTERM, "KILL": _signal.SIGKILL, "HUP": _signal.SIGHUP, "INT": _signal.SIGINT}
    if sig not in sig_map:
        return {"error": f"unsupported signal '{sig}', use one of {sorted(sig_map)}"}

    try:
        with open(f"/proc/{pid}/cmdline", "rb") as f:
            cmdline = f.read().decode(errors="replace")
    except FileNotFoundError:
        return {"ok": True, "note": f"pid {pid} not found (already gone)"}

    if expected_name_substring not in cmdline:
        return {"ok": False, "error": f"refused: cmdline {cmdline!r} does not contain {expected_name_substring!r}"}

    try:
        os.kill(pid, sig_map[sig])
    except PermissionError:
        return {"ok": False, "error": f"PermissionError sending {sig} to pid {pid} (owned by another user, e.g. root)"}
    except ProcessLookupError:
        return {"ok": True, "note": f"pid {pid} already gone"}

    for _ in range(20):
        if not os.path.exists(f"/proc/{pid}"):
            return {"ok": True, "pid": pid, "stopped": True}
        _time.sleep(0.1)
    return {"ok": True, "pid": pid, "stopped": False, "note": "still alive 2s after signal"}


@mcp.tool()
def noema_taskplan_add(
    kind: str,
    title: str,
    description: str = "",
    category: str = "",
    source: str = "claude-code",
) -> dict[str, Any]:
    """MANDATORY, real-time, non-optional (Adrian, stated repeatedly): call
    this the moment you start, finish, or fix something -- not batched at
    the end of a session. This is how NOEMA's own memory persists work
    across sessions; skipping it or deferring it "for later" is a direct
    violation of an explicit standing instruction from the project owner.

    Write one row to NOEMA's TaskPlan DB (tasks/plans/lessons) — the
    third of three writers added 2026-07-10 after an audit found the DB had
    exactly one row in its entire history: self-model.py now writes
    'lessons' for anomalies, trigger_daemon.py now writes 'decisions' for
    novel high-coherence situations, and this tool is the third writer
    Adrian asked for ('wszystkie') — Claude Code itself, recording real
    task/plan/lesson entries for work actually done in a session, instead
    of that context living only in conversation transcripts.

    kind: one of 'task', 'plan', 'lesson'. Each maps to TaskPlanDB's
    matching add_*() method with sane defaults for the fields this tool
    doesn't expose (priority='medium' for tasks, no steps for plans,
    lesson_date=today for lessons).
    """
    import datetime as _dt

    if kind not in ("task", "plan", "lesson"):
        return {"error": "kind must be one of: task, plan, lesson"}
    try:
        from ciel_geometry.taskplan_db import TaskPlanDB
        db = TaskPlanDB()
        if kind == "task":
            result = db.add_task(title=title, description=description, category=category or "claude-code")
        elif kind == "plan":
            result = db.add_plan(title=title, description=description, steps=[])
        else:
            today = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d")
            result = db.add_lesson(
                lp=f"CC-{title[:40].replace(' ', '_')}-{today}",
                title=title, description=description,
                category=category or "claude-code-session",
                lesson_date=today, source=source,
            )
        return {"ok": True, "kind": kind, "result": result}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


@mcp.tool()
def noema_run_script(script_path: str, args: list[str] | None = None, timeout: int = 60) -> dict[str, Any]:
    """Run a NOEMA script (scripts/*.py or src/*.py) with PYTHONPATH set up
    correctly, and return stdout/stderr/returncode.

    `script_path` must be relative to the NOEMA repo root and end in .py,
    inside scripts/ or src/ — this is not a general command executor.
    """
    rel = Path(script_path)
    if rel.is_absolute() or ".." in rel.parts:
        return {"error": "script_path must be a relative path with no '..'"}
    if not (str(rel).startswith("scripts/") or str(rel).startswith("src/")):
        return {"error": "script_path must be under scripts/ or src/"}
    if rel.suffix != ".py":
        return {"error": "script_path must end in .py"}
    full = ROOT / rel
    if not full.exists():
        return {"error": f"not found: {full}"}

    cmd = [sys.executable, str(full)] + (args or [])
    env = {"PYTHONPATH": str(ROOT / "src")}
    import os
    env = {**os.environ, **env}
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=str(ROOT), env=env)
        return {"returncode": proc.returncode, "stdout": proc.stdout[-8000:], "stderr": proc.stderr[-4000:]}
    except subprocess.TimeoutExpired:
        return {"error": f"timed out after {timeout}s"}


@mcp.tool()
def noema_skill_lookup(query: str) -> dict[str, Any]:
    """Search SKILLS.md for skill entries whose name or description
    contains `query` (case-insensitive substring match). Returns matching
    rows (SK number, name, source file) so a skill's real script path can
    be found before calling noema_run_script on it.
    """
    skills_path = ROOT / "SKILLS.md"
    if not skills_path.exists():
        return {"error": "SKILLS.md not found"}
    q = query.lower()
    matches = []
    for line in skills_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("| SK-") and q in line.lower():
            matches.append(line.strip())
        if len(matches) >= 25:
            break
    return {"query": query, "matches": matches}


if __name__ == "__main__":
    mcp.run()
