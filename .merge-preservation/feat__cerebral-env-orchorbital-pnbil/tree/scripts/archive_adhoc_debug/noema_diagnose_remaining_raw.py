#!/usr/bin/env python3
"""Diagnozuj pozostałe wpisy z raw JSON essence."""
import sys, sqlite3, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ciel_geometry.paths import P

DB = Path(str(P.DB.KNOWLEDGE))
conn = sqlite3.connect(str(DB), timeout=8)

t0 = time.time()

total = conn.execute("SELECT COUNT(*) FROM doc_analysis").fetchone()[0]
raw = conn.execute("SELECT COUNT(*) FROM doc_analysis WHERE essence LIKE '{%'").fetchone()[0]
terms = conn.execute("SELECT COUNT(DISTINCT term) FROM term_index").fetchone()[0]
pairs = conn.execute("SELECT COUNT(*) FROM semantic_affinity").fetchone()[0]

print(f"DB OK ({time.time()-t0:.1f}s)")
print(f"Docs: {total} | Terms: {terms} | Pairs: {pairs}")
print(f"Raw JSON essence: {raw} ({100*raw/total:.1f}%)")

# Typy plików bez RANDOM - pierwsze 1000
rows = conn.execute("""
    SELECT source_url FROM doc_analysis WHERE essence LIKE '{%' LIMIT 1000
""").fetchall()

exts = {}
for (url,) in rows:
    if url is None:
        ext = "NULL"
    elif url.endswith(".json"):
        ext = ".json"
    elif url.endswith(".jsonl"):
        ext = ".jsonl"
    elif url.endswith(".md"):
        ext = ".md"
    elif url.endswith(".py"):
        ext = ".py"
    elif url.endswith(".yaml") or url.endswith(".yml"):
        ext = ".yaml"
    else:
        ext = "inne"
    exts[ext] = exts.get(ext, 0) + 1

print(f"\nTypy (z {len(rows)} próbek):")
for ext, cnt in sorted(exts.items(), key=lambda x: -x[1]):
    print(f"  {ext}: {cnt}")

conn.close()
