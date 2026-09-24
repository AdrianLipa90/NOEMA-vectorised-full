#!/usr/bin/env python3
"""Sprawdź stan affinity w DB."""
import sys, sqlite3, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ciel_geometry.paths import P

t0 = time.time()
db = sqlite3.connect(str(P.DB.KNOWLEDGE), timeout=3)
try:
    n = db.execute("SELECT COUNT(*) FROM semantic_affinity").fetchone()[0]
    terms = db.execute("SELECT COUNT(DISTINCT term) FROM term_index").fetchone()[0]
    docs = db.execute("SELECT COUNT(*) FROM doc_analysis").fetchone()[0]
    db.close()
    elapsed = time.time() - t0
    print(f"OK ({elapsed:.2f}s)")
    print(f"Docs: {docs} | Unique terms: {terms}")
    print(f"Affinity pairs: {n}")
    import stat
    db_path = Path(str(P.DB.KNOWLEDGE))
    mtime = db_path.stat().st_mtime
    print(f"DB last modified: {time.ctime(mtime)}")
except sqlite3.OperationalError as e:
    print(f"DB locked/error: {e}")
