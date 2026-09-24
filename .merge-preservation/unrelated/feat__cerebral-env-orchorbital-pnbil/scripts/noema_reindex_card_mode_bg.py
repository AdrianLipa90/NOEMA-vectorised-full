#!/usr/bin/env python3
"""Re-indeksuj karty NOEMA z raw JSON essence — używa naprawionego card_mode=True.

Fork do tła. Log: /media/adrian/New Volume/CIEL_memories/logs/reindex_card_mode.log
"""
from __future__ import annotations
import os, sys, sqlite3, time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from ciel_geometry.paths import P
import noema_library_loader as ldr

LOG_PATH = Path("/media/adrian/New Volume/CIEL_memories/logs/reindex_card_mode.log")


def _log(log, msg):
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    log.write(line + "\n")
    log.flush()


def run():
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    log = open(str(LOG_PATH), "w", encoding="utf-8")

    _log(log, "=== reindex_card_mode START ===")

    conn = sqlite3.connect(str(P.DB.KNOWLEDGE), timeout=60)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")

    # Wszyscy kandydaci z raw JSON essence
    rows = conn.execute(
        "SELECT idx, filename, source_url FROM doc_analysis WHERE essence LIKE '{%'"
    ).fetchall()
    _log(log, f"Kandydatów z raw JSON essence: {len(rows)}")

    updated = skipped_no_path = skipped_no_nl = skipped_unchanged = 0

    for i, (idx, filename, source_url) in enumerate(rows):
        # Resolve path
        path = None
        if source_url:
            p = Path(source_url)
            if p.exists():
                path = p
        if path is None:
            p2 = ldr.NOEMA_LIBRARY / filename
            if p2.exists():
                path = p2
        if path is None:
            p3 = Path(filename)
            if p3.is_absolute() and p3.exists():
                path = p3
        if path is None:
            skipped_no_path += 1
            continue

        # Parsuj z nowym card_mode
        try:
            new_content = ldr.parse_json(path)
        except Exception as e:
            _log(log, f"  ERROR parse_json({filename}): {e}")
            raise

        if not new_content or new_content.strip().startswith("{"):
            skipped_no_nl += 1
            continue

        new_essence = new_content[:500]
        old_essence = conn.execute(
            "SELECT essence FROM doc_analysis WHERE idx=?", (idx,)
        ).fetchone()
        old_essence = (old_essence[0] or "") if old_essence else ""

        if old_essence[:500] == new_essence:
            skipped_unchanged += 1
            continue

        # Aktualizuj
        conn.execute(
            "UPDATE doc_analysis SET essence=?, full_text_len=? WHERE idx=?",
            (new_essence, len(new_content), idx)
        )
        conn.execute("DELETE FROM term_index WHERE idx=?", (idx,))
        ldr._update_term_index(conn, idx, new_content)
        updated += 1

        if updated % 100 == 0:
            conn.commit()
            _log(log, f"  [{i+1}/{len(rows)}] updated={updated} no_path={skipped_no_path} no_nl={skipped_no_nl}")

    conn.commit()
    terms = conn.execute("SELECT COUNT(DISTINCT term) FROM term_index").fetchone()[0]
    conn.close()

    _log(log, f"\n=== DONE ===")
    _log(log, f"Updated: {updated} | No path: {skipped_no_path} | No NL: {skipped_no_nl} | Unchanged: {skipped_unchanged}")
    _log(log, f"Unique terms po reindexie: {terms}")
    log.close()


def main():
    pid = os.fork()
    if pid > 0:
        print(f"reindex_card_mode uruchomiony, PID={pid}")
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
