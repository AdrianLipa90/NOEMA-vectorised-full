#!/usr/bin/env python3
"""Diagnostyka: ile kart JSON jest w KB, ile ma surowe JSON, ile ma NL po naprawie."""
import sys, json, re, sqlite3
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ciel_geometry.paths import P

KNOWLEDGE_DB = Path(P.DB.KNOWLEDGE)
MIN_CHUNK = 40

print(f"DB: {KNOWLEDGE_DB}")
print(f"DB size: {KNOWLEDGE_DB.stat().st_size / 1024 / 1024:.1f} MB")

conn = sqlite3.connect(str(KNOWLEDGE_DB))
cur = conn.cursor()

# Ile dokumentow ogółem
cur.execute("SELECT COUNT(*) FROM doc_analysis")
total = cur.fetchone()[0]
print(f"\nDokumenty ogółem: {total}")

# Ile to karty JSON
cur.execute("SELECT COUNT(*) FROM doc_analysis WHERE filename LIKE '%.noema.card.json'")
card_json = cur.fetchone()[0]
print(f"Kart .noema.card.json: {card_json}")

# Ile to inne .json
cur.execute("SELECT COUNT(*) FROM doc_analysis WHERE filename LIKE '%.json' AND filename NOT LIKE '%.noema.card.json'")
other_json = cur.fetchone()[0]
print(f"Inne .json: {other_json}")

# Ile NL (nie-json)
print(f"Tekstowe/inne: {total - card_json - other_json}")

# Sprawdz terminy dla kilku kart
cur.execute("""
    SELECT d.filename, COUNT(t.term) as term_count
    FROM doc_analysis d
    JOIN term_index t ON d.idx = t.idx
    WHERE d.filename LIKE '%.noema.card.json'
    GROUP BY d.idx
    ORDER BY term_count DESC
    LIMIT 5
""")
print(f"\nTop 5 kart z największą liczbą terminów:")
for row in cur.fetchall():
    print(f"  {row[1]:6d} terminów: {Path(row[0]).name}")

# Porównaj: ile terminów ma typowy plik NL vs karta JSON
cur.execute("""
    SELECT AVG(tc) FROM (
        SELECT COUNT(t.term) as tc FROM doc_analysis d
        JOIN term_index t ON d.idx = t.idx
        WHERE d.filename LIKE '%.md'
        GROUP BY d.idx LIMIT 100
    )
""")
md_avg = cur.fetchone()[0]
cur.execute("""
    SELECT AVG(tc) FROM (
        SELECT COUNT(t.term) as tc FROM doc_analysis d
        JOIN term_index t ON d.idx = t.idx
        WHERE d.filename LIKE '%.noema.card.json'
        GROUP BY d.idx LIMIT 100
    )
""")
card_avg = cur.fetchone()[0]
print(f"\nŚrednia liczba terminów/doc:")
print(f"  .md files: {md_avg:.0f}" if md_avg else "  .md: brak")
print(f"  .noema.card.json: {card_avg:.0f}" if card_avg else "  karty: brak")

# Próbka: wyciągnij tekst (essence) z kilku kart
cur.execute("SELECT idx, filename, essence FROM doc_analysis WHERE filename LIKE '%.noema.card.json' LIMIT 3")
print(f"\nEssence 3 losowych kart:")
for row in cur.fetchall():
    print(f"  [{row[0]}] {Path(row[1]).name}: {(row[2] or '')[:120]!r}")

conn.close()

# Test parse_json z naprawką
sys.path.insert(0, str(Path(__file__).resolve().parent))
import noema_library_loader as ldr

sample = Path("/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/cards/base/noema_nonlocal_db/010_PROJECT.noema.card.json")
if sample.exists():
    old_text = json.dumps(json.loads(sample.read_text()), ensure_ascii=False, indent=1)
    new_text = ldr.parse_json(sample)
    print(f"\nPorównanie parse_json dla 010_PROJECT.noema.card.json:")
    print(f"  Stara metoda (raw JSON): {len(old_text)} znaków, {len(re.findall(r'[a-ząćęłńóśźż]{{3,}}', old_text.lower()))} tokenów")
    print(f"  Nowa metoda (NL extract): {len(new_text)} znaków, {len(re.findall(r'[a-ząćęłńóśźż]{{3,}}', new_text.lower()))} tokenów")
    print(f"  Próbka nowego tekstu: {new_text[:200]!r}")
