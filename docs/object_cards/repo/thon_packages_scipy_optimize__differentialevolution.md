# _differentialevolution.py — .python_packages/scipy/optimize/_differentialevolution.py

## Tożsamość
- **id_karty:** `REPO-_DIFFERENTIALEVOLUTI-6CF6`
- **ścieżka:** `.python_packages/scipy/optimize/_differentialevolution.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.002`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/optimize/_differentialevolution.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.002 |
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
differential_evolution: The differential evolution global optimization algorithm

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** DifferentialEvolutionSolver, _ConstraintWrapper
- **funkcje:** `differential_evolution`, `mutation_func`, `init_population_lhs`, `init_population_qmc`, `init_population_random`, `init_population_array`, `x`, `convergence`, `converged`, `solve`, `_result`, `_calculate_population_energies`, `_promote_lowest_energy`, `_constraint_violation_fn`, `_calculate_population_feasibilities`, `_accept_trial`, `_scale_parameters`, `_unscale_parameters`, `_ensure_constraint`, `_mutate_custom`, `_mutate_many`, `_mutate`, `_best1`, `_rand1`, `_randtobest1`, `_currenttobest1`, `_best2`, `_rand2`, `_select_samples`, `violation`

## Opis
differential_evolution: The differential evolution global optimization algorithm
Added by Andrew Nelson 2014
