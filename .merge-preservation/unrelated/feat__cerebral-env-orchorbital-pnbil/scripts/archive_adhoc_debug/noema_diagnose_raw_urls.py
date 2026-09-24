#!/usr/bin/env python3
"""Co dokładnie jest w source_url dla wpisów z raw JSON essence?"""
import sqlite3
from pathlib import Path
from collections import Counter

sys_path_insert = __import__("sys").path.insert
sys_path_insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ciel_geometry.paths import P

conn = sqlite3.connect(str(P.DB.KNOWLEDGE), timeout=10)

# Próbka 50 wpisów z raw JSON essence
rows = conn.execute("""
    SELECT filename, source_url, full_text_len
    FROM doc_analysis
    WHERE essence LIKE '{%'
    LIMIT 50
""").fetchall()

conn.close()

print(f"=== Próbka 50 wpisów z raw JSON essence ===\n")

prefixes = Counter()
exists_count = 0
not_exists_count = 0

for fname, url, flen in rows:
    p = Path(url) if url else None
    exists = p.exists() if p else False
    if exists:
        exists_count += 1
    else:
        not_exists_count += 1

    # Prefix do klasyfikacji
    if url is None:
        prefix = "NULL"
    elif url.startswith("/media/adrian/New Volume/NOEMA_LIBRARY"):
        prefix = "NOEMA_LIBRARY"
    elif url.startswith("/media/adrian/New Volume/CIEL_PROJECT_CANON"):
        prefix = "CIEL_PROJECT_CANON"
    elif url.startswith("/home/adrian/noema"):
        prefix = "/home/adrian/noema"
    elif url.startswith("/home/adrian"):
        prefix = "/home/adrian/other"
    elif url.startswith("/media"):
        prefix = "/media/other"
    elif url.startswith("/tmp"):
        prefix = "/tmp"
    else:
        prefix = "inne"
    prefixes[prefix] += 1

    # Pokaż pierwsze 15 z informacją o istnieniu
    if len([x for x in rows[:15] if x[0] == fname]) == 1:
        idx = next(i for i, r in enumerate(rows) if r[0] == fname)
        if idx < 15:
            status = "EXISTS" if exists else "BRAK"
            url_short = (url or "NULL")[:80]
            print(f"  [{status}] {fname[:40]} → {url_short}")

print(f"\n=== Prefixes (z 50 próbek) ===")
for prefix, cnt in prefixes.most_common():
    print(f"  {prefix}: {cnt}")

print(f"\n=== Istnienie pliku ===")
print(f"  EXISTS: {exists_count}/50")
print(f"  BRAK:   {not_exists_count}/50")

# Sprawdź jeden konkretny "brak" - czy można go znaleźć inaczej
brak_sample = [(f, u) for f, u, _ in rows if u and not Path(u).exists()][:3]
if brak_sample:
    print(f"\n=== Szukam w alternatywnych lokalizacjach ===")
    SEARCH_DIRS = [
        Path("/media/adrian/New Volume/NOEMA_LIBRARY"),
        Path("/media/adrian/New Volume/CIEL_PROJECT_CANON"),
        Path("/home/adrian/noema"),
    ]
    for fname, url in brak_sample:
        basename = Path(fname).name
        found_alt = []
        for d in SEARCH_DIRS:
            if d.exists():
                hits = list(d.rglob(basename))
                found_alt.extend(hits)
        print(f"  {basename}: " + (f"ZNALEZIONO w {[str(h) for h in found_alt[:2]]}" if found_alt else "nigdzie"))
