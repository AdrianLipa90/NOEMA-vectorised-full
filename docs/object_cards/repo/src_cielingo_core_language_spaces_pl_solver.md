# solver.py — src/cielingo_core/language_spaces/pl/solver.py

## Tożsamość
- **id_karty:** `REPO-SOLVER-3730`
- **ścieżka:** `src/cielingo_core/language_spaces/pl/solver.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.053`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/cielingo_core/language_spaces/pl/solver.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.053 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `FOLD`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.351212`
- **R₃:** `0.661831`
- **R₆:** `0.649218`
- **R₉:** `0.522246`
- **potencjal_kappa:** `-0.135067`
- **masa_semantyczna:** `-0.137397`
- **rodzaj_karty:** `0.29302`


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
