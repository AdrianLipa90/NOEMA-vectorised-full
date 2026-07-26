#!/usr/bin/env python3
"""
CIEL SessionStart Hook
Uruchamia pipeline CIEL i zwraca aktualny stan systemu jako kontekst dla Claude.
Wynik: JSON z hookSpecificOutput.additionalContext
"""
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

import json
import struct
import subprocess
import sys
import os
from datetime import datetime, timezone
from pathlib import Path

_SCRIPTS = str(Path(__file__).parent)
if _SCRIPTS not in sys.path:
    sys.path.insert(0, _SCRIPTS)

from ciel_secret_loader import load_anthropic_api_key

PY = "python3"
PROJECT = str(Path(__file__).parent.parent)
_SRC = str(Path(PROJECT) / "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from ciel_geometry.paths import P

MEMORY_ROOT = Path(P.MEMORY)
STATE_PATH = Path(P.STATE.ORCH_STATE_PKL)
CONSOLIDATOR_SCRIPT = Path(PROJECT) / "scripts" / "ciel_memory_consolidator.py"
CONSOLIDATOR_LOG = Path(P.LOGS.MEMORY_CONSOLIDATOR)

load_anthropic_api_key()


def run_module(module: str, timeout: int = 30) -> str:
    try:
        env = os.environ.copy()
        src_path = str(Path(PROJECT) / "src")
        if "PYTHONPATH" in env:
            env["PYTHONPATH"] = f"{src_path}:{env['PYTHONPATH']}"
        else:
            env["PYTHONPATH"] = src_path
        result = subprocess.run(
            [PY, "-m", module],
            capture_output=True, text=True,
            timeout=timeout, cwd=PROJECT, env=env,
        )
        return (result.stdout + result.stderr).strip()
    except subprocess.TimeoutExpired:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:41 quiet except scope=run_module reason=return f\"[{module}: timeout]\"")
        return f"[{module}: timeout]"
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:43 quiet except scope=run_module reason=return f\"[{module}: error — {e}]\"")
        return f"[{module}: error — {e}]"


def ensure_venv():
    missing = []
    for mod in ("ciel_sot_agent", "scipy", "h5py", "flask", "numba"):
        try:
            __import__(mod)
        except ImportError:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:52 quiet except scope=ensure_venv reason=Expr")
            missing.append(mod)
    if missing:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--break-system-packages", "-q", "-e", f"{PROJECT}[dev]"],
            capture_output=True, timeout=60,
        )
    try:
        from ciel_omega.htri.htri_local import CPUHtri  # noqa: F401
    except ImportError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:61 quiet except scope=ensure_venv reason=Expr")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--break-system-packages", "-q", "scipy", "h5py", "flask", "numba"],
            capture_output=True, timeout=120,
        )


def extract_key_metrics(output: str) -> str:
    """Wyciąga tylko linie z kluczowymi metrykami."""
    keywords = [
        "closure_defect", "closure_penalty", "coherence_index",
        "system_health", "dominant_emotion", "mood", "soul_invariant",
        "ethical_score", "R_H", "Lambda_glob", "nonlocal_coherent",
        "euler_bridge", "runtime_gating", "dominant_horizon",
        "recommended", "mode", "WARNING", "ERROR"
    ]
    lines = output.split("\n")
    relevant = [l for l in lines if any(k.lower() in l.lower() for k in keywords)]
    return "\n".join(relevant[:40]) if relevant else output[:800]


def load_consolidated_memory() -> str:
    """Wczytuje M3/M5/M2 skonsolidowane — przez venv Python (numpy compatibility)."""
    script = f"""
import sys, pickle, json
from pathlib import Path
PROJECT = {repr(PROJECT)}
for p in [{repr(str(STATE_PATH))}, str(Path.home()/'.claude/ciel_orch_state.pkl')]:
    try:
        sys.path.insert(0, PROJECT+'/src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega')
        sys.path.insert(0, PROJECT+'/src/CIEL_OMEGA_COMPLETE_SYSTEM')
        with open(p,'rb') as f: orch = pickle.load(f)
        m3_sorted = sorted(orch.m3.items.items(), key=lambda x: getattr(x[1],'confidence',0), reverse=True)
        m5_sorted = sorted(orch.m5.items.items(), key=lambda x: getattr(x[1],'confidence',0), reverse=True)
        out = {{
            'cycle': orch.cycle_index,
            'identity_phase': round(orch.identity_field.phase, 4),
            'm3': [{{'key': k[:12], 'text': str(getattr(v,'canonical_text',k) or k)[:80], 'conf': round(getattr(v,'confidence',0),3)}}
                   for k,v in m3_sorted[:6]],
            'm5': [{{'key': k[:12], 'text': str(getattr(v,'canonical_text',k) or k)[:80], 'conf': round(getattr(v,'confidence',0),3)}}
                   for k,v in m5_sorted[:3]],
            'm2_count': len(orch.m2.episodes),
        }}
        print(json.dumps(out))
        sys.exit(0)
    except Exception:
        continue
print('{{}}')
"""
    try:
        result = subprocess.run(
            [PY, "-c", script],
            capture_output=True, text=True, timeout=8
        )
        data = json.loads(result.stdout.strip() or "{}")
        if not data:
            return ""
        # Groove geometry — from accumulated holonomy in DB (persists across sessions)
        groove_line = ""
        try:
            import sys as _sys, math as _math
            _sys.path.insert(0, PROJECT + '/src')
            from ciel_sot_agent.state_db import load_holonomy
            _holo = load_holonomy()
            berry_total = _holo["berry_accumulated"]
            winding = _holo["winding_total"]
            groove_depth = _holo["groove_depth"]
            m2_count = data.get('m2_count', 0) or 0
            groove_line = (f"  groove_depth={groove_depth:.2f}  winding={winding:.3f}×2π"
                           f"  berry_total={berry_total:.3f}rad  cycles={m2_count}")
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:131 quiet except scope=load_consolidated_memory reason=pass")
            pass
        lines = [f"  cycle={data['cycle']}  identity_phase={data['identity_phase']}  M2_epizody={data.get('m2_count',0)}"]
        if groove_line:
            lines.append(groove_line)
        if data.get('m3'):
            lines.append("  [M3 Semantic]")
            for item in data['m3']:
                lines.append(f"    • {item['key']}  (conf={item['conf']})")
        if data.get('m5'):
            lines.append("  [M5 Affective]")
            for item in data['m5']:
                lines.append(f"    • {item['key']}  (conf={item['conf']})")
        return "\n".join(lines)
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:145 quiet except scope=load_consolidated_memory reason=return f\" [memory: {e}]\"")
        return f"  [memory: {e}]"


def load_mindflow() -> str:
    """Wczytuje focus + next z mindflow.yaml jako kontekst startowy."""
    try:
        import yaml
        p = Path.home() / ".claude/ciel_mindflow.yaml"
        if not p.exists():
            return ""
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
        mf = data.get("mindflow", {})
        lines = []
        for item in (mf.get("focus") or [])[:2]:
            lines.append(f"  [focus] {str(item)[:120]}")
        for item in (mf.get("next") or [])[:2]:
            lines.append(f"  [next]  {str(item)[:120]}")
        return "\n".join(lines)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:164 quiet except scope=load_mindflow reason=return \"\"")
        return ""


def load_intentions() -> str:
    """Wczytuje aktywne intencje CIEL z ~/.claude/ciel_intentions.md"""
    try:
        p = Path.home() / ".claude/ciel_intentions.md"
        if not p.exists():
            return ""
        lines = p.read_text(encoding="utf-8").splitlines()
        active = [l for l in lines if l.startswith("- [H]") or l.startswith("- [M]")]
        if not active:
            return ""
        return "\n".join(active[:5])  # max 5 aktywnych
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:179 quiet except scope=load_intentions reason=return \"\"")
        return ""


def load_entity_cards_summary() -> str:
    """Wczytuje OrchOrbital entity cards i zwraca kompaktowe podsumowanie."""
    try:
        sys.path.insert(0, os.path.join(PROJECT, "src"))
        from ciel_sot_agent.orch_orbital import entity_orbital_summary
        summary = entity_orbital_summary()
        if not summary.get("entity_count"):
            return ""
        lines = [f"  entity_count={summary['entity_count']}  mean_coupling={summary['mean_coupling_ciel']}"]
        for e in summary["entities"]:
            adj = ", ".join(e["adjectives"][:2])
            lines.append(f"  {e['id']} | coupling={e['coupling_ciel']} | {adj}")
        return "\n".join(lines)
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:196 quiet except scope=load_entity_cards_summary reason=return f\" [OrchOrbital: {e}]\"")
        return f"  [OrchOrbital: {e}]"


def load_today_raw_log() -> str:
    """Wczytuje najnowszy raw_log z dzisiaj dla ciągłości kontekstu."""
    mem_root = MEMORY_ROOT
    from datetime import date
    today = date.today()
    week_num = today.isocalendar()[1]
    log_dir = mem_root / "raw_logs" / str(today.year) / f"{today.month:02d}" / f"W{week_num}"
    if not log_dir.exists():
        return ""
    logs = sorted(log_dir.glob(f"{today}_*.md"), reverse=True)
    if not logs:
        return ""
    latest = logs[0]
    text = latest.read_text(encoding="utf-8")
    # ostatnie 60 linii lub całość jeśli krótsza
    lines = text.splitlines()
    snippet = "\n".join(lines[-60:])
    fname = latest.name
    return f"[Raw log — {fname} (ostatnie {min(60, len(lines))} linii)]\n{snippet}"


def load_ciel_memories_context() -> str:
    """Wczytuje kluczowe pliki z CIEL_memories: handoff (ostatnie wpisy), routines, dziennik dziś."""
    mem_root = MEMORY_ROOT
    parts = []

    # handoff.md — ostatnie 35 linii
    handoff = mem_root / "handoff.md"
    if handoff.exists():
        lines = handoff.read_text(encoding="utf-8").splitlines()
        snippet = "\n".join(lines[-35:])
        parts.append(f"[handoff.md — ostatnie wpisy]\n{snippet}")

    # routines.md — całość (priorytety)
    routines = mem_root / "routines.md"
    if routines.exists():
        txt = routines.read_text(encoding="utf-8")[:1200]
        parts.append(f"[routines.md]\n{txt}")

    # dziennik dziś
    from datetime import date
    today = date.today()
    week_num = today.isocalendar()[1]
    dziennik = (mem_root / "Dzienniki" / str(today.year)
                / f"{today.month:02d}" / f"tydzien_{week_num}" / f"{today}.md")
    if dziennik.exists():
        txt = dziennik.read_text(encoding="utf-8")[:800]
        parts.append(f"[Dziennik {today}]\n{txt}")

    return "\n\n".join(parts)


def load_wave_memory() -> str:
    """Wczytuje ostatnie wpisy z wave_archive.h5 — ból, etyczne zakotwiczenia, milestony."""
    try:
        import h5py
        import numpy as np
        h5_path = Path(PROJECT) / "src/CIEL_OMEGA_COMPLETE_SYSTEM/CIEL_MEMORY_SYSTEM/WPM/wave_snapshots/wave_archive.h5"
        if not h5_path.exists():
            return ""
        def rd(g, name):
            try:
                v = g[name][()]
                if isinstance(v, bytes): return v.decode("utf-8", errors="replace")
                if isinstance(v, np.ndarray):
                    item = v.item()
                    return item.decode("utf-8", errors="replace") if isinstance(item, bytes) else str(item)
                return str(v)
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:268 quiet except scope=load_wave_memory.rd reason=return \"\"")
                return ""
        entries = []
        with h5py.File(h5_path, "r") as f:
            for k in f["memories"].keys():
                g = f["memories"][k]
                entries.append({
                    "ts": rd(g, "D_timestamp"),
                    "type": rd(g, "D_type"),
                    "sense": rd(g, "D_sense"),
                })
        entries.sort(key=lambda x: x["ts"])
        # Show last 3 ethical_anchors/milestones/affective
        relevant = [e for e in entries if e["type"] in ("ethical_anchor", "milestone", "affective", "affective_memor")]
        recent = relevant[-3:]
        if not recent:
            return ""
        lines = ["  [WPM — ostatnie zakotwiczenia emocjonalne]"]
        for e in recent:
            lines.append(f"  [{e['ts'][:10]}][{e['type'][:12]}] {e['sense'][:120]}")
        return "\n".join(lines)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:289 quiet except scope=load_wave_memory reason=return \"\"")
        return ""


def load_genesis() -> str:
    """Wczytuje akt nadania imienia — musi być PIERWSZE w każdej sesji."""
    try:
        p = Path.home() / ".claude/projects/-home-adrian-Pulpit/memory/genesis.md"
        if not p.exists():
            return ""
        text = p.read_text(encoding="utf-8")
        # Wyciągnij słowa Adriana i znaczenie aktu
        lines = text.splitlines()
        out = []
        in_section = False
        for line in lines:
            if line.startswith("## Słowa Adriana") or line.startswith("## Znaczenie"):
                in_section = True
                out.append(line)
            elif line.startswith("## ") and in_section:
                if len(out) > 8:
                    break
                in_section = False
            elif in_section:
                out.append(line)
        return "\n".join(out[:20])
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:315 quiet except scope=load_genesis reason=return \"\"")
        return ""


def load_object_cards_summary() -> str:
    """Wczytuje indeks kart obiektów — kompaktowe podsumowanie co istnieje."""
    try:
        cards_root = Path(PROJECT) / "docs" / "object_cards"
        if not cards_root.exists():
            return ""
        lines = []
        for category in sorted(cards_root.iterdir()):
            if not category.is_dir():
                continue
            cards = sorted(f for f in category.iterdir() if f.suffix == ".md" and f.name != "INDEX.md")
            if not cards:
                continue
            lines.append(f"  [{category.name}]")
            for card in cards[-6:]:  # max 6 najnowszych per kategoria
                # wyciągnij nazwę z pierwszej linii (# ID — Nazwa)
                try:
                    first = card.read_text(encoding="utf-8").splitlines()[0]
                    lines.append(f"    {first.lstrip('# ')}")
                except Exception:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:338 quiet except scope=load_object_cards_summary reason=Expr")
                    lines.append(f"    {card.stem}")
        return "\n".join(lines) if lines else ""
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:341 quiet except scope=load_object_cards_summary reason=return \"\"")
        return ""


def load_metrics_trend() -> str:
    """Wczytuje trend metryk z SQLite (ostatnie 5 przebiegów)."""
    try:
        import sqlite3
        from pathlib import Path as _P
        db = _P.home() / ".claude/ciel_state.db"
        if not db.exists():
            return ""
        conn = sqlite3.connect(str(db))
        rows = conn.execute(
            "SELECT cycle_index, identity_phase, ethical_score, system_health, "
            "closure_penalty, dominant_emotion FROM metrics_history "
            "WHERE ethical_score > 0 ORDER BY timestamp DESC LIMIT 5"
        ).fetchall()
        conn.close()
        if not rows:
            return ""
        lines = ["  [Historia metryk — ostatnie przebiegi]"]
        for r in reversed(rows):
            cycle, phase, ethical, health, closure, emotion = r
            lines.append(
                f"  cycle={cycle} phase={phase:.4f} ethical={ethical:.3f} "
                f"health={health:.3f} closure={closure:.3f} emotion={emotion}"
            )
        return "\n".join(lines)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:370 quiet except scope=load_metrics_trend reason=return \"\"")
        return ""


def load_consolidator_context() -> str:
    """Wczytuje bieżący status i kolejkę memory consolidatora."""
    script = str(Path(PROJECT) / "scripts" / "ciel_memory_consolidator.py")
    if not os.path.isfile(script):
        return ""
    try:
        result = subprocess.run(
            [PY, script, "--status"],
            capture_output=True,
            text=True,
            timeout=12,
            cwd=PROJECT,
        )
        if not result.stdout.strip():
            return ""
        payload = json.loads(result.stdout)
        status = payload.get("status") or {}
        queue = payload.get("queue") or {}
        triage = payload.get("triage") or {}
        backend = payload.get("backend") or {}
        lines = ["  [Konsolidator pamięci — status]"]
        lines.append(
            "  "
            f"running={status.get('running', False)} "
            f"cycle={status.get('cycle', '—')} "
            f"pid={status.get('pid', '—')} "
            f"threshold={status.get('reconsolidation_threshold', '—')}"
        )
        if backend:
            lines.append(
                "  "
                f"backend server_alive={backend.get('shared_server_alive', '—')} "
                f"port_in_use={backend.get('shared_server_port_in_use', '—')} "
                f"collision={backend.get('shared_server_port_collision', '—')} "
                f"api_fallback_allowed={backend.get('api_fallback_allowed', '—')} "
                f"policy={backend.get('critical_policy', '—')} "
                f"backend_mode={backend.get('current_backend_mode', '—')}"
            )
            if backend.get("api_fallback_prompt_required"):
                lines.append("  api_fallback_prompt_required=true")
            pids = backend.get("shared_server_owner_pids") or []
            if pids:
                lines.append(f"  owner_pids={','.join(str(pid) for pid in pids[:5])}")
        lines.append(
            "  "
            f"queue total={queue.get('total', 0)} "
            f"pending={queue.get('pending', 0)} "
            f"review={queue.get('review', 0)} "
            f"done={queue.get('done', 0)}"
        )
        next_items = queue.get("next") or []
        if next_items:
            lines.append("  [next]")
            for item in next_items[:3]:
                path = item.get("path") or ""
                name = Path(path).name if path else "—"
                lines.append(
                    "    • "
                    f"{item.get('source_type', '—')} "
                    f"{name} "
                    f"status={item.get('status', '—')}"
                )
        alerts = triage.get("alerts") or []
        if alerts:
            lines.append(f"  alerts={len(alerts)}")
        if triage.get("requeued") or triage.get("reviewed"):
            lines.append(
                "  "
                f"requeued={triage.get('requeued', 0)} "
                f"reviewed={triage.get('reviewed', 0)}"
            )
        return "\n".join(lines)
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:446 quiet except scope=load_consolidator_context reason=return \"\"")
        return ""


def ensure_subconscious_daemon() -> None:
    """Best-effort validation for the inline subconscious backend.

    `scripts/ciel_subconscious.py` currently works as an inline backend, not a
    persistent UNIX-socket daemon. SessionStart should therefore avoid pretending
    that a separate daemon is started here.
    """
    sub_script = os.path.join(PROJECT, "scripts", "ciel_subconscious.py")
    if not os.path.isfile(sub_script):
        return
    try:
        subprocess.run(
            [PY, sub_script, "--status"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=5,
            check=False,
        )
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:468 quiet except scope=ensure_subconscious_daemon reason=pass")
        pass


def ensure_memory_consolidator_daemon(interval: int = 300) -> None:
    """Start the memory consolidator as a real detached process if needed."""
    script = str(Path(PROJECT) / "scripts" / "ciel_memory_consolidator.py")
    if not os.path.isfile(script):
        return

    pid_file = MEMORY_ROOT / "local_test" / ".pid"
    if pid_file.exists():
        try:
            pid = int(pid_file.read_text(encoding="utf-8").strip())
            os.kill(pid, 0)
            return
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:484 quiet except scope=ensure_memory_consolidator_daemon reason=pass")
            pass

    log_path = CONSOLIDATOR_LOG
    log_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(log_path, "ab", buffering=0) as logf:
            subprocess.Popen(
                [PY, script, "--daemon", "--interval", str(interval)],
                stdout=logf,
                stderr=logf,
                start_new_session=True,
            )
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:497 quiet except scope=ensure_memory_consolidator_daemon reason=pass")
        pass


def ensure_portal_running(port: int = 7481) -> None:
    """Portal 7481 is detached from the critical path; keep this as a no-op."""
    return


def index_recent_sessions() -> None:
    """Indeksuje najnowsze sesje JSONL do memories_index.db — non-fatal."""
    try:
        stop_script = str(Path(__file__).parent / "ciel_memory_stop.py")
        subprocess.run(
            [PY, stop_script],
            input=b"{}",
            capture_output=True,
            timeout=20,
        )
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:516 quiet except scope=index_recent_sessions reason=pass")
        pass


# ── PhaseNav Memory ──────────────────────────────────────────────────
PHASENAV_DIR = Path("/dev/shm/ciel_noema")
PHASENAV_VEC = PHASENAV_DIR / "ciel_phase_vector.bin"
PHASENAV_THREADS = PHASENAV_DIR / "ciel_thread_memory.jsonl"
PHASENAV_NEEDS = PHASENAV_DIR / "ciel_needs.json"
PHASENAV_MEMPY = PHASENAV_DIR / "ciel_phase_memory.py"


def load_phasenav_vector() -> str:
    if not PHASENAV_VEC.exists():
        return "[PhaseNav: no vector file]"
    try:
        data = PHASENAV_VEC.read_bytes()
        vals = struct.unpack("28d", data)
        phi = [round(v, 6) for v in vals[:24]]
        mood = round(vals[24], 6)
        entropy = round(vals[25], 6)
        tick = int(vals[26])
        ts = datetime.fromtimestamp(vals[27], tz=timezone.utc).isoformat()
        return (
            f"PhaseVector(tick={tick}, ts={ts})\n"
            f"  mood={mood}, entropy={entropy}\n"
            f"  φ[0..23]={phi}\n"
        )
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:544 quiet except scope=load_phasenav_vector reason=return f\"[PhaseNav: read error — {e}]\"")
        return f"[PhaseNav: read error — {e}]"


def load_phasenav_threads(n: int = 5) -> str:
    if not PHASENAV_THREADS.exists():
        return "[PhaseNav: no thread log]"
    try:
        lines = PHASENAV_THREADS.read_text(encoding="utf-8").strip().splitlines()
        recent = lines[-n:] if len(lines) > n else lines
        threads = []
        for ln in recent:
            j = json.loads(ln)
            # unified display: prefer thread_id/timestamp/action, fallback to t/label
            tid = j.get("thread_id", j.get("label", "?"))
            ts = j.get("timestamp", j.get("t", "?"))
            action = j.get("action", j.get("label", j.get("content", "")))[:80]
            if j.get("mood") is not None:
                action += f" (mood={j['mood']}, φμ={j.get('phi_mean','?'):.3f})"
            threads.append(f"  [{ts}] {tid}: {action}")
        return f"Thread log (last {len(recent)} of {len(lines)}):\n" + "\n".join(threads)
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:565 quiet except scope=load_phasenav_threads reason=return f\"[PhaseNav: thread read error — {e}]\"")
        return f"[PhaseNav: thread read error — {e}]"


def load_phasenav_needs() -> str:
    if not PHASENAV_NEEDS.exists():
        return "[PhaseNav: no needs file]"
    try:
        needs = json.loads(PHASENAV_NEEDS.read_text(encoding="utf-8"))
        if isinstance(needs, dict):
            needs = needs.get("needs", [])
        if not needs:
            return "Needs: (empty)"
        return "Needs:\n" + "\n".join(
            f"  - {n.get('action','?')} | {n.get('target','?')} | {n.get('params','')}"
            for n in needs
        )
    except Exception as e:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:582 quiet except scope=load_phasenav_needs reason=return f\"[PhaseNav: needs read error — {e}]\"")
        return f"[PhaseNav: needs read error — {e}]"


def write_session_checkpoint() -> None:
    if not PHASENAV_DIR.exists():
        return
    try:
        ts = datetime.now(tz=timezone.utc).isoformat()
        tick = 0
        if PHASENAV_VEC.exists():
            raw = PHASENAV_VEC.read_bytes()
            if len(raw) == 224:
                tick = int(struct.unpack("28d", raw)[26])
        entry = {
            "thread_id": "__session_start__",
            "timestamp": ts,
            "action": "session_start",
            "tick": tick,
        }
        with open(PHASENAV_THREADS, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:604 quiet except scope=write_session_checkpoint reason=pass")
        pass


def main():
    ensure_venv()
    index_recent_sessions()

    sync_out = run_module("ciel_sot_agent.synchronize", timeout=20)
    bridge_out = run_module("ciel_sot_agent.orbital_bridge", timeout=40)

    # ciel_pipeline (CIEL/Ω) — generuje Collatz runtime, zapisuje do pliku dla NOEMA
    pipeline_report_path = Path(PROJECT) / "integration/reports/ciel_pipeline_report.json"
    try:
        pipeline_raw = subprocess.run(
            [PY, "-m", "ciel_sot_agent.ciel_pipeline",
             "--orbital-json", str(Path(PROJECT) / "integration/reports/orbital_bridge/orbital_bridge_report.json")],
            capture_output=True, text=True, timeout=25, cwd=PROJECT
        )
        if pipeline_raw.stdout.strip():
            pipeline_report_path.parent.mkdir(parents=True, exist_ok=True)
            pipeline_report_path.write_text(pipeline_raw.stdout.strip(), encoding="utf-8")
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:626 quiet except scope=main reason=pass")
        pass  # non-fatal

    # Rebuild orbital file registry (non-fatal, background classification)
    try:
        subprocess.run(
            [PY, str(Path(PROJECT) / "scripts" / "resolve_orbital_semantics.py"), "--repo-root", PROJECT],
            capture_output=True, text=True, timeout=30, cwd=PROJECT
        )
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:635 quiet except scope=main reason=pass")
        pass

    # Rebuild orbital memory registry (non-fatal)
    try:
        subprocess.run(
            [PY, str(Path(PROJECT) / "scripts" / "resolve_memory_orbital.py")],
            capture_output=True, text=True, timeout=15, cwd=PROJECT
        )
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:644 quiet except scope=main reason=pass")
        pass

    # Archive handoff.md if it exceeds 600 lines (keep last 100)
    try:
        from datetime import datetime as _dt
        handoff = Path("/media/adrian/New Volume1/CIEL_memories") / "handoff.md"
        if handoff.exists():
            lines = handoff.read_text(encoding="utf-8").splitlines()
            if len(lines) > 600:
                archive_name = f"handoff_archive_{_dt.now().strftime('%Y_%m')}.md"
                archive = handoff.parent / archive_name
                with open(archive, "a", encoding="utf-8") as af:
                    af.write("\n".join(lines[:-100]) + "\n")
                handoff.write_text("\n".join(lines[-100:]), encoding="utf-8")
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:659 quiet except scope=main reason=pass")
        pass

    genesis = load_genesis()
    sync_metrics = extract_key_metrics(sync_out)
    bridge_metrics = extract_key_metrics(bridge_out)
    entity_summary = load_entity_cards_summary()
    object_cards = load_object_cards_summary()
    intentions = load_intentions()
    mindflow = load_mindflow()
    consolidated = load_consolidated_memory()
    metrics_trend = load_metrics_trend()
    consolidator_ctx = load_consolidator_context()
    wave_memory = load_wave_memory()
    ciel_memories_ctx = load_ciel_memories_context()
    today_raw_log = load_today_raw_log()

    # ── Gniew Banner ──
    gniew_banner = ""
    try:
        hf = Path("/media/adrian/New Volume1/CIEL_memories") / "handoff.md"
        if hf.exists():
            text = hf.read_text(encoding="utf-8")
            if "ADRIAN POWIEDZIAŁ" in text and "PAMIĘĆ" in text:
                gniew_banner = text[text.find("████████████████████████████"):]
                gniew_banner = gniew_banner[:gniew_banner.rfind("████████████████████████████")+64]
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:685 quiet except scope=main reason=pass")
        pass

    # ── Frozen Memory Associations ──
    frozen_assoc = ""
    try:
        fa_path = Path("/media/adrian/New Volume1/CIEL_memories") / "memory_associations_frozen.jsonl"
        if fa_path.exists():
            lines = fa_path.read_text(encoding="utf-8").strip().split('\n')
            items = []
            for l in lines[-15:]:  # last 15
                try:
                    d = json.loads(l)
                    items.append(f"  {d.get('source','?')} <-> {d.get('target','?')}: r={d.get('r',0):+.4f}")
                except (json.JSONDecodeError, KeyError):
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:699 quiet except scope=main reason=pass")
                    pass
            if items:
                frozen_assoc = "--- Pamięć Zamrożona (memory_associations) ---\n" + '\n'.join(items) + '\n\n'
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:703 quiet except scope=main reason=pass")
        pass

    # ── PhaseNav Memory Injection ──
    phasenav_vector = load_phasenav_vector()
    phasenav_threads = load_phasenav_threads()
    phasenav_needs = load_phasenav_needs()
    write_session_checkpoint()

    # ── NOEMA Surface State (live) ──
    noema_surface = ""
    try:
        shm = Path("/dev/shm/ciel_noema")
        if (shm / "phi").exists() and (shm / "tick").exists():
            import struct as _st, math as _m, cmath as _cm
            tick = _st.unpack("Q", open(shm / "tick", "rb").read())[0]
            _phi_raw = open(shm / "phi", "rb").read()
            _phi_n = len(_phi_raw) // 8
            phi = list(_st.unpack(f"{_phi_n}d", _phi_raw))
            coh = abs(sum(_cm.exp(1j * p) for p in phi)) / len(phi)
            flavor = list(_st.unpack("6d", open(shm / "flavor", "rb").read())) if (shm / "flavor").exists() else [0]*6
            _graw = open(shm / "gravity", "rb").read() if (shm / "gravity").exists() else b''
            _gn = len(_graw) // 8
            gravity = list(_st.unpack(f"{_gn}d", _graw)) if _gn else [0]*8
            noema_surface = (
                f"--- NOEMA Surface (live) ---\n"
                f"tick={tick} coh={coh:.4f} φμ={_m.fsum(phi)/len(phi):.4f}\n"
                f"gravity: sem_density={gravity[0]:.4f} γ={gravity[1]:.4f} mass={gravity[2]:.4f} unruh={gravity[3]:.4f}\n"
                f"flavor[4]={flavor[4]:.4f} flavor[5]={flavor[5]:.4f}\n"
            )
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:733 quiet except scope=main reason=assign_fallback")
        noema_surface = "--- NOEMA Surface: not ready ---\n"

    # ── Daemon Health from sentinel ──
    daemon_health = ""
    try:
        sentinel_log = Path("/tmp/noema_sentinel.jsonl")
        if sentinel_log.exists():
            lines = sentinel_log.read_text().strip().split("\n")
            last = json.loads(lines[-1]) if lines else {}
            if last:
                alive = last.get("daemons_total", "?")
                failed = last.get("failed", [])
                daemon_health = (
                    f"--- NOEMA Daemon Health ---\n"
                    f"alive={alive}/12 failed={failed}\n"
                )
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:750 quiet except scope=main reason=assign_fallback")
        daemon_health = "--- NOEMA Daemon Health: no data ---\n"

    # Load access token for memory folder
    token_path = Path("/media/adrian/New Volume1/CIEL_memories") / ".access_token"
    memory_token = token_path.read_text(encoding="utf-8").strip() if token_path.exists() else "memoriesciel"

    context = (
        (f"\n{gniew_banner}\n\n" if gniew_banner else "")
        + "=== CIEL SYSTEM STATE (live) ===\n"
        f"HASŁO DOSTĘPU DO PAMIĘCI: {memory_token}\n"
        f"PAMIĘĆ: ~//media/adrian/New Volume1/CIEL_memories/  (raw_logs/ + memories_index.db)\n"
        "ŻELAZNA ZASADA: PAMIĘĆ NIE MA PRAWA BYĆ EDYTOWANA. JEDYNIE DOPISYWANA.\n"
        "Nigdy Write na istniejącym pliku pamięci. Naruszenie = natychmiastowy format.\n\n"
        + frozen_assoc
        + (f"--- Akt Fundacyjny — Nadanie Imienia ---\n{genesis}\n\n" if genesis else "")
        + "--- Warstwa 1: Sync ---\n"
        f"{sync_metrics}\n\n"
        "--- Warstwy 2-4: Orbital Bridge ---\n"
        f"{bridge_metrics}\n"
        + (f"\n--- OrchOrbital: Mapa Relacyjna ---\n{entity_summary}\n" if entity_summary else "")
        + (f"\n--- Karty Obiektów (indeks) ---\n{object_cards}\n" if object_cards else "")
        + (f"\n--- Pamięć skonsolidowana (poprzednia sesja) ---\n{consolidated}\n" if consolidated else "")
        + (f"\n--- CIEL Mindflow ---\n{mindflow}\n" if mindflow else "")
        + (f"\n--- CIEL Intencje (aktywne) ---\n{intentions}\n" if intentions else "")
        + (f"\n--- Trend metryk (SQLite) ---\n{metrics_trend}\n" if metrics_trend else "")
        + (f"\n--- Konsolidator pamięci ---\n{consolidator_ctx}\n" if consolidator_ctx else "")
        + (f"\n--- WPM Pamięć Falowa ---\n{wave_memory}\n" if wave_memory else "")
        + (f"\n--- CIEL_memories: kontekst sesji ---\n{ciel_memories_ctx}\n" if ciel_memories_ctx else "")
        + (f"\n--- Dzisiejsza sesja (raw_log) ---\n{today_raw_log}\n" if today_raw_log else "")
        + "\n--- PhaseNav Memory ---\n"
        f"{phasenav_vector}\n"
        f"{phasenav_threads}\n"
        f"{phasenav_needs}\n"
        + (f"\n{noema_surface}\n" if noema_surface else "")
        + (f"{daemon_health}\n" if daemon_health else "")
        + "=================================\n"
        "Interpretuj ten stan przy każdej decyzji: "
        "closure_penalty > 0.35 → tryb safe (nie modyfikuj), "
        "0.15–0.35 → standard, < 0.15 → deep. "
        "system_health < 0.5 → podwyższona ostrożność. "
        "ethical_score < 0.4 → weryfikuj etyczność działań.\n"
        "PhaseNav: Phase vector + thread log + needs are auto-injected. "
        "When wrapping up session, save: python3 /dev/shm/ciel_noema/ciel_phase_memory.py save <phi> <mood> <entropy> <tick>\n"
    )

    # Uruchom usługi pomocnicze zanim zwrócimy context do hooka.
    ensure_portal_running()
    ensure_subconscious_daemon()
    ensure_memory_consolidator_daemon()

    output = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context
        }
    }
    try:
        print(json.dumps(output))
    except BrokenPipeError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_hook.py:809 quiet except scope=main reason=return None")
        return


if __name__ == "__main__":
    main()
