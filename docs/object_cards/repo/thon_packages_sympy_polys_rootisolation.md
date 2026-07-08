# rootisolation.py — .python_packages/sympy/polys/rootisolation.py

## Tożsamość
- **id_karty:** `REPO-ROOTISOLATION-4ED8`
- **ścieżka:** `.python_packages/sympy/polys/rootisolation.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.419`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/polys/rootisolation.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.419 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_POSSIBILITY`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.565748`
- **R₃:** `0.628966`
- **R₆:** `0.492583`
- **R₉:** `0.589778`
- **potencjal_kappa:** `0.024081`
- **masa_semantyczna:** `-0.294904`
- **rodzaj_karty:** `0.302592`


## Rola
Real and complex root isolation and refinement algorithms.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** RealInterval, ComplexInterval
- **funkcje:** `dup_sturm`, `dup_root_upper_bound`, `dup_root_lower_bound`, `dup_cauchy_upper_bound`, `dup_cauchy_lower_bound`, `dup_mignotte_sep_bound_squared`, `_mobius_from_interval`, `_mobius_to_interval`, `dup_step_refine_real_root`, `dup_inner_refine_real_root`, `dup_outer_refine_real_root`, `dup_refine_real_root`, `dup_inner_isolate_real_roots`, `_discard_if_outside_interval`, `dup_inner_isolate_positive_roots`, `dup_inner_isolate_negative_roots`, `_isolate_zero`, `dup_isolate_real_roots_sqf`, `dup_isolate_real_roots`, `dup_isolate_real_roots_list`, `_disjoint_p`, `_real_isolate_and_disjoin`, `dup_count_real_roots`, `_classify_point`, `_intervals_to_quadrants`, `_traverse_quadrants`, `_reverse_intervals`, `_winding_number`, `dup_count_complex_roots`, `_vertical_bisection`

## Opis
Real and complex root isolation and refinement algorithms.
