# test_extras.py — .python_packages/numpy/ma/tests/test_extras.py

## Tożsamość
- **id_karty:** `REPO-TEST_EXTRAS-6F41`
- **ścieżka:** `.python_packages/numpy/ma/tests/test_extras.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.704`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numpy/ma/tests/test_extras.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.704 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONSENT`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.382156`
- **R₃:** `0.389068`
- **R₆:** `0.420273`
- **R₉:** `0.412754`
- **potencjal_kappa:** `-0.014557`
- **masa_semantyczna:** `0.231183`
- **rodzaj_karty:** `0.291598`


## Rola
Tests suite for MaskedArray.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestGeneric, TestAverage, TestConcatenator, TestNotMasked, TestCompressFunctions, TestApplyAlongAxis, TestApplyOverAxes, TestMedian, TestCov, TestCorrcoef, TestPolynomial, TestArraySetOps, TestShapeBase, TestNDEnumerate, TestStack
- **funkcje:** `test_masked_all`, `test_masked_all_with_object_nested`, `test_masked_all_with_object`, `test_masked_all_like`, `check_clump`, `test_clump_masked`, `test_clump_unmasked`, `test_flatnotmasked_contiguous`, `test_testAverage1`, `test_testAverage2`, `test_testAverage3`, `test_testAverage4`, `test_weight_and_input_dims_different`, `test_onintegers_with_mask`, `test_complex`, `test_basic_keepdims`, `test_masked_weights`, `test_1d`, `test_2d`, `test_masked_constant`, `test_edges`, `test_contiguous`, `test_compress_nd`, `test_compress_rowcols`, `test_mask_rowcols`, `test_mask_row_cols_axis_deprecation`, `test_dot`, `test_dot_returns_maskedarray`, `test_dot_out`, `test_3d`

## Opis
Tests suite for MaskedArray.
Adapted from the original test_ma by Pierre Gerard-Marchant

:author: Pierre Gerard-Marchant
:contact: pierregm_at_uga_dot_edu
