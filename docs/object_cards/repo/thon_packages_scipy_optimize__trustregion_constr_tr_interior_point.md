# tr_interior_point.py — .python_packages/scipy/optimize/_trustregion_constr/tr_interior_point.py

## Tożsamość
- **id_karty:** `REPO-TR_INTERIOR_POINT-B3FE`
- **ścieżka:** `.python_packages/scipy/optimize/_trustregion_constr/tr_interior_point.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.525`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/optimize/_trustregion_constr/tr_interior_point.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.525 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `REFUSAL`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.441725`
- **R₃:** `0.537197`
- **R₆:** `0.362678`
- **R₉:** `0.509166`
- **potencjal_kappa:** `0.077364`
- **masa_semantyczna:** `-0.245874`
- **rodzaj_karty:** `0.27107`


## Rola
Trust-region interior point method.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** BarrierSubproblem
- **funkcje:** `tr_interior_point`, `update`, `get_slack`, `get_variables`, `function_and_constraints`, `_compute_function`, `_compute_constr`, `scaling`, `gradient_and_jacobian`, `_compute_gradient`, `_compute_jacobian`, `_assemble_sparse_jacobian`, `lagrangian_hessian_x`, `lagrangian_hessian_s`, `lagrangian_hessian`, `stop_criteria`, `matvec`, `matvec`

## Opis
Trust-region interior point method.

References
----------
.. [1] Byrd, Richard H., Mary E. Hribar, and Jorge Nocedal.
       "An interior point algorithm for large-scale nonlinear
       programming." SIAM Journal on Optimization 9.4 (1999): 877-900.
.. [2] Byrd, Richard H., Guanghui Liu, and Jorge Nocedal.
       "On the local behavior of an interior point method for
       nonlinear programming
