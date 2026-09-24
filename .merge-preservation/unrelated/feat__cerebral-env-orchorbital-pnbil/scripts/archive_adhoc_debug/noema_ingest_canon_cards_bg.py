#!/usr/bin/env python3
"""Zaindeksuj karty z CIEL_PROJECT_CANON/NOEMA/cards/ do Knowledge DB w tle.

Fork do tła — aktuator dostaje wynik natychmiast.
Log: /media/adrian/New Volume/CIEL_memories/logs/ingest_canon_cards.log
"""
from __future__ import annotations
import os, sys, sqlite3, time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

LOG_PATH = Path("/media/adrian/New Volume/CIEL_memories/logs/ingest_canon_cards.log")
CARDS_DIR = Path("/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/cards")


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

    _log(log, "=== ingest_canon_cards START ===")
    _log(log, f"Katalog kart: {CARDS_DIR}")
    _log(log, f"DB: {ldr.KNOWLEDGE_DB}")

    conn = sqlite3.connect(str(ldr.KNOWLEDGE_DB), timeout=60)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA cache_size=-64000")
    ldr.ensure_schema(conn)
    conn.commit()

    before = conn.execute("SELECT COUNT(*) FROM doc_analysis").fetchone()[0]

    t0 = time.time()
    processed = 0
    inserted = 0
    skipped = 0

    files = ldr.collect_files(CARDS_DIR)
    _log(log, f"Plików do przetworzenia: {len(files)}")

    for fpath in files:
        result = ldr.load_file(fpath, conn, skip_pdf=True)
        processed += 1
        if result:
            inserted += 1
        else:
            skipped += 1

        if processed % 200 == 0:
            conn.commit()
            elapsed = time.time() - t0
            rate = processed / elapsed if elapsed > 0 else 0
            _log(log, f"  [{processed}/{len(files)}] inserted={inserted} skip={skipped} ({rate:.1f} f/s)")

    conn.commit()

    after = conn.execute("SELECT COUNT(*) FROM doc_analysis").fetchone()[0]
    total_terms = conn.execute("SELECT COUNT(DISTINCT term) FROM term_index").fetchone()[0]
    conn.close()

    elapsed = time.time() - t0
    _log(log, "")
    _log(log, f"=== DONE: {elapsed:.0f}s ===")
    _log(log, f"Nowych dokumentów: {after - before}")
    _log(log, f"Razem docs: {after} | unique terms: {total_terms}")
    _log(log, f"Counters: {dict(ldr._counters)}")
    log.close()


def main():
    pid = os.fork()
    if pid > 0:
        print(f"Canon cards ingestion uruchomiony, PID={pid}")
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
