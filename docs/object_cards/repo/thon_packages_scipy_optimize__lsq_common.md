# common.py — .python_packages/scipy/optimize/_lsq/common.py

## Tożsamość
- **id_karty:** `REPO-COMMON-6938`
- **ścieżka:** `.python_packages/scipy/optimize/_lsq/common.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.007`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/optimize/_lsq/common.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.007 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RETURN`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.642878`
- **R₃:** `0.503912`
- **R₆:** `0.555289`
- **R₉:** `0.707983`
- **potencjal_kappa:** `-0.270999`
- **masa_semantyczna:** `-0.074142`
- **rodzaj_karty:** `0.291714`


## Rola
Functions used by least-squares algorithms.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `intersect_trust_region`, `solve_lsq_trust_region`, `solve_trust_region_2d`, `update_tr_radius`, `build_quadratic_1d`, `minimize_quadratic_1d`, `evaluate_quadratic`, `in_bounds`, `step_size_to_bound`, `find_active_constraints`, `make_strictly_feasible`, `CL_scaling_vector`, `reflective_transformation`, `print_header_nonlinear`, `print_iteration_nonlinear`, `print_header_linear`, `print_iteration_linear`, `compute_grad`, `compute_jac_scale`, `left_multiplied_operator`, `right_multiplied_operator`, `regularized_lsq_operator`, `right_multiply`, `left_multiply`, `check_termination`, `scale_for_robust_loss_function`, `phi_and_derivative`, `matvec`, `matmat`, `rmatvec`

## Opis
Functions used by least-squares algorithms.
