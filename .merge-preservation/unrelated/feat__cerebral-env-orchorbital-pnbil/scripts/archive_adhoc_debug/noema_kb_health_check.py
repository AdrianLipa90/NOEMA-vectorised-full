#!/usr/bin/env python3
"""Szybki health check KB + test knowledge search po card_mode fix."""
import sqlite3, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ciel_geometry.paths import P

conn = sqlite3.connect(f"file:{P.DB.KNOWLEDGE}?mode=ro", uri=True, timeout=15)

# 1. Podstawowe metryki
total_docs = conn.execute("SELECT COUNT(*) FROM doc_analysis").fetchone()[0]
raw_count = conn.execute("SELECT COUNT(*) FROM doc_analysis WHERE substr(essence,1,1)='{'").fetchone()[0]
nl_count = total_docs - raw_count
affinity_count = conn.execute("SELECT COUNT(*) FROM semantic_affinity").fetchone()[0]

print(f"=== KB HEALTH CHECK ===")
print(f"Docs: {total_docs} | NL essence: {nl_count} | Raw JSON: {raw_count}")
print(f"Affinity pairs: {affinity_count}")

# 2. Test query — szukaj NOEMA kart HTRI
t0 = time.time()
rows = conn.execute("""
    SELECT da.filename, da.essence, ti.tfidf
    FROM term_index ti
    JOIN doc_analysis da ON da.idx = ti.idx
    WHERE ti.term IN ('htri', 'kuramoto', 'holonomy')
    ORDER BY ti.tfidf DESC
    LIMIT 5
""").fetchall()
elapsed = time.time() - t0

print(f"\nTest query 'htri/kuramoto/holonomy' ({elapsed:.2f}s, {len(rows)} wyników):")
for fname, essence, tfidf in rows:
    is_nl = not essence.strip().startswith('{')
    print(f"  {'NL' if is_nl else 'RAW'} {Path(fname).name[:50]} tfidf={tfidf:.4f}")
    if is_nl:
        print(f"       → {essence[:100]!r}")

# 3. Próbka NOEMA kart — czy mają NL essence
sample = conn.execute("""
    SELECT filename, essence FROM doc_analysis
    WHERE filename LIKE '%.noema.card.json'
    LIMIT 5
""").fetchall()
print(f"\nPróbka .noema.card.json (5 kart):")
for fname, essence in sample:
    is_nl = not essence.strip().startswith('{')
    print(f"  {'NL ✓' if is_nl else 'RAW ✗'} {Path(fname).name[:50]}")
    if is_nl:
        print(f"       → {essence[:80]!r}")

conn.close()
