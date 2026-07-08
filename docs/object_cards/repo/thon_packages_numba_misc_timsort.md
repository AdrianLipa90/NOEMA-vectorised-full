# timsort.py — .python_packages/numba/misc/timsort.py

## Tożsamość
- **id_karty:** `REPO-TIMSORT-1E44`
- **ścieżka:** `.python_packages/numba/misc/timsort.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.185`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/misc/timsort.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.185 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `QUESTION`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.394639`
- **R₃:** `0.763677`
- **R₆:** `0.521308`
- **R₉:** `0.466584`
- **potencjal_kappa:** `-0.203086`
- **masa_semantyczna:** `-0.0017`
- **rodzaj_karty:** `0.305584`


## Rola
Timsort implementation.  Mostly adapted from CPython's listobject.c.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `make_timsort_impl`, `make_py_timsort`, `make_jit_timsort`, `has_values`, `merge_init`, `merge_init_with_values`, `merge_append`, `merge_pop`, `merge_getmem`, `merge_adjust_gallop`, `LT`, `binarysort`, `count_run`, `gallop_left`, `gallop_right`, `merge_compute_minrun`, `sortslice_copy`, `sortslice_copy_down`, `merge_lo`, `merge_hi`, `merge_at`, `merge_collapse`, `merge_force_collapse`, `reverse_slice`, `run_timsort_with_mergestate`, `run_timsort`, `run_timsort_with_values`

## Opis
Timsort implementation.  Mostly adapted from CPython's listobject.c.

For more information, see listsort.txt in CPython's source tree.
