# test_trustregion_exact.py — .python_packages/scipy/optimize/tests/test_trustregion_exact.py

## Tożsamość
- **id_karty:** `REPO-TEST_TRUSTREGION_EXA-59A4`
- **ścieżka:** `.python_packages/scipy/optimize/tests/test_trustregion_exact.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.132`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/optimize/tests/test_trustregion_exact.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.132 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `IDENTITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.405566`
- **R₃:** `0.499333`
- **R₆:** `0.494094`
- **R₉:** `0.455981`
- **potencjal_kappa:** `0.08965`
- **masa_semantyczna:** `-0.024381`
- **rodzaj_karty:** `0.279273`


## Rola
Unit tests for trust-region iterative subproblem.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestEstimateSmallestSingularValue, TestSingularLeadingSubmatrix, TestIterativeSubproblem
- **funkcje:** `random_entry`, `test_for_ill_condiotioned_matrix`, `test_for_already_singular_leading_submatrix`, `test_for_simetric_indefinite_matrix`, `test_for_first_element_equal_to_zero`, `test_for_the_easy_case`, `test_for_the_hard_case`, `test_gh20244`, `test_for_interior_convergence`, `test_for_jac_equal_zero`, `test_for_jac_very_close_to_zero`, `test_for_random_entries`, `test_for_finite_number_of_iterations`

## Opis
Unit tests for trust-region iterative subproblem.
