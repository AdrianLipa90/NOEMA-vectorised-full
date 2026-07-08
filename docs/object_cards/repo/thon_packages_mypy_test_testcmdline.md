# testcmdline.py — .python_packages/mypy/test/testcmdline.py

## Tożsamość
- **id_karty:** `REPO-TESTCMDLINE-D311`
- **ścieżka:** `.python_packages/mypy/test/testcmdline.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.994`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/test/testcmdline.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.994 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `FOLD`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.351212`
- **R₃:** `0.661831`
- **R₆:** `0.649218`
- **R₉:** `0.522246`
- **potencjal_kappa:** `-0.135067`
- **masa_semantyczna:** `-0.137397`
- **rodzaj_karty:** `0.29302`


## Rola
Test cases for the command line.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** PythonCmdlineSuite
- **funkcje:** `test_python_cmdline`, `parse_args`, `parse_cwd`, `normalize_devnull`, `run_case`

## Opis
Test cases for the command line.

To begin we test that "mypy <directory>[/]" always recurses down the
whole tree.
