# extbuild.py — .python_packages/numpy/testing/_private/extbuild.py

## Tożsamość
- **id_karty:** `REPO-EXTBUILD-AABA`
- **ścieżka:** `.python_packages/numpy/testing/_private/extbuild.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.921`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numpy/testing/_private/extbuild.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.921 |
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
Build a c-extension module on-the-fly in tests.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `build_and_import_extension`, `compile_extension_module`, `_convert_str_to_file`, `_make_methods`, `_make_source`, `_c_compile`, `build`, `get_so_suffix`

## Opis
Build a c-extension module on-the-fly in tests.
See build_and_import_extensions for usage hints
