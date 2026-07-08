# test_loadtxt.py — .python_packages/numpy/lib/tests/test_loadtxt.py

## Tożsamość
- **id_karty:** `REPO-TEST_LOADTXT-E315`
- **ścieżka:** `.python_packages/numpy/lib/tests/test_loadtxt.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.241`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numpy/lib/tests/test_loadtxt.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.241 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SOURCE_REQUIRED`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.509375`
- **R₃:** `0.557002`
- **R₆:** `0.453972`
- **R₉:** `0.573802`
- **potencjal_kappa:** `-0.191054`
- **masa_semantyczna:** `-0.307021`
- **rodzaj_karty:** `0.246226`


## Rola
Tests specific to `np.loadtxt` added during the move of loadtxt to be backed

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** TestCReaderUnitTests, BadSequence, BadFileLike, BadFileLike
- **funkcje:** `test_scientific_notation`, `test_comment_multiple_chars`, `mixed_types_structured`, `test_structured_dtype_and_skiprows_no_empty_lines`, `test_unpack_structured`, `test_structured_dtype_with_shape`, `test_structured_dtype_with_multi_shape`, `test_nested_structured_subarray`, `test_structured_dtype_offsets`, `test_exception_negative_row_limits`, `test_exception_noninteger_row_limits`, `test_ndmin_single_row_or_col`, `test_bad_ndmin`, `test_blank_lines_spaces_delimit`, `test_blank_lines_normal_delimiter`, `test_maxrows_no_blank_lines`, `test_exception_message_bad_values`, `test_converters_negative_indices`, `test_converters_negative_indices_with_usecols`, `test_ragged_error`, `test_ragged_usecols`, `test_empty_usecols`, `test_large_unicode_characters`, `test_unicode_with_converter`, `test_converter_with_structured_dtype`, `test_converter_with_unicode_dtype`, `test_read_huge_row`, `test_huge_float`, `test_string_no_length_given`, `test_float_conversion`

## Opis
Tests specific to `np.loadtxt` added during the move of loadtxt to be backed
by C code.
These tests complement those found in `test_io.py`.
