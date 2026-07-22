#!/usr/bin/env python3
"""Probe: co jest w knowledge DB dla zapytań o NOEMA/PhaseNav."""
import sys, sqlite3
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from ciel_geometry.paths import P
from cielingo_core.bridge.knowledge_bridge import query as kb_query

db_path = str(P.DB.KNOWLEDGE)
print(f"Knowledge DB: {db_path}")

db = sqlite3.connect(db_path)
n_docs = db.execute("SELECT COUNT(*) FROM doc_analysis WHERE status='analyzed'").fetchone()[0]
print(f"Docs zaindeksowanych: {n_docs}\n")

# Próbka tematyczna
for theme in ("NOEMA", "PhaseNav", "CIELingo", "HTRI"):
    rows = db.execute(
        "SELECT filename, essence FROM doc_analysis WHERE filename LIKE ? AND status='analyzed' LIMIT 3",
        (f"%{theme}%",)
    ).fetchall()
    print(f"--- {theme} ({len(rows)} trafień) ---")
    for r in rows:
        print(f"  {r[0]}")
        print(f"  essence: {(r[1] or '')[:120]}\n")

db.close()

print("\n=== QUERY TEST ===")
for q in [
    "Czym jest system NOEMA i jak działa jego architektura?",
    "PhaseNav operator fazy",
    "CIELingo lingofizyka",
]:
    hits = kb_query(q, top_n=3)
    print(f"\nQ: {q}")
    for h in hits:
        print(f"  sim={h['similarity']:.3f} | {h['filename']}")
        print(f"  essence: {h['essence'][:100]}")
