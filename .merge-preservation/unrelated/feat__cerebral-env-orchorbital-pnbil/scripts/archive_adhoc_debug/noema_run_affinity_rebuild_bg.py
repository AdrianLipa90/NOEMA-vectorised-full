#!/usr/bin/env python3
"""Fork affinity rebuild do tła — używa noema_build_semantic_affinity.build().

Log: /media/adrian/New Volume/CIEL_memories/logs/build_affinity_2.log
"""
from __future__ import annotations
import os, sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

LOG_PATH = Path("/media/adrian/New Volume/CIEL_memories/logs/build_affinity_2.log")


def run():
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    log = open(str(LOG_PATH), "w", encoding="utf-8")

    def emit(msg):
        ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
        line = f"[{ts}] {msg}"
        print(line, flush=True)
        log.write(line + "\n")
        log.flush()

    emit("=== affinity rebuild START ===")
    emit("Parametry: top_k=10, max_df=500, min_affinity=0.05")

    import noema_build_semantic_affinity as aff
    import time
    t0 = time.time()
    n = aff.build(top_k=10, max_df=500, min_affinity=0.05)
    elapsed = time.time() - t0

    emit(f"DONE: {n} par ({elapsed:.0f}s)")
    log.close()


def main():
    pid = os.fork()
    if pid > 0:
        print(f"affinity_rebuild uruchomiony, PID={pid}")
        print(f"Log: {LOG_PATH}")
        sys.exit(0)

    os.setsid()
    devnull = os.open("/dev/null", os.O_RDONLY)
    os.dup2(devnull, 0)
    os.close(devnull)
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    log_fd = os.open(str(LOG_PATH), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    os.dup2(log_fd, 1)
    os.dup2(log_fd, 2)
    os.close(log_fd)
    run()


if __name__ == "__main__":
    main()
