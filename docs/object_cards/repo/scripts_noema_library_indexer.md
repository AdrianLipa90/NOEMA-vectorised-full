# noema_library_indexer.py — scripts/noema_library_indexer.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_LIBRARY_INDEXE-4ABA`
- **ścieżka:** `scripts/noema_library_indexer.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `5.361`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_library_indexer.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 5.361 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `FORCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.552175`
- **R₃:** `0.435218`
- **R₆:** `0.571397`
- **R₉:** `0.579087`
- **potencjal_kappa:** `0.300939`
- **masa_semantyczna:** `0.016845`
- **rodzaj_karty:** `0.260112`


## Rola
Przepisuje library_index.npy (1284 koncepty) na zip_catalog/index.jsonl.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_normalize`, `_nearest_operator`, `main`

## Opis
Przepisuje library_index.npy (1284 koncepty) na zip_catalog/index.jsonl.

Dla każdego konceptu:
  1. Laduje 24D vector
  2. Znajduje najbliższy operator (cosine similarity)
  3. Zapisuje jako JSONL wpis zgodny z formatem PhaseNav daemona

Usage:
    .venv/bin/python3 scripts/noema_library_indexer.py
