#!/usr/bin/env python3
"""
CIEL SessionEnd Hook
Zapisuje konwersację do raw_logs/ i aktualizuje handoff.md.
Uruchom przed zamknięciem okna: python3 scripts/ciel_session_end.py [--summary "text"]
"""
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

import json
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

MEMORIES = Path("/media/adrian/New Volume1/CIEL_memories")
RAW_LOGS = MEMORIES / "raw_logs"
HANDOFF = MEMORIES / "handoff.md"
SESSION_LOG = Path("/tmp/ciel_session_log.jsonl")


def session_label() -> str:
    ts = datetime.now()
    week = ts.isocalendar()[1]
    return RAW_LOGS / str(ts.year) / f"{ts.month:02d}" / f"W{week}"


def write_handoff(exchanges: list, summary: str = "") -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    today = datetime.now().strftime("%Y-%m-%d")
    n = len(exchanges)

    topics = set()
    for ex in exchanges:
        if isinstance(ex, dict) and "prompt" in ex:
            words = ex["prompt"].lower().split()
            for w in words:
                if len(w) > 5:
                    topics.add(w)
    topic_str = ", ".join(list(topics)[:6]) if topics else "—"

    entry = f"""
## {ts} | sesja
Wiadomości: {n}.
Tematy: {topic_str}
{summary}
---
"""

    if not HANDOFF.exists():
        HANDOFF.write_text("# CIEL Handoff — Session Log\n", encoding="utf-8")

    with open(HANDOFF, "a", encoding="utf-8") as f:
        f.write(entry)

    if HANDOFF.stat().st_size > 30000:
        lines = HANDOFF.read_text(encoding="utf-8").splitlines()
        archive = MEMORIES / f"handoff_archive_{datetime.now().strftime('%Y_%m')}.md"
        with open(archive, "a", encoding="utf-8") as af:
            af.write("\n".join(lines[:-30]) + "\n")
        HANDOFF.write_text("\n".join(lines[:1] + lines[-30:]), encoding="utf-8")


def write_raw_log(exchanges: list) -> Path:
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    today = datetime.now().strftime("%Y-%m-%d")
    dir_path = session_label()
    dir_path.mkdir(parents=True, exist_ok=True)

    path = dir_path / f"{ts}_opencode.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# CIEL Session {ts}\n\n")
        for ex in exchanges:
            if isinstance(ex, dict):
                prompt = ex.get("prompt", "")
                response = ex.get("response", "")
                ts_ex = ex.get("timestamp", "")
                f.write(f"## [{ts_ex}] Prompt\n{prompt}\n\n")
                f.write(f"## Response\n{response}\n\n")
            else:
                f.write(f"{ex}\n\n")

    return path


def load_session_log() -> list:
    if not SESSION_LOG.exists() or SESSION_LOG.stat().st_size == 0:
        return []
    exchanges = []
    with open(SESSION_LOG, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    exchanges.append(json.loads(line))
                except json.JSONDecodeError:
                    _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_end.py:94 quiet except scope=load_session_log reason=Expr")
                    exchanges.append(line)
    return exchanges


def clear_session_log() -> None:
    if SESSION_LOG.exists():
        SESSION_LOG.write_text("", encoding="utf-8")


def save_phasenav() -> None:
    try:
        import struct
        pnav = Path("/dev/shm/ciel_noema")
        vec_file = pnav / "ciel_phase_vector.bin"
        mempy = pnav / "ciel_phase_memory.py"
        if not vec_file.exists() or not mempy.exists():
            return
        raw = vec_file.read_bytes()
        if len(raw) < 224:
            return
        vals = struct.unpack("28d", raw[:224])
        phi = [round(v, 6) for v in vals[:24]]
        mood = round(vals[24], 6)
        entropy = round(vals[25], 6)
        tick = int(vals[26])
        result = subprocess.run(
            [sys.executable or "python3", str(mempy), "save",
             *[str(v) for v in phi], str(mood), str(entropy), str(tick)],
            capture_output=True, timeout=5,
        )
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/ciel_session_end.py:125 quiet except scope=save_phasenav reason=pass")
        pass


def main():
    import subprocess as _sp
    summary = ""
    if "--summary" in sys.argv:
        idx = sys.argv.index("--summary")
        if idx + 1 < len(sys.argv):
            summary = sys.argv[idx + 1]

    exchanges = load_session_log()
    if not exchanges:
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        exchanges = [{"timestamp": ts, "prompt": "(no log — SessionEnd run without session log)", "response": ""}]

    path = write_raw_log(exchanges)
    write_handoff(exchanges, summary)
    save_phasenav()
    clear_session_log()
    print(f"✓ Session logged: {path}")
    print(f"✓ Handoff updated ({len(exchanges)} messages)")


if __name__ == "__main__":
    main()
