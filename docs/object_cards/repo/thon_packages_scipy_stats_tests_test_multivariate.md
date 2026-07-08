# test_multivariate.py — .python_packages/scipy/stats/tests/test_multivariate.py

## Tożsamość
- **id_karty:** `REPO-TEST_MULTIVARIATE-82CC`
- **ścieżka:** `.python_packages/scipy/stats/tests/test_multivariate.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.515`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/stats/tests/test_multivariate.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.515 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ASSERTION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.563342`
- **R₃:** `0.601856`
- **R₆:** `0.54039`
- **R₉:** `0.584219`
- **potencjal_kappa:** `-0.098441`
- **masa_semantyczna:** `0.347732`
- **rodzaj_karty:** `0.261593`


## Rola
Test functions for multivariate normal, t, and related distributions.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestCovariance, MVNProblem, SingularMVNProblem, TestMultivariateNormal, TestMarginal, TestMatrixNormal, TestMatrixT, TestDirichlet, TestWishart, TestMultinomial, TestInvwishart, TestSpecialOrthoGroup, TestOrthoGroup, TestRandomCorrelation, TestUniformDirection, TestUnitaryGroup, TestMultivariateT, TestMultivariateHypergeom, TestRandomTable, TestVonMises_Fisher
- **funkcje:** `assert_close`, `_random_covariance`, `_sample_orthonormal_matrix`, `marginal_pdf`, `test_multivariate_normal_dimensions_mismatch`, `check_pickling`, `test_random_state_property`, `test_input_validation`, `test_factories`, `test_covariance`, `test_mvn_with_covariance`, `test_mvn_with_covariance_cdf`, `test_covariance_instantiation`, `test_gh9942`, `test_gh19197`, `g`, `generate_semigeneral`, `generate_constant`, `generate_halves`, `find_target`, `_univariate_term`, `univariate_func`, `plot_integrand`, `generate_semiinfinite`, `find_target`, `_univariate_term`, `univariate_func`, `plot_integrand`, `test_input_shape`, `test_scalar_values`

## Opis
Test functions for multivariate normal, t, and related distributions.
