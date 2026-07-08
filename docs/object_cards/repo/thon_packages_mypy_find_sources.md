# find_sources.py — .python_packages/mypy/find_sources.py

## Tożsamość
- **id_karty:** `REPO-FIND_SOURCES-C75F`
- **ścieżka:** `.python_packages/mypy/find_sources.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.708`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/find_sources.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.708 |
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
Routines for finding the sources that mypy will check

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** InvalidSourceList, SourceFinder
- **funkcje:** `create_source_list`, `keyfunc`, `normalise_package_base`, `get_explicit_package_bases`, `module_join`, `strip_py`, `is_explicit_package_base`, `find_sources_in_dir`, `crawl_up`, `crawl_up_dir`, `_crawl_up_helper`, `get_init_file`

## Opis
Routines for finding the sources that mypy will check
