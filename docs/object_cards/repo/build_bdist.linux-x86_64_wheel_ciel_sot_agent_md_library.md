# md_library.py — build/bdist.linux-x86_64/wheel/ciel_sot_agent/md_library.py

## Tożsamość
- **id_karty:** `REPO-MD_LIBRARY-F3BD`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_sot_agent/md_library.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.526`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_sot_agent/md_library.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.526 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `DIFFERENCE`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.563622`
- **R₃:** `0.51399`
- **R₆:** `0.516024`
- **R₉:** `0.447233`
- **potencjal_kappa:** `-0.196591`
- **masa_semantyczna:** `-0.06476`
- **rodzaj_karty:** `0.313562`


## Rola
MD Library — System Informacji o Systemie (SIS).

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_categorize`, `_extract_title`, `_extract_tags`, `scan`, `build`

## Opis
MD Library — System Informacji o Systemie (SIS).

Skanuje wszystkie pliki .md w CIEL1 i buduje indeks z kategoryzacją,
tytułami i tagami. Wynik zapisuje do integration/registries/md_library_index.json.

Usage:
    python -m ciel_sot_agent.md_library
