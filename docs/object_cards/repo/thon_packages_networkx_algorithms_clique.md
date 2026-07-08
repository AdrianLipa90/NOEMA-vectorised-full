# clique.py — .python_packages/networkx/algorithms/clique.py

## Tożsamość
- **id_karty:** `REPO-CLIQUE-23A0`
- **ścieżka:** `.python_packages/networkx/algorithms/clique.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.922`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/networkx/algorithms/clique.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.922 |
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
Functions for finding and manipulating cliques.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** MaxWeightClique
- **funkcje:** `enumerate_all_cliques`, `find_cliques`, `find_cliques_recursive`, `make_max_clique_graph`, `make_clique_bipartite`, `node_clique_number`, `number_of_cliques`, `max_weight_clique`, `expand`, `update_incumbent_if_improved`, `greedily_find_independent_set`, `find_branching_nodes`, `expand`, `find_max_weight_clique`

## Opis
Functions for finding and manipulating cliques.

Finding the largest clique in a graph is NP-complete problem, so most of
these algorithms have an exponential running time; for more information,
see the Wikipedia article on the clique problem [1]_.

.. [1] clique problem:: https://en.wikipedia.org/wiki/Clique_problem
