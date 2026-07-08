# gdb_print_extension.py — .python_packages/numba/misc/gdb_print_extension.py

## Tożsamość
- **id_karty:** `REPO-GDB_PRINT_EXTENSION-CC3E`
- **ścieżka:** `.python_packages/numba/misc/gdb_print_extension.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.626`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/misc/gdb_print_extension.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.626 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MEMORY`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.481637`
- **R₃:** `0.436994`
- **R₆:** `0.50573`
- **R₉:** `0.517955`
- **potencjal_kappa:** `0.179117`
- **masa_semantyczna:** `0.012321`
- **rodzaj_karty:** `0.236997`


## Rola
gdb printing extension for Numba types.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** NumbaArrayPrinter, NumbaComplexPrinter, NumbaTuplePrinter, NumbaUniTuplePrinter, NumbaUnicodeTypePrinter
- **funkcje:** `_create_printers`, `to_string`, `to_string`, `to_string`, `to_string`, `to_string`, `dwarr2inttuple`

## Opis
gdb printing extension for Numba types.
