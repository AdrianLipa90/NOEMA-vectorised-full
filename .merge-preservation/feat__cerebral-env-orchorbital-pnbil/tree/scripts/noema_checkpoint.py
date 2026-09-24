#!/usr/bin/env python3
"""NOEMA Checkpoint System — interaktywna checklista przed odpowiedzią.

Usage:
    python3 scripts/noema_checkpoint.py          # pełny checkpoint
    python3 scripts/noema_checkpoint.py --quick   # szybki (tylko krytyczne)
    python3 scripts/noema_checkpoint.py --json    # JSON output dla agenta
"""

from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import json
import math
import os
import struct
import sys
from pathlib import Path

import numpy as np

SURFACE = Path("/dev/shm/ciel_noema")
BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "src"))
from ciel_geometry.noema_host_ledger import NoemaHostLedger

HOST_LEDGER = NoemaHostLedger()
PID_LOCK = Path(os.environ.get("XDG_RUNTIME_DIR", "/run/user/1000")) / "noema" / "noema_trigger_daemon.pid"
AGENTS = BASE / "AGENTS.md"
LESSONS = BASE / "LEARNED_LESSONS.md"
FUNCTIONS = BASE / "FUNCTIONS.md"
SKILLS = BASE / "SKILLS.md"
TASK_QUEUE = BASE / "NOEMA" / "task_queue.noema.json"


# ── Check helpers ─────────────────────────────────────────────────────

def _ok(msg: str) -> str:
    return f"  ✅ {msg}"


def _warn(msg: str) -> str:
    return f"  ⚠️  {msg}"


def _fail(msg: str) -> str:
    return f"  ❌ {msg}"


def _check_surface() -> list[str]:
    """Sprawdź stan powierzchni — daemony, attractor, coherence."""
    results = []
    try:
        sys.path.insert(0, str(BASE / "src"))
        from ciel_geometry.agent_attractor import agent_attractor_state
        from ciel_geometry.noema_surface_mmap import open_surface, read_surface_state

        surface = open_surface(SURFACE, mode="r")
        state = read_surface_state(surface)
        attractor_state = agent_attractor_state(np.asarray(surface["phi"], dtype=np.float64))
        alive = len(list((SURFACE / "registry").glob("*.json")))
        coh = float(state.get("coherence_index", state.get("R_global", 0.0)))
        attractor = "locked" if attractor_state.get("locked") else "unlocked"
        aerr = float(attractor_state.get("max_delta", 1.0))
        tick = state.get("noema_tick", 0)

        if alive >= 2:
            results.append(_ok(f"Surface owners registered: {alive}"))
        elif alive == 1:
            results.append(_warn("Surface owners registered: 1"))
        else:
            results.append(_fail("Surface owners registered: 0"))

        # 36 osc z τ dynamicznym i realnym sensorem: R∈[0.3, 0.6] normalne
        if coh >= 0.7:
            results.append(_ok(f"Kuramoto R: {coh:.3f}"))
        elif coh >= 0.4:
            results.append(_warn(f"Kuramoto R: {coh:.3f} — normalna dla 36 osc z sensorem"))
        else:
            results.append(_fail(f"Kuramoto R: {coh:.3f} — rozsynchronizowanie!"))

        if attractor == "locked" and aerr < 0.15:
            results.append(_ok(f"Attractor: {attractor} (err={aerr:.4f})"))
        elif attractor == "locked":
            results.append(_warn(f"Attractor: {attractor} (err={aerr:.4f})"))
        else:
            results.append(_fail(f"Attractor: {attractor} (err={aerr:.4f})"))

        results.append(_ok(f"Tick: {tick}"))

        # Phi — AGENT M1
        phi_data = (SURFACE / "phi").read_bytes()
        phi = list(struct.unpack("36d", phi_data)) if len(phi_data) >= 288 else []
        if len(phi) >= 6:
            agent_phi = [round(p, 4) for p in phi[3:6]]
            target = 0.7854  # π/4
            devs = [abs(p - target) for p in agent_phi]
            max_dev = max(devs)
            if max_dev < 0.15:
                results.append(_ok(f"AGENT: {agent_phi} dev={max_dev:.4f} (near π/4)"))
            elif max_dev < 0.3:
                results.append(_warn(f"AGENT: {agent_phi} dev={max_dev:.4f}"))
            else:
                results.append(_fail(f"AGENT: {agent_phi} dev={max_dev:.4f} — dryf!"))

    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_checkpoint.py:91 quiet except scope=_check_surface reason=Expr")
        results.append(_fail(f"Surface read error: {e}"))

    return results


def _check_files() -> list[str]:
    """Sprawdź czy kluczowe pliki istnieją."""
    results = []
    checks = [
        ("AGENTS.md", AGENTS),
        ("LEARNED_LESSONS.md", LESSONS),
        ("FUNCTIONS.md", FUNCTIONS),
        ("SKILLS.md", SKILLS),
        ("task_queue.noema.json", TASK_QUEUE),
    ]
    for name, path in checks:
        if path.exists():
            results.append(_ok(f"{name} exists"))
        else:
            results.append(_fail(f"{name} NOT FOUND at {path}"))
    return results


def _check_task_queue() -> list[str]:
    """Sprawdź HIGH priority taski."""
    results = []
    try:
        data = json.loads(TASK_QUEUE.read_text())
        queue = data.get("queue", [])
        high = [t for t in queue if t.get("status") == "pending"
                and t.get("priority", "").startswith("HIGH")]
        if high:
            results.append(_warn(f"HIGH pending: {len(high)} tasks:"))
            for t in high:
                task_text = t.get("task", "?")[:80]
                results.append(f"       ⚡ {task_text}")
        else:
            results.append(_ok("No HIGH pending tasks"))
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_checkpoint.py:130 quiet except scope=_check_task_queue reason=Expr")
        raise
        results.append(_fail("Cannot read task queue"))
    return results


def _check_agent_hint() -> list[str]:
    """Sprawdź agent_hint — next step."""
    results = []
    try:
        hint = json.loads((SURFACE / "agent_hint").read_text())
        next_step = hint.get("next", "")
        action = hint.get("action", "")
        if next_step:
            results.append(_warn(f"agent_hint next: {next_step}"))
            if action:
                results.append(f"       action: {action}")
        else:
            results.append(_ok("agent_hint: no pending next step"))
    except FileNotFoundError:
        results.append(_ok("agent_hint: no data (fresh start)"))
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.debug("scripts/noema_checkpoint.py:148 quiet except scope=_check_agent_hint reason=Expr")
        results.append(_fail("agent_hint read error"))
    return results


def _check_state_files() -> list[str]:
    """Sprawdź czy jest stan sesji do kontynuacji."""
    results = []
    state = HOST_LEDGER.get_state("trigger.last_triggered", {})
    if isinstance(state, dict) and state:
        results.append(_ok(f"Trigger state (host ledger): {len(state)} entries"))
    else:
        results.append(_ok("Trigger state (host ledger): empty"))

    # PID lock — czy trigger daemon żyje
    if PID_LOCK.exists():
        try:
            pid = int(PID_LOCK.read_text().strip())
            results.append(_ok(f"Trigger daemon PID: {pid}"))
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_checkpoint.py:170 quiet except scope=_check_state_files reason=pass")
            raise
            pass

    return results


def _check_lessons_reminder() -> list[str]:
    """Przypomnienie o LEARNED_LESSONS."""
    return [
        "",
        "  📋 LEARNED_LESSONS.md — pamiętaj:",
        "     - L-005: jak nie wiesz — pytaj",
        "     - L-015: czytaj LEARNED_LESSONS przed każdą akcją",
        "     - L-025: PhaseNav decision = ROZKAZ do zmiany fizycznej",
        "     - L-029: karty NOEMA wymagają wszystkich pól",
    ]


# ── Główny checkpoint ─────────────────────────────────────────────────

def run_checkpoint(quick: bool = False) -> dict:
    """Wykonaj pełny checkpoint, zwróć dict z wynikami i statusem."""
    sections = {}

    sections["surface"] = _check_surface()
    sections["files"] = _check_files()
    sections["task_queue"] = _check_task_queue()
    sections["agent_hint"] = _check_agent_hint()
    sections["state"] = _check_state_files()
    if not quick:
        sections["lessons"] = _check_lessons_reminder()

    # Ocena ogólna
    all_lines = []
    fails = 0
    warns = 0
    for section_name, lines in sections.items():
        if not lines:
            continue
        all_lines.append(f"\n── {section_name.upper()} ──")
        for line in lines:
            all_lines.append(line)
            if line.startswith("  ❌"):
                fails += 1
            elif line.startswith("  ⚠️"):
                warns += 1

    status = "PASS"
    if fails > 0:
        status = "FAIL"
    elif warns > 0:
        status = "WARN"

    return {
        "status": status,
        "fails": fails,
        "warns": warns,
        "sections": sections,
        "summary": "\n".join(all_lines),
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="NOEMA Checkpoint System")
    parser.add_argument("--quick", action="store_true", help="Tylko krytyczne")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    result = run_checkpoint(quick=args.quick)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        ticks = "✅" if result["status"] == "PASS" else "⚠️" if result["status"] == "WARN" else "❌"
        print(f"\n{'='*50}")
        print(f"  NOEMA CHECKPOINT  —  {result['status']}  {ticks}")
        print(f"  Fails: {result['fails']}  Warnings: {result['warns']}")
        print(f"{'='*50}")
        print(result["summary"])
        print(f"\n{'='*50}")

        # Kod wyjścia dla skryptów
        if result["fails"] > 0:
            sys.exit(2)
        elif result["warns"] > 0:
            sys.exit(1)
        sys.exit(0)
