# __main__.py — src/cielingo/__main__.py

## Tożsamość
- **id_karty:** `REPO-__MAIN__-5CF8`
- **ścieżka:** `src/cielingo/__main__.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.890`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo/__main__.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.890 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ORDER`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.408132`
- **R₃:** `0.527143`
- **R₆:** `0.447287`
- **R₉:** `0.516074`
- **potencjal_kappa:** `0.213299`
- **masa_semantyczna:** `0.199346`
- **rodzaj_karty:** `0.279908`


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
