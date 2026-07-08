# backfill.py — scripts/ciel_confidence_system/backfill.py

## Tożsamość
- **id_karty:** `REPO-BACKFILL-A968`
- **ścieżka:** `scripts/ciel_confidence_system/backfill.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `5.981`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_confidence_system/backfill.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 5.981 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `TRANSFORM`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.489274`
- **R₃:** `0.512237`
- **R₆:** `0.547669`
- **R₉:** `0.477906`
- **potencjal_kappa:** `0.124323`
- **masa_semantyczna:** `-0.167832`
- **rodzaj_karty:** `0.281825`


## Rola
ciel_backfill_confidence.py — Backfill confidence scores for existing docs.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `guess_source_type`, `backfill`, `main`

## Opis
ciel_backfill_confidence.py — Backfill confidence scores for existing docs.

Dla każdego dokumentu w doc_analysis który ma confidence=NULL lub confidence=0.5:
  1. Określ source_type na podstawie filename/essence
  2. Sprawdź cross-reference z innymi dokumentami
  3. Oblicz recency (brak daty → neutral 0.5)
  4. Zapisz confidence + wpis w confidence_scores

Uruchom:
    python3 scripts/ciel_backfi
