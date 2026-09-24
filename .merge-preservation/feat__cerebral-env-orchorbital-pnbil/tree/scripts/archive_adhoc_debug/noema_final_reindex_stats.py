#!/usr/bin/env python3
"""Finalny raport po reindex card_mode — log + DB stats."""
import sqlite3, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ciel_geometry.paths import P

LOG = Path("/media/adrian/New Volume/CIEL_memories/logs/reindex_card_mode.log")

print("=== LOG ===")
if LOG.exists():
    lines = LOG.read_text(encoding="utf-8").splitlines()
    for l in lines:
        print(f"  {l}")
else:
    print("  BRAK LOGU")

print("\n=== DB STATS ===")
conn = sqlite3.connect(f"file:{P.DB.KNOWLEDGE}?mode=ro", uri=True, timeout=15)
conn.execute("PRAGMA journal_mode=WAL")

total_docs = conn.execute("SELECT COUNT(*) FROM doc_analysis").fetchone()[0]
total_terms = conn.execute("SELECT COUNT(DISTINCT term) FROM term_index").fetchone()[0]
term_rows = conn.execute("SELECT COUNT(*) FROM term_index").fetchone()[0]

# Szybkie sprawdzenie ile ma essence[0]='{'
raw_count = conn.execute(
    "SELECT COUNT(*) FROM doc_analysis WHERE substr(essence,1,1)='{'"
).fetchone()[0]

print(f"  Total docs: {total_docs}")
print(f"  Raw JSON essence (substr): {raw_count}")
print(f"  Unique terms: {total_terms}")
print(f"  term_index rows: {term_rows}")

conn.close()
