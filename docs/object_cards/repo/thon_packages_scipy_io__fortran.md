# _fortran.py — .python_packages/scipy/io/_fortran.py

## Tożsamość
- **id_karty:** `REPO-_FORTRAN-8EB7`
- **ścieżka:** `.python_packages/scipy/io/_fortran.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.484`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/scipy/io/_fortran.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.484 |
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
Module to read / write Fortran unformatted sequential files.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** FortranEOFError, FortranFormattingError, FortranFile
- **funkcje:** `_read_size`, `write_record`, `read_record`, `read_ints`, `read_reals`, `close`

## Opis
Module to read / write Fortran unformatted sequential files.

This is in the spirit of code written by Neil Martinsen-Burrell and Joe Zuntz.
