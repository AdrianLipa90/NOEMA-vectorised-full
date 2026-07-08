# test_hyp2f1.py — .python_packages/scipy/special/tests/test_hyp2f1.py

## Tożsamość
- **id_karty:** `REPO-TEST_HYP2F1-6A38`
- **ścieżka:** `.python_packages/scipy/special/tests/test_hyp2f1.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.040`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/special/tests/test_hyp2f1.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.040 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `NEGATION`
- **odcisk_harmoniczny:** `LHLL`
- **R₁:** `0.425094`
- **R₃:** `0.614676`
- **R₆:** `0.450577`
- **R₉:** `0.387679`
- **potencjal_kappa:** `0.085998`
- **masa_semantyczna:** `-0.143065`
- **rodzaj_karty:** `0.271614`


## Rola
Tests for hyp2f1 for complex values.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Hyp2f1TestCase, TestHyp2f1, TestHyp2f1ExtremeInputs
- **funkcje:** `mp_hyp2f1`, `test_c_non_positive_int`, `test_unital_argument`, `test_special_case_z_near_minus_1`, `test_a_b_negative_int`, `test_a_b_neg_int_after_euler_hypergeometric_transformation`, `test_region1`, `test_region2`, `test_region3`, `test_region4`, `test_region5`, `test_region6`, `test_miscellaneous`, `test_test_hyp2f1`, `_get_test_parameters`, `test_inf_a_b`, `test_large_a_b`

## Opis
Tests for hyp2f1 for complex values.

Author: Albert Steppi, with credit to Adam Kullberg (FormerPhycisist) for
the implementation of mp_hyp2f1 below, which modifies mpmath's hyp2f1 to
return the same branch as scipy's on the standard branch cut.
