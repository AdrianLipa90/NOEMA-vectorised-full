#!/usr/bin/env python3
"""Uruchom noema_build_semantic_affinity w tle — fork do tła, aktuator nie blokuje.

Log: /media/adrian/New Volume/CIEL_memories/logs/build_affinity.log
"""
from __future__ import annotations
import os, sys
from pathlib import Path

LOG_PATH = Path("/media/adrian/New Volume/CIEL_memories/logs/build_affinity.log")

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))


def run():
    import noema_build_semantic_affinity as aff
    from datetime import datetime, timezone

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    log = open(str(LOG_PATH), "w", encoding="utf-8")

    def emit(msg):
        ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
        line = f"[{ts}] {msg}"
        print(line, flush=True)
        log.write(line + "\n")
        log.flush()

    emit("=== noema_build_semantic_affinity START ===")
    emit("Parametry: top_k=10, max_df=500, min_affinity=0.05")
    try:
        n = aff.build(top_k=10, max_df=500, min_affinity=0.05)
        emit(f"=== DONE: {n} par wstawionych ===")
    except Exception as e:
        emit(f"ERROR: {e}")
        raise
    finally:
        log.close()


def main():
    pid = os.fork()
    if pid > 0:
        print(f"Affinity rebuild uruchomiony, PID={pid}")
        print(f"Log: {LOG_PATH}")
        sys.exit(0)

    os.setsid()
    devnull = os.open("/dev/null", os.O_RDONLY)
    os.dup2(devnull, 0)
    os.close(devnull)
    # Przekieruj stdout+stderr do loga — żeby build() print() był widoczny
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    log_fd = os.open(str(LOG_PATH), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    os.dup2(log_fd, 1)
    os.dup2(log_fd, 2)
    os.close(log_fd)
    run()


if __name__ == "__main__":
    main()
