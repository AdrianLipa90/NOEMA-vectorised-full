#!/usr/bin/env python3
"""Test parse_json() dla konkretnej karty i sprawdź czy reindex by ją zaktualizował."""
import sys, sqlite3
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from ciel_geometry.paths import P
import noema_library_loader as ldr

CARD = Path("/media/adrian/New Volume/CIEL_PROJECT_CANON/NOEMA/cards/noema_nonlocal_db/001_DOCTOR.noema.card.json")

print(f"=== parse_json() dla {CARD.name} ===")
result = ldr.parse_json(CARD)
print(f"Wynik ({len(result)} znaków):")
print(repr(result[:300]))
print()

# Sprawdź co jest w DB jako essence
conn = sqlite3.connect(str(P.DB.KNOWLEDGE), timeout=10)
row = conn.execute(
    "SELECT idx, essence, source_url FROM doc_analysis WHERE filename = ?",
    (CARD.name,)
).fetchone()
conn.close()

if row:
    idx, essence, url = row
    print(f"DB essence (pierwsze 200 znaków):")
    print(repr(essence[:200]))
    print(f"\nCzy parse_json() = raw JSON? {result.strip().startswith('{')}")
    print(f"Czy essence = raw JSON? {(essence or '').strip().startswith('{')}")
    new_essence = result[:500]
    print(f"\nCzy by zaktualizował? {(essence or '')[:500] != new_essence}")
else:
    print(f"Karty nie ma w DB!")

# Sprawdź też kilka innych kart z próbki
print("\n=== 5 innych kart (parse_json wynik) ===")
for fname in [
    "002_PIPELINE_SURFACE.noema.card.json",
    "003_HTRI_KURAMOTO_120.noema.card.json",
    "004_J_FUNCTIONAL.noema.card.json",
]:
    p = Path(CARD.parent / fname)
    if p.exists():
        r = ldr.parse_json(p)
        is_raw = r.strip().startswith('{')
        print(f"  {fname}: {'RAW JSON' if is_raw else 'NL'} ({len(r)} chars)")
        if not is_raw:
            print(f"    → {repr(r[:100])}")
