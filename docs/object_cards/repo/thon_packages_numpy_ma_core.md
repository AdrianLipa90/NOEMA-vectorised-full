# core.py — .python_packages/numpy/ma/core.py

## Tożsamość
- **id_karty:** `REPO-CORE-B2AE`
- **ścieżka:** `.python_packages/numpy/ma/core.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.157`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numpy/ma/core.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.157 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `COMPOSITION`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.528337`
- **R₃:** `0.492776`
- **R₆:** `0.696453`
- **R₉:** `0.565583`
- **potencjal_kappa:** `0.185923`
- **masa_semantyczna:** `-0.141173`
- **rodzaj_karty:** `0.274318`


## Rola
numpy.ma : a package to handle missing or invalid values.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** MaskedArrayFutureWarning, MAError, MaskError, _DomainCheckInterval, _DomainTan, _DomainSafeDivide, _DomainGreater, _DomainGreaterEqual, _MaskedUFunc, _MaskedUnaryOperation, _MaskedBinaryOperation, _DomainedBinaryOperation, _MaskedPrintOption, MaskedIterator, MaskedArray, mvoid, MaskedConstant, _extrema_operation
- **funkcje:** `_deprecate_argsort_axis`, `doc_note`, `_recursive_fill_value`, `_get_dtype_of`, `default_fill_value`, `_extremum_fill_value`, `minimum_fill_value`, `maximum_fill_value`, `_recursive_set_fill_value`, `_check_fill_value`, `set_fill_value`, `get_fill_value`, `common_fill_value`, `filled`, `get_masked_subclass`, `getdata`, `fix_invalid`, `is_string_or_list_of_strings`, `_replace_dtype_fields_recursive`, `_replace_dtype_fields`, `make_mask_descr`, `getmask`, `getmaskarray`, `is_mask`, `_shrink_mask`, `make_mask`, `make_mask_none`, `_recursive_mask_or`, `mask_or`, `flatten_mask`

## Opis
numpy.ma : a package to handle missing or invalid values.

This package was initially written for numarray by Paul F. Dubois
at Lawrence Livermore National Laboratory.
In 2006, the package was completely rewritten by Pierre Gerard-Marchant
(University of Georgia) to make the MaskedArray class a subclass of ndarray,
and to improve support of structured arrays.


Copyright 1999, 2000, 2001 Regents o
