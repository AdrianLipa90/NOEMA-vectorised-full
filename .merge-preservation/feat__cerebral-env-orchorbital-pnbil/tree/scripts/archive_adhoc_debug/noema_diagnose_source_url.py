#!/usr/bin/env python3
"""Sprawdź source_url dla kilku wpisów JSON z raw essence."""
import sys, sqlite3
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ciel_geometry.paths import P

KNOWLEDGE_DB = Path(P.DB.KNOWLEDGE)
conn = sqlite3.connect(str(KNOWLEDGE_DB), timeout=10)

rows = conn.execute(
    "SELECT idx, filename, source_url FROM doc_analysis "
    "WHERE (essence LIKE '{%' OR essence LIKE ' {%') "
    "AND filename LIKE '%.noema.card.json' LIMIT 10"
).fetchall()

print(f"Pierwsze 10 kart z raw JSON essence:")
for idx, filename, source_url in rows:
    su = source_url or "(NULL/empty)"
    exists = Path(source_url).exists() if source_url else False
    print(f"  idx={idx} exists_source_url={exists}")
    print(f"    filename:   {filename!r}")
    print(f"    source_url: {su!r}")

# Policz ile kart .noema.card.json ma istniejący source_url
rows2 = conn.execute(
    "SELECT source_url FROM doc_analysis "
    "WHERE (essence LIKE '{%' OR essence LIKE ' {%') "
    "AND filename LIKE '%.noema.card.json'"
).fetchall()
print(f"\nŁączna liczba kart noema.card.json z raw essence: {len(rows2)}")
existing = sum(1 for (su,) in rows2 if su and Path(su).exists())
print(f"Z istniejącym source_url: {existing}")
conn.close()
