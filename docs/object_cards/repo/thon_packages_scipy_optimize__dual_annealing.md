# _dual_annealing.py — .python_packages/scipy/optimize/_dual_annealing.py

## Tożsamość
- **id_karty:** `REPO-_DUAL_ANNEALING-1587`
- **ścieżka:** `.python_packages/scipy/optimize/_dual_annealing.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.200`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/optimize/_dual_annealing.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.200 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `BOUNDARY`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.587016`
- **R₃:** `0.481937`
- **R₆:** `0.525424`
- **R₉:** `0.380572`
- **potencjal_kappa:** `-0.130804`
- **masa_semantyczna:** `0.12548`
- **rodzaj_karty:** `0.280526`


## Rola
A Dual Annealing global optimization algorithm

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** VisitingDistribution, EnergyState, StrategyChain, ObjectiveFunWrapper, LocalSearchWrapper
- **funkcje:** `dual_annealing`, `visiting`, `visit_fn`, `reset`, `update_best`, `update_current`, `accept_reject`, `run`, `local_search`, `fun`, `local_search`, `wrapped_jac`, `wrapped_hess`, `wrapped_hessp`

## Opis
A Dual Annealing global optimization algorithm
