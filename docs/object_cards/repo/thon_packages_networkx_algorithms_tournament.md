# tournament.py — .python_packages/networkx/algorithms/tournament.py

## Tożsamość
- **id_karty:** `REPO-TOURNAMENT-FBFD`
- **ścieżka:** `.python_packages/networkx/algorithms/tournament.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.206`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/networkx/algorithms/tournament.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.206 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_NECESSITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.449701`
- **R₃:** `0.392905`
- **R₆:** `0.402231`
- **R₉:** `0.439135`
- **potencjal_kappa:** `-0.089486`
- **masa_semantyczna:** `-0.210953`
- **rodzaj_karty:** `0.286192`


## Rola
Functions concerning tournament graphs.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `index_satisfying`, `is_tournament`, `hamiltonian_path`, `random_tournament`, `score_sequence`, `tournament_matrix`, `is_reachable`, `is_strongly_connected`, `two_neighborhood`, `is_closed`

## Opis
Functions concerning tournament graphs.

A `tournament graph`_ is a complete oriented graph. In other words, it
is a directed graph in which there is exactly one directed edge joining
each pair of distinct nodes. For each function in this module that
accepts a graph as input, you must provide a tournament graph. The
responsibility is on the caller to ensure that the graph is a tournament
graph:
