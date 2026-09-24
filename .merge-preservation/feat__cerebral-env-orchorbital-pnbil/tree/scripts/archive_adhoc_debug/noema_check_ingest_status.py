#!/usr/bin/env python3
"""Sprawdź status ingest_object_cards i stan DB."""
import sys, sqlite3, time, os
from pathlib import Path

LOG = Path("/media/adrian/New Volume/CIEL_memories/logs/ingest_object_cards.log")
AFFINITY_LOG = Path("/media/adrian/New Volume/CIEL_memories/logs/build_affinity.log")

print("=== STATUS SPRAWDZENIA ===")

# Sprawdź log
if LOG.exists():
    content = LOG.read_text(encoding="utf-8", errors="replace")
    lines = content.strip().splitlines()
    print(f"\nLog ingest_object_cards ({len(lines)} linii):")
    for l in lines:
        print(f"  {l}")
else:
    print("LOG NIE ISTNIEJE")

# Sprawdź DB z krótkim timeout
DB = Path("/media/adrian/New Volume/CIEL_memories/state/noema_knowledge.db")
try:
    conn = sqlite3.connect(str(DB), timeout=5)
    docs = conn.execute("SELECT COUNT(*) FROM doc_analysis").fetchone()[0]
    terms = conn.execute("SELECT COUNT(DISTINCT term) FROM term_index").fetchone()[0]
    pairs = conn.execute("SELECT COUNT(*) FROM semantic_affinity").fetchone()[0]
    conn.close()
    print(f"\nDB (nie zablokowana):")
    print(f"  Docs: {docs} | Unique terms: {terms} | Affinity pairs: {pairs}")
    mtime = DB.stat().st_mtime
    print(f"  DB mtime: {time.ctime(mtime)}")
except sqlite3.OperationalError as e:
    print(f"\nDB zablokowana: {e}")
