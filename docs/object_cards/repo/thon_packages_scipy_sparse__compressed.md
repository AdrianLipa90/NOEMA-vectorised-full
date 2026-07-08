# _compressed.py — .python_packages/scipy/sparse/_compressed.py

## Tożsamość
- **id_karty:** `REPO-_COMPRESSED-EA54`
- **ścieżka:** `.python_packages/scipy/sparse/_compressed.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.747`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/sparse/_compressed.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.747 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SCOPE`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.516458`
- **R₃:** `0.452404`
- **R₆:** `0.493743`
- **R₉:** `0.465851`
- **potencjal_kappa:** `0.026123`
- **masa_semantyczna:** `0.147985`
- **rodzaj_karty:** `0.241584`


## Rola
Base class for sparse matrix formats using compressed storage.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** _cs_matrix
- **funkcje:** `_make_diagonal_csr`, `_process_slice`, `_getnnz`, `count_nonzero`, `check_format`, `_scalar_binopt`, `_add_dense`, `_add_sparse`, `_sub_sparse`, `_multiply_2d_with_broadcasting`, `_matmul_vector`, `_matmul_multivector`, `_matmul_sparse`, `diagonal`, `sum`, `_minor_reduce`, `_get_intXint`, `_get_sliceXslice`, `_get_arrayXarray`, `_get_columnXarray`, `_major_index_fancy`, `_major_slice`, `_minor_index_fancy`, `_minor_slice`, `_get_submatrix`, `_set_intXint`, `_set_arrayXarray`, `_set_arrayXarray_sparse`, `_setdiag`, `_prepare_indices`

## Opis
Base class for sparse matrix formats using compressed storage.
