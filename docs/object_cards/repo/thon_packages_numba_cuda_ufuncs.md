# ufuncs.py — .python_packages/numba/cuda/ufuncs.py

## Tożsamość
- **id_karty:** `REPO-UFUNCS-B4B5`
- **ścieżka:** `.python_packages/numba/cuda/ufuncs.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.596`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/cuda/ufuncs.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.596 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_PERMISSION`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.453718`
- **R₃:** `0.541785`
- **R₆:** `0.466054`
- **R₉:** `0.529069`
- **potencjal_kappa:** `0.025212`
- **masa_semantyczna:** `0.161862`
- **rodzaj_karty:** `0.285369`


## Rola
Contains information on how to translate different ufuncs for the CUDA

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `get_ufunc_info`, `ufunc_db`, `np_unary_impl`, `np_binary_impl`, `np_real_log_impl`, `np_real_log2_impl`, `np_real_log10_impl`, `np_real_sin_impl`, `np_real_cos_impl`, `np_real_tan_impl`, `np_real_asin_impl`, `np_real_acos_impl`, `np_real_atan_impl`, `np_real_atan2_impl`, `np_real_hypot_impl`, `np_real_sinh_impl`, `np_complex_sinh_impl`, `np_real_cosh_impl`, `np_complex_cosh_impl`, `np_real_tanh_impl`, `np_complex_tanh_impl`, `np_real_asinh_impl`, `np_real_acosh_impl`, `np_real_atanh_impl`

## Opis
Contains information on how to translate different ufuncs for the CUDA
target. It is a database of different ufuncs and how each of its loops maps to
a function that implements the inner kernel of that ufunc (the inner kernel
being the per-element function).

Use get_ufunc_info() to get the information related to a ufunc.
