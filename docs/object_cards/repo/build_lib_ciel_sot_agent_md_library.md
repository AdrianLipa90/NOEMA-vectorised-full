# md_library.py — build/lib/ciel_sot_agent/md_library.py

## Tożsamość
- **id_karty:** `REPO-MD_LIBRARY-05BB`
- **ścieżka:** `build/lib/ciel_sot_agent/md_library.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.062`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_sot_agent/md_library.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.062 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `PAUSE`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.508756`
- **R₃:** `0.557009`
- **R₆:** `0.421727`
- **R₉:** `0.55292`
- **potencjal_kappa:** `-0.020552`
- **masa_semantyczna:** `0.206252`
- **rodzaj_karty:** `0.260435`


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
