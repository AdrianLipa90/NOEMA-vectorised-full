#!/usr/bin/env python3
"""Sprawdź schema i indeksy term_index bez blokowania DB."""
import sqlite3, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ciel_geometry.paths import P

# Połącz read-only przez URI — nie blokuje
conn = sqlite3.connect(f"file:{P.DB.KNOWLEDGE}?mode=ro", uri=True, timeout=5)

# Schema tabeli term_index
cols = conn.execute("PRAGMA table_info(term_index)").fetchall()
print("term_index columns:")
for c in cols:
    print(f"  {c}")

# Indeksy
idxs = conn.execute(
    "SELECT name, sql FROM sqlite_master WHERE type='index' AND tbl_name='term_index'"
).fetchall()
print(f"\nterm_index indexes ({len(idxs)}):")
for name, sql in idxs:
    print(f"  {name}: {sql}")

# Szybki count z read snapshot
try:
    n = conn.execute("SELECT COUNT(*) FROM term_index").fetchone()[0]
    print(f"\nterm_index rows: {n}")
except Exception as e:
    print(f"\nCOUNT error: {e}")

conn.close()
