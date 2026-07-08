# test_linalg.py — .python_packages/numpy/linalg/tests/test_linalg.py

## Tożsamość
- **id_karty:** `REPO-TEST_LINALG-7B66`
- **ścieżka:** `.python_packages/numpy/linalg/tests/test_linalg.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.343`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numpy/linalg/tests/test_linalg.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.343 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SIMULATION_BOUNDARY`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.575665`
- **R₃:** `0.306554`
- **R₆:** `0.381064`
- **R₉:** `0.528951`
- **potencjal_kappa:** `-0.226686`
- **masa_semantyczna:** `-0.021063`
- **rodzaj_karty:** `0.269599`


## Rola
Test functions for linalg module

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** LinalgCase, LinalgTestCase, LinalgSquareTestCase, LinalgNonsquareTestCase, HermitianTestCase, LinalgGeneralizedSquareTestCase, LinalgGeneralizedNonsquareTestCase, HermitianGeneralizedTestCase, SolveCases, TestSolve, InvCases, TestInv, EigvalsCases, TestEigvals, EigCases, TestEig, SVDBaseTests, SVDCases, TestSVD, SVDHermitianCases
- **funkcje:** `consistent_subclass`, `assert_almost_equal`, `get_real_dtype`, `get_complex_dtype`, `get_rtol`, `apply_tag`, `_make_generalized_cases`, `_stride_comb_iter`, `_make_strided_cases`, `identity_like_generalized`, `test_pinv_rtol_arg`, `test_reduced_rank`, `test_byteorder_check`, `test_generalized_raise_multiloop`, `test_xerbla_override`, `test_sdot_bug_8577`, `test_unsupported_commontype`, `test_blas64_dot`, `test_blas64_geqrf_lwork_smoketest`, `test_diagonal`, `test_trace`, `test_cross`, `test_tensordot`, `test_matmul`, `test_matrix_transpose`, `test_matrix_norm`, `test_matrix_norm_empty`, `test_vector_norm`, `test_vector_norm_empty`, `check`

## Opis
Test functions for linalg module
