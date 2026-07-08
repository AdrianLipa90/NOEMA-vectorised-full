# _helpers.py — .python_packages/scipy/_external/array_api_compat/common/_helpers.py

## Tożsamość
- **id_karty:** `REPO-_HELPERS-1811`
- **ścieżka:** `.python_packages/scipy/_external/array_api_compat/common/_helpers.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.738`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/_external/array_api_compat/common/_helpers.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.738 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_OBLIGATION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.59271`
- **R₃:** `0.552945`
- **R₆:** `0.534582`
- **R₉:** `0.582078`
- **potencjal_kappa:** `0.23834`
- **masa_semantyczna:** `-0.091456`
- **rodzaj_karty:** `0.276031`


## Rola
Various helper functions which are not part of the spec.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** _ClsToXPInfo, _dask_device
- **funkcje:** `_issubclass_fast`, `_is_jax_zero_gradient_array`, `is_numpy_array`, `is_cupy_array`, `is_torch_array`, `is_ndonnx_array`, `is_dask_array`, `is_jax_array`, `is_pydata_sparse_array`, `is_array_api_obj`, `_is_array_api_cls`, `_compat_module_name`, `is_numpy_namespace`, `is_cupy_namespace`, `is_torch_namespace`, `is_ndonnx_namespace`, `is_dask_namespace`, `is_jax_namespace`, `is_pydata_sparse_namespace`, `is_array_api_strict_namespace`, `_check_api_version`, `_cls_to_namespace`, `_jax_namespace`, `array_namespace`, `_check_device`, `device`, `_cupy_to_device`, `_torch_to_device`, `to_device`, `size`

## Opis
Various helper functions which are not part of the spec.

Functions which start with an underscore are for internal use only but helpers
that are in __all__ are intended as additional helper functions for use by end
users of the compat library.
