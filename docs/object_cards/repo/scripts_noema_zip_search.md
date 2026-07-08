# noema_zip_search.py — scripts/noema_zip_search.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_ZIP_SEARCH-CC16`
- **ścieżka:** `scripts/noema_zip_search.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `4.084`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_zip_search.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 4.084 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `UNRUH_DRIVE`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.695214`
- **R₃:** `0.356299`
- **R₆:** `0.471302`
- **R₉:** `0.535169`
- **potencjal_kappa:** `0.138014`
- **masa_semantyczna:** `0.204514`
- **rodzaj_karty:** `0.244249`


## Rola
PhaseNav ZIP Search — szukaj archiwów po operator fingerprint + surface state.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `load_index`, `surface_phasenav`, `operator_distribution`, `fingerprint_distribution`, `search_by_operator`, `search_by_fingerprint`, `search_surface_match`, `format_entry`, `main`

## Opis
PhaseNav ZIP Search — szukaj archiwów po operator fingerprint + surface state.

Usage:
    python scripts/noema_zip_search.py                           # surface → top 5 matching ZIPS
    python scripts/noema_zip_search.py --operator MEMORY         # ręczny operator
    python scripts/noema_zip_search.py --fingerprint HHHL        # ręczny fingerprint
    python scripts/noema_zip_search.py --list-o
