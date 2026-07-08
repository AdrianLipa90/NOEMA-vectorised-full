# test_classes.py — .python_packages/numpy/polynomial/tests/test_classes.py

## Tożsamość
- **id_karty:** `REPO-TEST_CLASSES-7868`
- **ścieżka:** `.python_packages/numpy/polynomial/tests/test_classes.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.073`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numpy/polynomial/tests/test_classes.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.073 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ORDER`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.408132`
- **R₃:** `0.527143`
- **R₆:** `0.447287`
- **R₉:** `0.516074`
- **potencjal_kappa:** `0.213299`
- **masa_semantyczna:** `0.199346`
- **rodzaj_karty:** `0.279908`


## Rola
Test inter-conversion of different polynomial classes.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestInterpolate
- **funkcje:** `Poly`, `assert_poly_almost_equal`, `test_conversion`, `test_cast`, `test_identity`, `test_basis`, `test_fromroots`, `test_bad_conditioned_fit`, `test_fit`, `test_equal`, `test_not_equal`, `test_add`, `test_sub`, `test_mul`, `test_floordiv`, `test_truediv`, `test_mod`, `test_divmod`, `test_roots`, `test_degree`, `test_copy`, `test_integ`, `test_deriv`, `test_linspace`, `test_pow`, `test_call`, `test_call_with_list`, `test_cutdeg`, `test_truncate`, `test_trim`

## Opis
Test inter-conversion of different polynomial classes.

This tests the convert and cast methods of all the polynomial classes.
