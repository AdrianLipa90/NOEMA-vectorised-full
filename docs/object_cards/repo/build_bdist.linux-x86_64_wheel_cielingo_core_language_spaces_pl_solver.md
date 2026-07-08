# solver.py — build/bdist.linux-x86_64/wheel/cielingo_core/language_spaces/pl/solver.py

## Tożsamość
- **id_karty:** `REPO-SOLVER-2479`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/cielingo_core/language_spaces/pl/solver.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.981`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/cielingo_core/language_spaces/pl/solver.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.981 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_OBLIGATION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.59271`
- **R₃:** `0.552945`
- **R₆:** `0.534582`
- **R₉:** `0.582078`
- **potencjal_kappa:** `0.23834`
- **masa_semantyczna:** `-0.091456`
- **rodzaj_karty:** `0.276031`


## Rola
Adapted Polish regional solver for CIELingo 0.5O.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** PolishRegionalSolver
- **funkcje:** `_pl_v02_diagnostics`, `segment`, `solve`

## Opis
Adapted Polish regional solver for CIELingo 0.5O.

Adds Polish v0.2 regional diagnostics:
- case_hint candidates, not full cases;
- role_candidate objects, not final semantic roles;
- negation-scope candidates, not complete logical scope;
- imperative/action-force candidates, not runtime authorization;
- source_required candidates, not SOURCE;
- canon_attempt/canon_block candidates, not canon;
- b
