# imputils.py — .python_packages/numba/core/imputils.py

## Tożsamość
- **id_karty:** `REPO-IMPUTILS-C865`
- **ścieżka:** `.python_packages/numba/core/imputils.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.017`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/core/imputils.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.017 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ATTRACTOR`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.476161`
- **R₃:** `0.526498`
- **R₆:** `0.547584`
- **R₉:** `0.472579`
- **potencjal_kappa:** `4.910705`
- **masa_semantyczna:** `13.031004`
- **rodzaj_karty:** `1.5`


## Rola
Utilities to simplify the boilerplate for native lowering.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Registry, RegistryLoader, _IternextResult, RefType
- **funkcje:** `_decorate_getattr`, `_decorate_setattr`, `fix_returning_optional`, `user_function`, `user_generator`, `iterator_impl`, `iternext_impl`, `call_getiter`, `call_iternext`, `call_len`, `for_iter`, `impl_ret_new_ref`, `impl_ret_borrowed`, `impl_ret_untracked`, `force_error_model`, `numba_typeref_ctor`, `lower`, `_decorate_attr`, `lower_getattr`, `lower_getattr_generic`, `lower_setattr`, `lower_setattr_generic`, `lower_cast`, `lower_constant`, `imp`, `imp`, `wrapper`, `set_exhausted`, `set_valid`, `yield_`

## Opis
Utilities to simplify the boilerplate for native lowering.
