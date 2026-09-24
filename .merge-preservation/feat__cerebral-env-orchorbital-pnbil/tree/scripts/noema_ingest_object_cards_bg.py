#!/usr/bin/env python3
"""Zaindeksuj docs/object_cards z CIEL_PROJECT_CANON do Knowledge DB w tle.

Fork do tła — aktuator dostaje wynik natychmiast.
Log: /media/adrian/New Volume/CIEL_memories/logs/ingest_object_cards.log
"""
from __future__ import annotations
import os, sys, sqlite3, time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

LOG_PATH = Path("/media/adrian/New Volume/CIEL_memories/logs/ingest_object_cards.log")
TARGET_DIR = Path("/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/docs/object_cards")


def _log(log, msg: str) -> None:
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    log.write(line + "\n")
    log.flush()


def run():
    from ciel_geometry.paths import P
    import noema_library_loader as ldr

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    log = open(str(LOG_PATH), "w", encoding="utf-8")

    _log(log, "=== ingest_object_cards START ===")
    _log(log, f"Katalog: {TARGET_DIR}")
    _log(log, f"DB: {ldr.KNOWLEDGE_DB}")

    conn = sqlite3.connect(str(ldr.KNOWLEDGE_DB), timeout=60)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA cache_size=-32000")
    ldr.ensure_schema(conn)
    conn.commit()

    before = conn.execute("SELECT COUNT(*) FROM doc_analysis").fetchone()[0]

    t0 = time.time()
    files = ldr.collect_files(TARGET_DIR)
    _log(log, f"Plików: {len(files)}")

    inserted = skipped = errors = 0
    for i, fpath in enumerate(files):
        try:
            result = ldr.load_file(fpath, conn, skip_pdf=True)
            if result:
                inserted += 1
            else:
                skipped += 1
        except Exception as e:
            errors += 1
            _log(log, f"  ERROR {fpath.name}: {e}")
            raise

        if (i + 1) % 500 == 0:
            conn.commit()
            elapsed = time.time() - t0
            rate = (i + 1) / elapsed if elapsed > 0 else 0
            _log(log, f"  [{i+1}/{len(files)}] ins={inserted} skip={skipped} ({rate:.1f} f/s)")

    conn.commit()

    after = conn.execute("SELECT COUNT(*) FROM doc_analysis").fetchone()[0]
    total_terms = conn.execute("SELECT COUNT(DISTINCT term) FROM term_index").fetchone()[0]
    conn.close()

    elapsed = time.time() - t0
    _log(log, f"\n=== DONE: {elapsed:.0f}s ===")
    _log(log, f"Nowych: {after - before} | Razem: {after} docs | {total_terms} unique terms")
    _log(log, f"Counters: {dict(ldr._counters)}")
    log.close()


def main():
    pid = os.fork()
    if pid > 0:
        print(f"Object cards ingestion uruchomiony, PID={pid}")
        print(f"Log: {LOG_PATH}")
        sys.exit(0)

    os.setsid()
    devnull = os.open("/dev/null", os.O_RDWR)
    os.dup2(devnull, 0)
    os.dup2(devnull, 1)
    os.dup2(devnull, 2)
    os.close(devnull)
    run()


if __name__ == "__main__":
    main()
