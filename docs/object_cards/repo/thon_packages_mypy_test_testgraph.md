# testgraph.py — .python_packages/mypy/test/testgraph.py

## Tożsamość
- **id_karty:** `REPO-TESTGRAPH-16D7`
- **ścieżka:** `.python_packages/mypy/test/testgraph.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.133`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/test/testgraph.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.133 |
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
Test cases for graph processing code in build.py.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** GraphSuite
- **funkcje:** `test_topsort_empty`, `test_topsort`, `test_topsort_orphan`, `test_topsort_independent`, `test_topsort_linear_chain`, `test_topsort_self_dependency`, `test_topsort_orphan_diamond`, `test_topsort_cycle`, `test_scc`, `_make_manager`, `test_sorted_components`, `test_order_ascc`

## Opis
Test cases for graph processing code in build.py.
