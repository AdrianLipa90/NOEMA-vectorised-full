# test_dtype.py — .python_packages/h5py/tests/test_dtype.py

## Tożsamość
- **id_karty:** `REPO-TEST_DTYPE-4AE1`
- **ścieżka:** `.python_packages/h5py/tests/test_dtype.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.037`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/h5py/tests/test_dtype.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.037 |
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
Tests for converting between numpy dtypes and h5py data types

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestVlen, TestExplicitCast, TestOffsets, TestStrings, TestDateTime, TestBitfield
- **funkcje:** `test_write_empty_vlen`, `test_write_vlen_length0_compound`, `test_opaque`, `test_create_bitfield`, `test_complex_compat`, `assertVlenArrayEqual`, `test_compound`, `test_compound_vlen_bool`, `test_compound_vlen_enum`, `test_vlen_enum`, `test_f2_casting`, `test_compound_vlen`, `test_aligned_offsets`, `test_aligned_data`, `test_compound_robustness`, `test_out_of_order_offsets`, `test_float_round_tripping`, `test_vlen_utf8`, `test_vlen_ascii`, `test_fixed_utf8`, `test_fixed_ascii`, `test_datetime`, `test_timedelta`, `test_b8_bool`, `test_b8_bool_compound`, `test_b8_bool_compound_nested`, `test_b8_bool_compound_mixed_types`, `test_b8_bool_array`, `_test_b8`, `test_b16_uint16`

## Opis
Tests for converting between numpy dtypes and h5py data types
