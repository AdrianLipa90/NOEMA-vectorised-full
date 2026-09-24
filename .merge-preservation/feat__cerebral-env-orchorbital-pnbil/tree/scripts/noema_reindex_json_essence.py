#!/usr/bin/env python3
"""Re-indeksuj pliki JSON, których essence zaczyna się od '{' (surowy JSON).

Wykrywa wpisy doc_analysis z essence='{...', re-parsuje source_url przez
naprawione parse_json(), aktualizuje essence + term_index.
Uruchamia się w tle przez os.fork() — aktuator dostaje wynik natychmiast.

Log: /media/adrian/New Volume/CIEL_memories/logs/reindex_json_essence.log
"""
from __future__ import annotations
import os, sys, json, math, re, sqlite3, time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from ciel_geometry.paths import P
import noema_library_loader as ldr

LOG_PATH = Path("/media/adrian/New Volume/CIEL_memories/logs/reindex_json_essence.log")
KNOWLEDGE_DB = Path(P.DB.KNOWLEDGE)
NOEMA_LIBRARY = ldr.NOEMA_LIBRARY

BATCH_SIZE = 100  # commit co ile dokumentów


def _log(log, msg: str) -> None:
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    log.write(line + "\n")
    log.flush()


def _candidates(conn: sqlite3.Connection) -> list[tuple[int, str, str]]:
    """Zwróć (idx, filename, source_url) gdzie essence zaczyna się od '{'."""
    rows = conn.execute(
        "SELECT idx, filename, source_url FROM doc_analysis "
        "WHERE essence LIKE '{%' OR essence LIKE ' {%'"
    ).fetchall()
    return rows


def _resolve_path(filename: str, source_url: str) -> Path | None:
    """Znajdź fizyczny plik — source_url pierwszeństwo, fallback NOEMA_LIBRARY."""
    if source_url:
        p = Path(source_url)
        if p.exists():
            return p
    # spróbuj NOEMA_LIBRARY / filename (relative)
    p2 = NOEMA_LIBRARY / filename
    if p2.exists():
        return p2
    # filename może być absolutną ścieżką
    p3 = Path(filename)
    if p3.exists():
        return p3
    return None


def _reindex_doc(conn: sqlite3.Connection, idx: int, filename: str, source_url: str,
                 log) -> bool:
    path = _resolve_path(filename, source_url)
    if path is None:
        _log(log, f"  SKIP (nie znaleziono pliku): {filename}")
        return False

    try:
        new_content = ldr.parse_json(path)
    except Exception as e:
        _log(log, f"  ERROR parse_json({filename}): {e}")
        raise

    if not new_content or len(new_content.strip()) < ldr.MIN_CHUNK:
        _log(log, f"  SKIP (pusty NL): {filename}")
        return False

    old_essence = conn.execute(
        "SELECT essence FROM doc_analysis WHERE idx = ?", (idx,)
    ).fetchone()
    old_essence = (old_essence[0] or "") if old_essence else ""

    new_essence = new_content[:500]
    if old_essence == new_essence:
        return False  # bez zmian

    # Aktualizuj essence i full_text_len
    conn.execute(
        "UPDATE doc_analysis SET essence = ?, full_text_len = ? WHERE idx = ?",
        (new_essence, len(new_content), idx)
    )
    # Usuń stary term_index
    conn.execute("DELETE FROM term_index WHERE idx = ?", (idx,))
    # Zbuduj nowy term_index z NL content
    ldr._update_term_index(conn, idx, new_content)
    return True


def run_reindex():
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    log = open(str(LOG_PATH), "w", encoding="utf-8")

    _log(log, "=== noema_reindex_json_essence START ===")
    _log(log, f"DB: {KNOWLEDGE_DB} ({KNOWLEDGE_DB.stat().st_size / 1024 / 1024:.1f} MB)")

    conn = sqlite3.connect(str(KNOWLEDGE_DB), timeout=60)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA cache_size=-32000")

    candidates = _candidates(conn)
    _log(log, f"Kandydaci do re-indeksacji (essence startsWith '{{'): {len(candidates)}")

    updated = 0
    skipped = 0
    errors = 0
    t0 = time.time()

    for i, (idx, filename, source_url) in enumerate(candidates):
        try:
            changed = _reindex_doc(conn, idx, filename, source_url, log)
            if changed:
                updated += 1
            else:
                skipped += 1
        except Exception as e:
            errors += 1
            _log(log, f"  EXCEPTION idx={idx} {filename}: {e}")

        if (i + 1) % BATCH_SIZE == 0:
            conn.commit()
            elapsed = time.time() - t0
            rate = (i + 1) / elapsed if elapsed > 0 else 0
            _log(log, f"  [{i+1}/{len(candidates)}] updated={updated} skip={skipped} err={errors} "
                      f"({rate:.1f} doc/s, ETA {(len(candidates)-i-1)/max(rate,0.01):.0f}s)")

    conn.commit()

    total_docs = conn.execute("SELECT COUNT(*) FROM doc_analysis").fetchone()[0]
    total_terms = conn.execute("SELECT COUNT(DISTINCT term) FROM term_index").fetchone()[0]
    total_entries = conn.execute("SELECT COUNT(*) FROM term_index").fetchone()[0]
    aff_count = conn.execute("SELECT COUNT(*) FROM semantic_affinity").fetchone()[0]
    still_raw = conn.execute(
        "SELECT COUNT(*) FROM doc_analysis WHERE essence LIKE '{%' OR essence LIKE ' {%'"
    ).fetchone()[0]

    conn.close()

    elapsed = time.time() - t0
    _log(log, "")
    _log(log, "=== DONE ===")
    _log(log, f"Czas: {elapsed:.0f}s | updated={updated} skip={skipped} err={errors}")
    _log(log, f"DB: {total_docs} docs | {total_terms} unikalnych terminów | "
              f"{total_entries} wpisów term_index | {aff_count} affinity pairs")
    _log(log, f"Nadal raw JSON essence: {still_raw}")
    log.close()


def main():
    pid = os.fork()
    if pid > 0:
        # Rodzic — wypisz info i wróć natychmiast (aktuator zdąży przed timeout)
        print(f"Re-index uruchomiony w tle, PID={pid}")
        print(f"Log: {LOG_PATH}")
        sys.exit(0)

    # Dziecko — odłącz od terminalu i uruchom re-indeksację
    os.setsid()
    # Przekieruj stdin/stdout/stderr do /dev/null (dziecko jest orphanem)
    devnull = os.open("/dev/null", os.O_RDWR)
    os.dup2(devnull, 0)
    os.dup2(devnull, 1)
    os.dup2(devnull, 2)
    os.close(devnull)

    run_reindex()


if __name__ == "__main__":
    main()
