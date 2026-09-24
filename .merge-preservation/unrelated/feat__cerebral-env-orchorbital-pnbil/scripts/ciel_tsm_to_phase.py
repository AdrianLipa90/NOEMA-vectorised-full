#!/usr/bin/env python3
"""Bridge: TSM (ciel_doc_ingest chunks) → PhaseMemory (CIELingo query store).

TSM ma 59k+ chunków z proper ingest. PhaseMemory był pusty.
Ten skrypt odczytuje chunki z TSM, koduje przez CIELingo i wpisuje do PhaseMemory.
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)

import hashlib
import logging
import sqlite3
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
_SRC = str(ROOT / "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

logging.basicConfig(level=logging.INFO, format="[tsm2phase] %(asctime)s %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger(__name__)

TSM_PATHS = [
    Path("/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/src/CIEL_MEMORY_SYSTEM/TSM/ledger/memory_ledger.db"),
    Path("/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/src/CIEL_OMEGA_COMPLETE_SYSTEM/CIEL_MEMORY_SYSTEM/TSM/ledger/memory_ledger.db"),
]

PHASE_MEMORY_PATH = Path("/tmp/cielingo_phase_memory")

BATCH_SIZE = 500
SLEEP_BETWEEN = 0.01
BATCH_PAUSE = 0.5  # extra pause every 10 batches


def _find_tsm() -> Path | None:
    for p in TSM_PATHS:
        if p.exists():
            return p
    return None


def run(limit: int = 0, clear_existing: bool = True):
    from ciel_geometry.cielingo_phase_memory import PhaseMemory
    from ciel_geometry.cielingo_phase_encoder import fast_encode_text

    tsm_path = _find_tsm()
    if not tsm_path:
        log.error("TSM DB not found at any path")
        return
    log.info("TSM: %s", tsm_path)

    conn = sqlite3.connect(str(tsm_path))
    conn.execute("PRAGMA journal_mode=WAL")
    total = conn.execute("SELECT COUNT(*) FROM memories WHERE D_sense IS NOT NULL AND length(D_sense) > 20").fetchone()[0]
    log.info("Total TSM entries with content: %d", total)

    if limit and limit < total:
        log.info("Limiting to %d (use --limit 0 for all)", limit)
        rows = conn.execute(
            "SELECT memorise_id, D_sense, source FROM memories WHERE D_sense IS NOT NULL AND length(D_sense) > 20 ORDER BY created_at ASC LIMIT ?",
            (limit,)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT memorise_id, D_sense, source FROM memories WHERE D_sense IS NOT NULL AND length(D_sense) > 20 ORDER BY created_at ASC"
        ).fetchall()
    conn.close()
    log.info("Loaded %d rows from TSM", len(rows))

    if clear_existing and PHASE_MEMORY_PATH.exists():
        import shutil
        shutil.rmtree(PHASE_MEMORY_PATH)
        log.info("Cleared existing PhaseMemory")

    pm = PhaseMemory.load_or_create(str(PHASE_MEMORY_PATH), max_size=50000)
    log.info("PhaseMemory ready (current: %d entries)", len(pm.texts))

    added = 0
    skipped = 0
    t0 = time.time()
    for i, (mid, text, source) in enumerate(rows):
        if not text or len(text.strip()) < 20:
            skipped += 1
            continue
        try:
            phi = fast_encode_text(text)
            pm.add(text, phi, source=f"tsm:{mid}", metadata={"tsm_id": mid, "source": source or ""})
            added += 1
        except Exception as e:
            skipped += 1

        if (i + 1) % BATCH_SIZE == 0:
            elapsed = time.time() - t0
            rate = (i + 1) / elapsed if elapsed > 0 else 0
            log.info("  [%d/%d] added=%d skipped=%d rate=%.0f/s", i + 1, len(rows), added, skipped, rate)
            # Extra pause every 10th batch
            if (i + 1) % (BATCH_SIZE * 10) == 0:
                time.sleep(BATCH_PAUSE)

    elapsed = time.time() - t0
    log.info("Done: %d added, %d skipped, %.1fs (%.0f/s)", added, skipped, elapsed, added / elapsed if elapsed > 0 else 0)
    pm.save(str(PHASE_MEMORY_PATH))
    log.info("PhaseMemory saved: %d entries at %s", len(pm.texts), PHASE_MEMORY_PATH)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="Limit entries (0=all)")
    ap.add_argument("--no-clear", action="store_true", help="Don't clear existing PhaseMemory")
    args = ap.parse_args()
    run(limit=args.limit, clear_existing=not args.no_clear)
