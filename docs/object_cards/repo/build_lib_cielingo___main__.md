# __main__.py — build/lib/cielingo/__main__.py

## Tożsamość
- **id_karty:** `REPO-__MAIN__-9A8B`
- **ścieżka:** `build/lib/cielingo/__main__.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.710`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/cielingo/__main__.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.710 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `NEGATION`
- **odcisk_harmoniczny:** `LHLL`
- **R₁:** `0.425094`
- **R₃:** `0.614676`
- **R₆:** `0.450577`
- **R₉:** `0.387679`
- **potencjal_kappa:** `0.085998`
- **masa_semantyczna:** `-0.143065`
- **rodzaj_karty:** `0.271614`


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
