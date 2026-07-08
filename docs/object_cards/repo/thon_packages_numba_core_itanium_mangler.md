# itanium_mangler.py — .python_packages/numba/core/itanium_mangler.py

## Tożsamość
- **id_karty:** `REPO-ITANIUM_MANGLER-6E93`
- **ścieżka:** `.python_packages/numba/core/itanium_mangler.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.835`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/core/itanium_mangler.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.835 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ACTION_REQUEST`
- **odcisk_harmoniczny:** `LLHL`
- **R₁:** `0.419252`
- **R₃:** `0.442825`
- **R₆:** `0.60198`
- **R₉:** `0.41548`
- **potencjal_kappa:** `-0.118614`
- **masa_semantyczna:** `0.191681`
- **rodzaj_karty:** `0.278922`


## Rola
Itanium CXX ABI Mangler

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_escape_string`, `_fix_lead_digit`, `_len_encoded`, `mangle_abi_tag`, `mangle_identifier`, `mangle_type_or_value`, `mangle_templated_ident`, `mangle_args`, `mangle`, `prepend_namespace`, `_split_mangled_ident`, `repl`

## Opis
Itanium CXX ABI Mangler

Reference: https://itanium-cxx-abi.github.io/cxx-abi/abi.html

The basics of the mangling scheme.

We are hijacking the CXX mangling scheme for our use.  We map Python modules
into CXX namespace.  A `module1.submodule2.foo` is mapped to
`module1::submodule2::foo`.   For parameterized numba types, we treat them as
templated types; for example, `array(int64, 1d, C)` becomes
