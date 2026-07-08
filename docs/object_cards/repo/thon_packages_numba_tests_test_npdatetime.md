# test_npdatetime.py — .python_packages/numba/tests/test_npdatetime.py

## Tożsamość
- **id_karty:** `REPO-TEST_NPDATETIME-43E3`
- **ścieżka:** `.python_packages/numba/tests/test_npdatetime.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.051`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/tests/test_npdatetime.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.051 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `WARP_DRIFT`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.47403`
- **R₃:** `0.56672`
- **R₆:** `0.57902`
- **R₉:** `0.540967`
- **potencjal_kappa:** `0.057762`
- **masa_semantyczna:** `0.153958`
- **rodzaj_karty:** `0.289083`


## Rola
Test np.datetime64 and np.timedelta64 support.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestModuleHelpers, TestMiscCompiling, TestTimedeltaArithmetic, TestTimedeltaArithmeticNoPython, TestDatetimeArithmetic, TestDatetimeArithmeticNoPython, TestMetadataScalingFactor, TestDatetimeDeltaOps, TestDatetimeArrayOps, TestDatetimeTypeOps, TestDatetimeIssues
- **funkcje:** `value_unit`, `add_usecase`, `sub_usecase`, `mul_usecase`, `div_usecase`, `floordiv_usecase`, `eq_usecase`, `ne_usecase`, `lt_usecase`, `le_usecase`, `gt_usecase`, `ge_usecase`, `pos_usecase`, `neg_usecase`, `abs_usecase`, `hash_usecase`, `min_usecase`, `max_usecase`, `int_cast_usecase`, `make_add_constant`, `add_constant`, `test_can_cast_timedelta`, `test_timedelta_conversion`, `test_datetime_timedelta_scaling`, `test_combine_datetime_timedelta_units`, `test_same_kind`, `test_jit_explicit_signature`, `test_vectorize_explicit_signature`, `test_constant_datetime`, `test_constant_timedelta`

## Opis
Test np.datetime64 and np.timedelta64 support.
