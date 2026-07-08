# npyfuncs.py — .python_packages/numba/np/npyfuncs.py

## Tożsamość
- **id_karty:** `REPO-NPYFUNCS-38B3`
- **ścieżka:** `.python_packages/numba/np/npyfuncs.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.750`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/np/npyfuncs.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.750 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `DIFFERENCE`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.563622`
- **R₃:** `0.51399`
- **R₆:** `0.516024`
- **R₉:** `0.447233`
- **potencjal_kappa:** `-0.196591`
- **masa_semantyczna:** `-0.06476`
- **rodzaj_karty:** `0.313562`


## Rola
Codegen for functions used as kernels in NumPy functions

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_check_arity_and_homogeneity`, `_call_func_by_name_with_cast`, `_dispatch_func_by_name_type`, `np_int_sdiv_impl`, `np_int_srem_impl`, `np_int_sdivrem_impl`, `np_int_udiv_impl`, `np_int_urem_impl`, `np_int_udivrem_impl`, `np_real_div_impl`, `np_real_mod_impl`, `np_real_fmod_impl`, `_fabs`, `np_complex_div_impl`, `_npy_logaddexp`, `_generate_logaddexp`, `_npy_logaddexp`, `np_real_logaddexp_impl`, `_npy_logaddexp2`, `npy_log2_1p`, `ol_npy_log2_1p`, `np_real_logaddexp2_impl`, `np_int_truediv_impl`, `np_real_floor_div_impl`, `np_real_divmod_impl`, `np_complex_floor_div_impl`, `np_complex_power_impl`, `real_float_power_impl`, `np_complex_float_power_impl`, `np_gcd_impl`

## Opis
Codegen for functions used as kernels in NumPy functions

Typically, the kernels of several ufuncs that can't map directly to
Python builtins
