# __main__.py — build/bdist.linux-x86_64/wheel/cielingo/__main__.py

## Tożsamość
- **id_karty:** `REPO-__MAIN__-7C57`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo/__main__.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.053`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo/__main__.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.053 |
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
CIELingo CLI — entry point for `cielingo` command.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_print_json`, `_cmd_info`, `_cmd_seeds`, `_cmd_modalities`, `_cmd_bus`, `main`

## Opis
CIELingo CLI — entry point for `cielingo` command.

Usage:
    cielingo info              — package version + module list
    cielingo seeds [--json]    — load infinitive seeds
    cielingo modalities [--json] — load modality seeds
    cielingo bus               — phase bus report
