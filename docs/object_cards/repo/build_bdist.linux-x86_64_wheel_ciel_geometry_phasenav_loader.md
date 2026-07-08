# loader.py — build/bdist.linux-x86_64/wheel/ciel_geometry/phasenav/loader.py

## Tożsamość
- **id_karty:** `REPO-LOADER-27CD`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_geometry/phasenav/loader.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.431`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_geometry/phasenav/loader.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.431 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONSENT`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.382156`
- **R₃:** `0.389068`
- **R₆:** `0.420273`
- **R₉:** `0.412754`
- **potencjal_kappa:** `-0.014557`
- **masa_semantyczna:** `0.231183`
- **rodzaj_karty:** `0.291598`


## Rola
Load PhaseNav data — concept cards, phases, orbits, edges.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TeleusingData
- **funkcje:** `load_teleusing`, `_default_path`, `_lines`, `_load_jsonl_map`, `_load_orbit_map`

## Opis
Load PhaseNav data — concept cards, phases, orbits, edges.

Adapted from CIEL teleusing into NOEMA PhaseNav architecture.
Supports both JSONL files and direct in-memory loading.
