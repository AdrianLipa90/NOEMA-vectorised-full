#!/usr/bin/env python3
"""NOEMA_LIBRARY Batch Loader — scan ~11k files into Knowledge DB.

Reads all text from NOEMA_LIBRARY, inserts into doc_analysis,
builds term_index (TF-IDF), and optionally rebuilds 36D embeddings.

Usage:
  python3 scripts/noema_library_loader.py                     # full load
  python3 scripts/noema_library_loader.py --dry-run           # preview only
  python3 scripts/noema_library_loader.py --skip-pdf          # skip PDFs
  python3 scripts/noema_library_loader.py --dir "Adrian_Lipa_Corpus"  # one dir
"""
from __future__ import annotations
import logging as _noema_quiet_logging
_NOEMA_QUIET_EXCEPT_LOGGER = _noema_quiet_logging.getLogger(__name__)


import argparse
import json
import math
import re
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

NOEMA_LIBRARY = Path("/media/adrian/New Volume1/NOEMA_LIBRARY")
KNOWLEDGE_DB = Path("/tmp/noema_knowledge.db")

MAX_CHUNK = 8000
MIN_CHUNK = 40

SKIP_DIRS = {"__pycache__", ".git", ".opencode", "node_modules", "raw_logs",
             "ciel_algo_repo/src"}
SKIP_SUFFIXES = {".pyc", ".npz", ".h5", ".pkl", ".lock", ".zip", ".png", ".jpg",
                 ".gif", ".ico", ".svg", ".woff", ".woff2", ".ttf", ".eot",
                 ".o", ".so", ".a", ".dll", ".dylib", ".aux", ".out", ".log",
                 ".blg", ".sha256", ".pyc"}

FILE_PARSERS: dict[str, str] = {
    ".md": "text", ".txt": "text", ".rst": "text", ".tex": "text",
    ".json": "json", ".jsonl": "jsonl",
    ".yaml": "yaml", ".yml": "yaml",
    ".csv": "text", ".tsv": "text",
    ".py": "text", ".sh": "text", ".js": "text", ".html": "text", ".css": "text",
    ".c": "text", ".h": "text", ".cpp": "text", ".hpp": "text",
    ".rs": "text", ".go": "text", ".java": "text",
    ".cfg": "text", ".conf": "text", ".ini": "text", ".toml": "text",
    ".xml": "text", ".svg": "text",
    ".db": "db", ".sqlite": "db", ".sqlite3": "db",
}

_counters = {"scanned": 0, "text": 0, "json": 0, "jsonl": 0, "yaml": 0,
             "db": 0, "skipped": 0, "errors": 0, "pdf_converted": 0,
             "existing": 0, "inserted": 0}


def parse_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        try:
            return path.read_text(encoding="latin-1", errors="replace")
        except Exception as e:
            _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_library_loader.py:60 quiet except scope=parse_text reason=raise")
            raise


def parse_json(path: Path) -> str:
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return ""
    if isinstance(data, str):
        return data
    return json.dumps(data, ensure_ascii=False, indent=1)


def parse_jsonl(path: Path) -> str:
    parts = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            item = json.loads(line)
        except Exception:
            parts.append(line)
            continue
        if isinstance(item, dict):
            text = (item.get("text") or item.get("content") or item.get("sense")
                    or item.get("description") or item.get("name") or str(item))
        else:
            text = str(item)
        parts.append(str(text).strip())
    return "\n\n".join(p for p in parts if len(p) >= MIN_CHUNK)


def parse_yaml(path: Path) -> str:
    try:
        import yaml
        data = yaml.safe_load(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return parse_text(path)
    if data is None:
        return ""
    if isinstance(data, str):
        return data
    return json.dumps(data, ensure_ascii=False, indent=2)


def parse_pdf(path: Path) -> str:
    try:
        result = subprocess.run(
            ["pdftotext", str(path), "-", "-l", "10", "-nopgbrk"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()[:8000]
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_library_loader.py:109 quiet except scope=parse_pdf reason=pass")
    return ""


def parse_db(path: Path) -> str:
    parts = []
    try:
        conn = sqlite3.connect(str(path), timeout=3)
        tables = [r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()]
        for table in tables[:5]:
            try:
                cols_info = conn.execute(f"PRAGMA table_info({table})").fetchall()
                text_cols = [c[1] for c in cols_info if "text" in c[2].lower() or "char" in c[2].lower()]
                if not text_cols:
                    continue
                rows = conn.execute(
                    f"SELECT {','.join(text_cols)} FROM {table} LIMIT 100"
                ).fetchall()
                for row in rows:
                    text = " | ".join(str(v) for v in row if v and len(str(v)) > 10)
                    if len(text) >= MIN_CHUNK:
                        parts.append(text[:500])
            except Exception:
                _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_library_loader.py:131 quiet except scope=parse_db reason=continue")
                continue
        conn.close()
    except Exception:
        _NOEMA_QUIET_EXCEPT_LOGGER.exception("scripts/noema_library_loader.py:136 quiet except scope=parse_db reason=pass")
    return "\n\n".join(parts)


def guess_themes(path: Path) -> list[str]:
    themes = []
    parts = path.relative_to(NOEMA_LIBRARY).parts if NOEMA_LIBRARY in path.parents else path.parts
    for p in parts[:-1]:
        p = re.sub(r'^\d+_', '', p)
        p = p.replace('_', ' ').replace('-', ' ').title()
        themes.append(p)
    fname = parts[-1].replace('_', ' ').replace('-', ' ')
    themes.append(fname.rsplit('.', 1)[0][:80])
    return list(dict.fromkeys(themes))


def ensure_schema(conn: sqlite3.Connection):
    existing = [r[1] for r in conn.execute("PRAGMA table_info(doc_analysis)").fetchall()]
    needed = [
        ("anchors", "TEXT"),
        ("hunch", "TEXT"),
        ("full_text_len", "INTEGER DEFAULT 0"),
        ("confidence", "REAL DEFAULT 0.5"),
        ("source_type", "TEXT DEFAULT 'library_scan'"),
        ("source_url", "TEXT DEFAULT ''"),
        ("source_reliability", "REAL DEFAULT 0.5"),
        ("cross_ref_count", "INTEGER DEFAULT 0"),
        ("recency_days", "INTEGER DEFAULT 0"),
        ("consistency_score", "REAL DEFAULT 0.5"),
        ("is_uncertain", "INTEGER DEFAULT 0"),
        ("ingested_at", "TEXT"),
    ]
    for col, col_type in needed:
        if col not in existing:
            conn.execute(f"ALTER TABLE doc_analysis ADD COLUMN {col} {col_type}")
            print(f"  schema: added column {col}")

    existing_terms = [r[1] for r in conn.execute("PRAGMA table_info(term_index)").fetchall()]
    if "id" not in existing_terms:
        print("  schema: term_index exists but may need rebuild")


def insert_doc(conn: sqlite3.Connection, filename: str, content: str,
               themes: str, source_type: str, source_url: str) -> int:
    existing = conn.execute(
        "SELECT idx FROM doc_analysis WHERE filename = ?", (filename,)
    ).fetchone()
    if existing:
        _counters["existing"] += 1
        return existing[0]

    cur = conn.execute("SELECT COALESCE(MAX(idx), -1) FROM doc_analysis")
    next_idx = cur.fetchone()[0] + 1

    now_iso = datetime.now(timezone.utc).isoformat()
    essence = content[:500] if content else ""
    conn.execute("""
        INSERT INTO doc_analysis
            (idx, filename, themes, affect, anchors, essence, hunch,
             full_text_len, status, confidence, source_type, source_url,
             source_reliability, cross_ref_count, recency_days,
             consistency_score, is_uncertain, ingested_at)
        VALUES (?, ?, ?, '', '', ?, '', ?, 'ingested', 0.5, ?, ?, 0.5, 0, 0, 0.5, 0, ?)
    """, (next_idx, filename, themes, essence, len(content),
          source_type, source_url, now_iso))

    _update_term_index(conn, next_idx, content)
    _counters["inserted"] += 1
    return next_idx


def _update_term_index(conn: sqlite3.Connection, doc_idx: int, content: str):
    STOP_WORDS = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
                  'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
                  'can', 'could', 'shall', 'should', 'may', 'might', 'must',
                  'i', 'you', 'he', 'she', 'it', 'we', 'they', 'this', 'that',
                  'these', 'those', 'of', 'in', 'on', 'at', 'to', 'for', 'with',
                  'by', 'from', 'as', 'into', 'through', 'during', 'before',
                  'after', 'above', 'below', 'between', 'out', 'off', 'over',
                  'under', 'again', 'further', 'then', 'once', 'here', 'there',
                  'when', 'where', 'why', 'how', 'all', 'each', 'every', 'both',
                  'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
                  'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
                  'and', 'but', 'or', 'about', 'up', 'down', 'also',
                  'just', 'because', 'into', 'over', 'still', 'while'}

    words = re.findall(r'\w{2,}', content.lower())
    word_counts: dict[str, int] = {}
    for w in words:
        if w not in STOP_WORDS:
            word_counts[w] = word_counts.get(w, 0) + 1

    total_docs = conn.execute("SELECT COUNT(*) FROM doc_analysis").fetchone()[0]

    for term, count in word_counts.items():
        tf = count / max(len(words), 0.1)
        existing = conn.execute(
            "SELECT COUNT(DISTINCT idx) FROM term_index WHERE term = ?",
            (term,)
        ).fetchone()[0]
        df = existing + 1
        idf = max(0.0, math.log((total_docs + 1) / df)) if df > 0 else 0.0
        try:
            conn.execute(
                "INSERT INTO term_index (term, idx, tf, idf, tfidf) VALUES (?, ?, ?, ?, ?)",
                (term, doc_idx, tf, idf, tf * idf)
            )
        except sqlite3.IntegrityError:
            pass


def load_file(path: Path, conn: sqlite3.Connection, skip_pdf: bool = False) -> bool:
    _counters["scanned"] += 1
    suffix = path.suffix.lower()

    if suffix in SKIP_SUFFIXES:
        _counters["skipped"] += 1
        return False
    if skip_pdf and suffix == ".pdf":
        _counters["skipped"] += 1
        return False

    parser_type = FILE_PARSERS.get(suffix, "text")
    if suffix == ".pdf":
        content = parse_pdf(path)
        if content:
            _counters["pdf_converted"] += 1
        else:
            _counters["errors"] += 1
            return False
    elif parser_type == "json":
        content = parse_json(path)
    elif parser_type == "jsonl":
        content = parse_jsonl(path)
    elif parser_type == "yaml":
        content = parse_yaml(path)
    elif parser_type == "db":
        content = parse_db(path)
    elif parser_type == "text":
        content = parse_text(path)
    else:
        content = parse_text(path)

    if not content or len(content.strip()) < MIN_CHUNK:
        _counters["skipped"] += 1
        return False

    # Shorten content for storage (max 5000 chars for essence)
    themes = guess_themes(path)
    themes_json = json.dumps(themes, ensure_ascii=False)
    source_type = "pdf" if suffix == ".pdf" else "library_scan"

    content = content[:MAX_CHUNK] if len(content) > MAX_CHUNK else content
    rel_path = str(path.relative_to(NOEMA_LIBRARY)) if NOEMA_LIBRARY in path.parents else str(path)
    insert_doc(conn, rel_path, content, themes_json, source_type, str(path))
    _counters[parser_type] = _counters.get(parser_type, 0) + 1
    return True


def collect_files(directory: Path) -> list[Path]:
    files = []
    for p in sorted(directory.rglob("*")):
        if any(skip in str(p) for skip in SKIP_DIRS):
            continue
        if p.suffix.lower() in SKIP_SUFFIXES:
            continue
        if p.is_file():
            files.append(p)
    return files


def scan_directory(directory: Path, conn: sqlite3.Connection,
                   skip_pdf: bool, label: str, batch_size: int = 500):
    files = collect_files(directory)
    total = len(files)
    print(f"\n{'='*60}")
    print(f"  {label}: {total} files")
    print(f"{'='*60}")

    t0 = time.time()
    batch_conn = sqlite3.connect(str(KNOWLEDGE_DB), timeout=10)
    batch_conn.execute("PRAGMA journal_mode=WAL")
    batch_conn.execute("PRAGMA synchronous=OFF")
    batch_conn.execute("PRAGMA cache_size=-64000")

    processed = 0
    for fpath in files:
        load_file(fpath, batch_conn, skip_pdf)
        processed += 1

        if processed % batch_size == 0:
            batch_conn.commit()
            elapsed = time.time() - t0
            rate = processed / elapsed if elapsed > 0 else 0
            print(f"  {processed}/{total} ({rate:.0f} files/s, "
                  f"{_counters['inserted']} inserted, "
                  f"{_counters['existing']} existing, "
                  f"{_counters['errors']} errors)")

    batch_conn.commit()
    elapsed = time.time() - t0
    print(f"  Done: {processed} files in {elapsed:.0f}s "
          f"({processed/elapsed:.1f} files/s)")
    batch_conn.close()


def show_stats(conn: sqlite3.Connection):
    doc_count = conn.execute("SELECT COUNT(*) FROM doc_analysis").fetchone()[0]
    term_count = conn.execute("SELECT COUNT(DISTINCT term) FROM term_index").fetchone()[0]
    entry_count = conn.execute("SELECT COUNT(*) FROM term_index").fetchone()[0]

    print(f"\n{'='*60}")
    print(f"  KNOWLEDGE DB STATS")
    print(f"{'='*60}")
    print(f"  Documents:   {doc_count}")
    print(f"  Unique terms: {term_count}")
    print(f"  Term entries: {entry_count}")
    print(f"  DB size:      {KNOWLEDGE_DB.stat().st_size / 1024:.0f} KB")
    print(f"{'='*60}")
    print(f"  Scan summary:")
    for k, v in sorted(_counters.items()):
        if v > 0:
            print(f"    {k}: {v}")


def main() -> int:
    ap = argparse.ArgumentParser(description="NOEMA_LIBRARY Batch Loader")
    ap.add_argument("--dry-run", action="store_true", help="Preview only")
    ap.add_argument("--skip-pdf", action="store_true", help="Skip PDF files")
    ap.add_argument("--dir", type=str, default=None,
                    help="Scan only one subdirectory (e.g. 'Adrian_Lipa_Corpus')")
    ap.add_argument("--stats", action="store_true", help="Show DB stats and exit")
    args = ap.parse_args()

    if args.stats:
        conn = sqlite3.connect(str(KNOWLEDGE_DB))
        show_stats(conn)
        conn.close()
        return 0

    if not NOEMA_LIBRARY.exists():
        print(f"ERROR: NOEMA_LIBRARY not found at {NOEMA_LIBRARY}")
        return 1

    print(f"NOEMA_LIBRARY: {NOEMA_LIBRARY}")
    print(f"Knowledge DB:  {KNOWLEDGE_DB}")
    if args.dry_run:
        print("DRY RUN — no changes will be made")

    # Migrate schema
    conn = sqlite3.connect(str(KNOWLEDGE_DB), timeout=5)
    ensure_schema(conn)
    conn.commit()
    conn.close()

    before = sqlite3.connect(str(KNOWLEDGE_DB))
    before_count = before.execute("SELECT COUNT(*) FROM doc_analysis").fetchone()[0]
    before.close()

    if args.dir:
        target = NOEMA_LIBRARY / args.dir
        if not target.exists():
            print(f"ERROR: {target} not found")
            return 1
        conn = sqlite3.connect(str(KNOWLEDGE_DB), timeout=10)
        scan_directory(target, conn, args.skip_pdf, f"Scanning {args.dir}")
        conn.close()
    else:
        dirs = sorted([d for d in NOEMA_LIBRARY.iterdir() if d.is_dir()])
        for d in dirs:
            if d.name in ("CONFIG", "LOGS", "PDF", "PHASE_INDEX", "DOCUMENTS", "MEMORIES",
                          "memory_palace", "models", "site", "CARDS", "INDEX"):
                print(f"\n  SKIP {d.name} (metadata/temp directory)")
                continue
            conn = sqlite3.connect(str(KNOWLEDGE_DB), timeout=10)
            scan_directory(d, conn, args.skip_pdf, f"Scanning {d.name}")
            conn.close()

    conn = sqlite3.connect(str(KNOWLEDGE_DB))
    after_count = conn.execute("SELECT COUNT(*) FROM doc_analysis").fetchone()[0]
    show_stats(conn)
    conn.close()

    print(f"\nNew docs loaded: {after_count - before_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
