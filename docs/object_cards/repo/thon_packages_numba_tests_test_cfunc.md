# test_cfunc.py — .python_packages/numba/tests/test_cfunc.py

## Tożsamość
- **id_karty:** `REPO-TEST_CFUNC-6A9E`
- **ścieżka:** `.python_packages/numba/tests/test_cfunc.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.569`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/tests/test_cfunc.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.569 |
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
Tests for @cfunc and friends.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestCFunc, TestCArray, TestCffiStruct
- **funkcje:** `add_usecase`, `div_usecase`, `square_usecase`, `objmode_usecase`, `make_cfarray_usecase`, `make_cfarray_dtype_usecase`, `cfarray_usecase`, `cfarray_usecase`, `test_basic`, `test_cffi`, `test_locals`, `test_errors`, `test_llvm_ir`, `test_object_mode`, `run_carray_usecase`, `check_carray_usecase`, `make_voidptr`, `make_float32_pointer`, `make_float64_pointer`, `check_carray_farray`, `test_carray`, `test_farray`, `make_carray_sigs`, `check_numba_carray_farray`, `test_numba_carray`, `test_numba_farray`, `get_ffi`, `test_type_parsing`, `test_cfunc_callback`, `test_unsupport_bitsize`

## Opis
Tests for @cfunc and friends.
