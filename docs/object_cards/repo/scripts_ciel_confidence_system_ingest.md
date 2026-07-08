# ingest.py — scripts/ciel_confidence_system/ingest.py

## Tożsamość
- **id_karty:** `REPO-INGEST-42B7`
- **ścieżka:** `scripts/ciel_confidence_system/ingest.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.063`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_confidence_system/ingest.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.063 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `ASSERTION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.563342`
- **R₃:** `0.601856`
- **R₆:** `0.54039`
- **R₉:** `0.584219`
- **potencjal_kappa:** `-0.098441`
- **masa_semantyczna:** `0.347732`
- **rodzaj_karty:** `0.261593`


## Rola
ciel_ingest.py — Data ingestion pipeline z confidence scoringiem.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `extract_fragments`, `guess_source_type`, `ingest_text`, `_update_term_index`, `main`

## Opis
ciel_ingest.py — Data ingestion pipeline z confidence scoringiem.

Każda informacja przechodzi przez:
  1. Parse — wyodrębnij znaczące fragmenty
  2. Score — oceń pewność (source, cross-ref, recency, consistency)
  3. Store — zapisz do Knowledge DB z confidence_score
  4. Flag — jeśli pewność < 60%, dodaj do uncertainty_log

Uruchom:
  python3 scripts/ciel_ingest.py --source academic_paper --url "
