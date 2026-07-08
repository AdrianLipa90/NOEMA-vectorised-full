# testdaemon.py — .python_packages/mypy/test/testdaemon.py

## Tożsamość
- **id_karty:** `REPO-TESTDAEMON-4956`
- **ścieżka:** `.python_packages/mypy/test/testdaemon.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.759`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/test/testdaemon.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.759 |
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
End-to-end test cases for the daemon (dmypy).

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** DaemonSuite, DaemonUtilitySuite
- **funkcje:** `test_daemon`, `parse_script`, `run_cmd`, `run_case`, `test_filter_out_missing_top_level_packages`, `make_file`, `makepath`

## Opis
End-to-end test cases for the daemon (dmypy).

These are special because they run multiple shell commands.

This also includes some unit tests.
