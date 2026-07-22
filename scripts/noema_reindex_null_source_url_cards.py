#!/usr/bin/env python3
"""Re-indeksuj karty .noema.card.json które mają NULL source_url w DB.

Szuka pliku po nazwie w znanych katalogach kart CIEL_PROJECT_CANON,
re-parsuje przez parse_json() i aktualizuje essence + term_index.
"""
from __future__ import annotations
import os, sys, sqlite3, time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from ciel_geometry.paths import P
import noema_library_loader as ldr

LOG_PATH = Path("/media/adrian/New Volume/CIEL_memories/logs/reindex_null_src_cards.log")
KNOWLEDGE_DB = Path(P.DB.KNOWLEDGE)

# Katalogi z kartami — przeszukuj w tej kolejności
CARD_SEARCH_DIRS = [
    Path("/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/cards"),
    Path("/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/docs/object_cards"),
    Path("/media/adrian/New Volume/NOEMA_LIBRARY"),
    Path("/home/adrian/noema/cards"),
]


def _find_card(basename: str) -> Path | None:
    for base_dir in CARD_SEARCH_DIRS:
        if not base_dir.exists():
            continue
        for candidate in base_dir.rglob(basename):
            if candidate.is_file():
                return candidate
    return None


def _log(log, msg: str) -> None:
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    log.write(line + "\n")
    log.flush()


def run():
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    log = open(str(LOG_PATH), "w", encoding="utf-8")

    _log(log, "=== noema_reindex_null_source_url_cards START ===")
    _log(log, f"DB: {KNOWLEDGE_DB}")

    conn = sqlite3.connect(str(KNOWLEDGE_DB), timeout=60)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")

    # Karty bez source_url z surowym JSON
    rows = conn.execute(
        "SELECT idx, filename FROM doc_analysis "
        "WHERE (essence LIKE '{%' OR essence LIKE ' {%') "
        "AND filename LIKE '%.noema.card.json' "
        "AND (source_url IS NULL OR source_url = '')"
    ).fetchall()

    _log(log, f"Kart bez source_url z raw essence: {len(rows)}")

    updated = skipped = errors = 0
    t0 = time.time()

    for idx, filename in rows:
        basename = Path(filename).name
        path = _find_card(basename)
        if path is None:
            _log(log, f"  NIE ZNALEZIONO: {basename}")
            skipped += 1
            continue

        try:
            new_content = ldr.parse_json(path)
        except Exception as e:
            _log(log, f"  ERROR parse_json({basename}): {e}")
            errors += 1
            raise

        if not new_content or len(new_content.strip()) < ldr.MIN_CHUNK:
            _log(log, f"  PUSTY NL: {basename}")
            skipped += 1
            continue

        old_essence = (conn.execute(
            "SELECT essence FROM doc_analysis WHERE idx = ?", (idx,)
        ).fetchone() or ("",))[0] or ""

        new_essence = new_content[:500]
        if old_essence == new_essence:
            skipped += 1
            continue

        conn.execute(
            "UPDATE doc_analysis SET essence = ?, full_text_len = ?, source_url = ? WHERE idx = ?",
            (new_essence, len(new_content), str(path), idx)
        )
        conn.execute("DELETE FROM term_index WHERE idx = ?", (idx,))
        ldr._update_term_index(conn, idx, new_content)
        updated += 1
        _log(log, f"  OK [{updated}]: {basename} → {path}")

    conn.commit()

    # Statystyki końcowe
    still_null = conn.execute(
        "SELECT COUNT(*) FROM doc_analysis "
        "WHERE (essence LIKE '{%') AND filename LIKE '%.noema.card.json' "
        "AND (source_url IS NULL OR source_url = '')"
    ).fetchone()[0]

    conn.close()
    elapsed = time.time() - t0
    _log(log, "")
    _log(log, f"=== DONE: {elapsed:.1f}s ===")
    _log(log, f"Updated={updated} Skip={skipped} Err={errors}")
    _log(log, f"Kart nadal bez source_url z raw essence: {still_null}")
    log.close()


def main():
    pid = os.fork()
    if pid > 0:
        print(f"Null-source_url card reindex uruchomiony, PID={pid}")
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
