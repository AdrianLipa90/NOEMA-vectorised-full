#!/usr/bin/env python3
"""Sprawdź status procesu reindex i diagnozuj bottleneck."""
from __future__ import annotations
import os, sys, sqlite3
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ciel_geometry.paths import P

PID = 2087905
LOG = Path("/media/adrian/New Volume/CIEL_memories/logs/reindex_card_mode.log")

# 1. Czy proces żyje?
proc_file = Path(f"/proc/{PID}/status")
if proc_file.exists():
    status_lines = proc_file.read_text().splitlines()
    state_line = next((l for l in status_lines if l.startswith("State:")), "")
    print(f"PID {PID}: ŻYJE — {state_line}")
else:
    print(f"PID {PID}: MARTWY (nie ma /proc/{PID}/)")

# 2. Log
lines = LOG.read_text(encoding="utf-8").strip().splitlines() if LOG.exists() else []
print(f"Log: {len(lines)} linii")
for l in lines[-5:]:
    print(f"  {l}")

# 3. DB stats — szybkie zapytania bez LIKE na essence
conn = sqlite3.connect(str(P.DB.KNOWLEDGE), timeout=10)
conn.execute("PRAGMA journal_mode=WAL")

total_docs = conn.execute("SELECT COUNT(*) FROM doc_analysis").fetchone()[0]
total_terms = conn.execute("SELECT COUNT(DISTINCT term) FROM term_index").fetchone()[0]
print(f"\nDB: {total_docs} docs, {total_terms} unique terms")

# Sprawdź indeksy na term_index
idx_info = conn.execute("SELECT name, sql FROM sqlite_master WHERE type='index' AND tbl_name='term_index'").fetchall()
print(f"Indeksy term_index: {[r[0] for r in idx_info]}")

# Szybki sample — ile ma { jako pierwsze 10 chars (bez LIKE na całej essence)
sample = conn.execute(
    "SELECT COUNT(*) FROM doc_analysis WHERE substr(essence,1,1)='{'"
).fetchone()[0]
print(f"Kandydaci z essence[0]='{{': {sample}")

conn.close()
