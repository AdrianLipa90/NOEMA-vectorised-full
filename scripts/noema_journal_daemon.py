#!/usr/bin/env python3
"""Journal daemon — journalctl pipe → NOEMA surface.

Czyta live log systemu przez `journalctl -f -o json`, parsuje,
mapuje severity → emocje, i zapisuje na powierzchnię.

Surface output (/dev/shm/ciel_noema/journal/):
  recent.jsonl  — ostatnie 64 wiadomości
  stats.json    — rate, severity distribution, top units
  alert.json    — najwyższy priorytet w oknie

Integracja:
  - severity → flavor/emotion dla CIELingo sync daemon
  - alert rate → ω modulation na M5 (Affective)
  - critical/fail → scar injection

Użycie:
  .venv/bin/python3 scripts/noema_journal_daemon.py
  systemctl --user start noema-journal.service
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
import signal
import subprocess
import sys
import time
from collections import Counter, deque
from pathlib import Path

from ciel_geometry.noema_registry import registry

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

SURFACE = Path("/dev/shm/ciel_noema")
JOURNAL_DIR = SURFACE / "journal"

# Severity → label, emotion map (syslog PRIORITY 0-7)
SEVERITY_MAP: dict[int, tuple[str, str]] = {
    0: ("emerg",   "fear"),
    1: ("alert",   "fear"),
    2: ("crit",    "fear"),
    3: ("err",     "anger"),
    4: ("warning", "tension"),
    5: ("notice",  "neutral"),
    6: ("info",    "curiosity"),
    7: ("debug",   "curiosity"),
}

# Jednostki NOEMA — filtrowane wyżej w logu
NOEMA_UNITS = set()

_RING: deque[dict] = deque(maxlen=64)
_RATE_DEQUE: deque[float] = deque(maxlen=30)  # timestampy ostatnich 30s
_UNIT_COUNT: Counter = Counter()
_SEV_COUNT: Counter = Counter()
_ALERT: dict | None = None  # najwyższy priorytet w oknie
_running = True
_last_heartbeat = 0

def log(msg: str) -> None:
    ts = time.strftime("%H:%M:%S")
    print(f"[journal] {ts} {msg}", flush=True)

def _severity_weight(sev: int) -> float:
    """0=emerg (1.0) → 7=debug (0.0)."""
    return 1.0 - sev / 7.0

def _init_dirs() -> None:
    JOURNAL_DIR.mkdir(parents=True, exist_ok=True)
    SURFACE.mkdir(parents=True, exist_ok=True)

def _write_surface() -> None:
    """Zapisz stan journala na surface."""
    now = time.time()

    # 1. stats.json
    total = sum(_SEV_COUNT.values())
    sev_dist = {k: {"count": v, "pct": round(100 * v / total, 1) if total else 0}
                for k, v in _SEV_COUNT.most_common()}
    top_units = [{"unit": u, "count": c}
                 for u, c in _UNIT_COUNT.most_common(10)]
    rate = len(_RATE_DEQUE) / max(30, 1)  # msgs/sec over last 30s

    # Dominant emotion
    dom_sev = _SEV_COUNT.most_common(1)
    dom_emotion = SEVERITY_MAP.get(dom_sev[0][0], ("?", "neutral"))[1] if dom_sev else "neutral"

    stats = {
        "ts": now,
        "total_msgs": total,
        "rate": round(rate, 2),
        "dominant_severity": dom_sev[0][0] if dom_sev else -1,
        "dominant_emotion": dom_emotion,
        "severity": sev_dist,
        "top_units": top_units,
        "alert": _ALERT,
    }
    with open(JOURNAL_DIR / "stats.json", "w") as f:
        json.dump(stats, f, indent=2)

    # 2. recent.jsonl — ostatnie 64
    with open(JOURNAL_DIR / "recent.jsonl", "w") as f:
        for entry in _RING:
            f.write(json.dumps(entry) + "\n")

    # 3. alert.json — najwyższy priorytet
    if _ALERT:
        with open(JOURNAL_DIR / "alert.json", "w") as f:
            json.dump(_ALERT, f, indent=2)

    # 4. Journal → flavor bridge: zapisz aktualną emocję jako plik
    #    CIELingo sync daemon czyta journal/emotion.json aby modulować flavor
    emotion_data = {
        "ts": now,
        "dominant_emotion": dom_emotion,
        "rate": round(rate, 2),
        "alert_severity": _ALERT["priority"] if _ALERT else -1,
        "alert_unit": _ALERT.get("unit", "") if _ALERT else "",
    }
    with open(JOURNAL_DIR / "emotion.json", "w") as f:
        json.dump(emotion_data, f)

def process_line(line: str) -> None:
    """Parsuj pojedynczą linię JSON z journalctl."""
    global _ALERT
    try:
        entry = json.loads(line)
    except json.JSONDecodeError:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_journal_daemon.py:138 quiet except scope=process_line reason=return None")
        raise
        return

    # Wyciągnij pola
    pri = entry.get("PRIORITY")
    if pri is None:
        return
    try:
        priority = int(pri)
    except (ValueError, TypeError):
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_journal_daemon.py:147 quiet except scope=process_line reason=assign_fallback")
        raise
        priority = 6

    # entry.get("MESSAGE", fallback) only uses fallback when the key is
    # ABSENT — journalctl sometimes emits {"MESSAGE": null} explicitly
    # (binary/malformed log entries), and `None[:200]` crashed the whole
    # daemon uncaught. Confirmed 2026-07-08 alongside the reg_token fix
    # above — same root cause class (540 restarts), this is the other half.
    msg = entry.get("MESSAGE") or entry.get("SYSLOG_IDENTIFIER") or ""
    msg = msg[:200]
    unit = entry.get("_SYSTEMD_UNIT", entry.get("SYSLOG_IDENTIFIER", "unknown"))
    pid = entry.get("_PID", entry.get("SYSLOG_IDENTIFIER", "0"))
    ts = entry.get("__REALTIME_TIMESTAMP", str(time.time()))

    severity_label, emotion = SEVERITY_MAP.get(priority, ("?", "neutral"))

    # Zbuduj wpis
    record = {
        "ts": int(ts) / 1_000_000 if ts.isdigit() else time.time(),
        "priority": priority,
        "severity": severity_label,
        "emotion": emotion,
        "unit": unit,
        "pid": pid,
        "msg": msg,
        "weight": round(_severity_weight(priority), 3),
    }

    # Oblicz rate
    now = time.time()
    _RATE_DEQUE.append(now)

    # Zapisz
    _RING.append(record)
    _UNIT_COUNT[unit] += 1
    _SEV_COUNT[priority] += 1

    # Alert: najwyższy priorytet (najniższa liczba = emerg)
    if _ALERT is None or priority < _ALERT["priority"]:
        _ALERT = record
    elif priority == _ALERT["priority"] and priority <= 3:
        # aktualizuj jeśli ten sam priorytet krytyczny
        _ALERT = record

def journal_feed() -> None:
    """Główna pętla: pipe journalctl -f, parsuj JSON."""
    global _running

    log("starting journal feed")

    # Uruchom journalctl
    cmd = [
        "journalctl", "-f", "-o", "json",
        "--no-pager", "--since=-10s",
        "-p", "debug",  # all levels
    ]

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1,  # line buffered
        )
    except FileNotFoundError:
        log("journalctl not found — is systemd running?")
        _running = False
        return

    log(f"journalctl PID={proc.pid}")

    # Was never defined — registry.heartbeat(reg_token) below raised
    # NameError every 50th loop iteration, uncaught by the loop's own
    # broad except (it's inside a nested try, but the crash still killed
    # the whole daemon since nothing above main() catches it). Confirmed
    # 2026-07-08: 540 systemd restarts on this service alone.
    reg_token = registry.register("journal")

    # Własna pętla z heartbeat co 5s gdy cisza
    poll = proc.stdout
    last_write = 0
    line_count = 0

    hb_count = 0
    while _running and proc.poll() is None:
        # registry heartbeat
        if hb_count % 50 == 0:
            try:
                registry.heartbeat(reg_token)
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_journal_daemon.py:223 quiet except scope=journal_feed reason=pass")
                raise
                pass
        hb_count += 1
        try:
            line = poll.readline()
        except Exception:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_journal_daemon.py:228 quiet except scope=journal_feed reason=break")
            raise
            break

        if not line:
            # heartbeat: zapisz stan nawet gdy cisza
            now = time.time()
            if now - last_write > 5:
                _write_surface()
                last_write = now
            else:
                time.sleep(0.05)
            continue

        line = line.strip()
        if not line:
            continue

        process_line(line)
        line_count += 1

        # Zapisz co 5 wiadomości lub co 5s
        now = time.time()
        if line_count % 5 == 0 or now - last_write > 5:
            _write_surface()
            last_write = now

        if line_count % 50 == 0:
            total = sum(_SEV_COUNT.values())
            log(f"{total} msgs | rate={len(_RATE_DEQUE)/30:.1f}/s "
                f"top={_UNIT_COUNT.most_common(1)[0][0] if _UNIT_COUNT else '?'}")

    # Cleanup
    if proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(3)
        except subprocess.TimeoutExpired:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_journal_daemon.py:264 quiet except scope=journal_feed reason=Expr")
            raise
            proc.kill()

    log(f"stopped — {line_count} lines processed")

def signal_handler(sig, frame) -> None:
    global _running
    log(f"signal {sig}, exiting")
    _running = False

def main() -> None:
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    _init_dirs()

    if "--once" in sys.argv:
        # Pojedynczy batch: ostatnie 30 wiadomości
        try:
            result = subprocess.run(
                ["journalctl", "-o", "json", "--no-pager",
                 "--since=-30s", "-n", "50"],
                capture_output=True, text=True, timeout=15,
            )
            for line in result.stdout.strip().splitlines():
                if line:
                    process_line(line)
            _write_surface()
            stats_path = JOURNAL_DIR / "stats.json"
            if stats_path.exists():
                print(stats_path.read_text())
        except Exception as e:
            log(f"--once error: {e}")
        return

    log("daemon start")
    journal_feed()
    log("daemon stop")

if __name__ == "__main__":
    main()
