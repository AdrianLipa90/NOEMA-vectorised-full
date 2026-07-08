# decorators.py — .python_packages/sympy/core/decorators.py

## Tożsamość
- **id_karty:** `REPO-DECORATORS-2F4F`
- **ścieżka:** `.python_packages/sympy/core/decorators.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.886`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/core/decorators.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.886 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `UNCERTAINTY`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.435049`
- **R₃:** `0.572136`
- **R₆:** `0.544042`
- **R₉:** `0.477522`
- **potencjal_kappa:** `0.159902`
- **masa_semantyczna:** `-0.053674`
- **rodzaj_karty:** `0.279085`


## Rola
SymPy core decorators.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** _SympifyWrapper
- **funkcje:** `_sympifyit`, `call_highest_priority`, `sympify_method_args`, `sympify_return`, `deco`, `priority_decorator`, `wrapper`, `make_wrapped`, `binary_op_wrapper`, `_func`

## Opis
SymPy core decorators.

The purpose of this module is to expose decorators without any other
dependencies, so that they can be easily imported anywhere in sympy/core.
