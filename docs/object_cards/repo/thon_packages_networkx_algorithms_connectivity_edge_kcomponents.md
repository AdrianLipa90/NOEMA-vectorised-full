# edge_kcomponents.py — .python_packages/networkx/algorithms/connectivity/edge_kcomponents.py

## Tożsamość
- **id_karty:** `REPO-EDGE_KCOMPONENTS-D583`
- **ścieżka:** `.python_packages/networkx/algorithms/connectivity/edge_kcomponents.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `6.233`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/networkx/algorithms/connectivity/edge_kcomponents.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 6.233 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ADDITION`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.662589`
- **R₃:** `0.614656`
- **R₆:** `0.542851`
- **R₉:** `0.417608`
- **potencjal_kappa:** `0.07638`
- **masa_semantyczna:** `0.206164`
- **rodzaj_karty:** `0.259027`


## Rola
Algorithms for finding k-edge-connected components and subgraphs.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** EdgeComponentAuxGraph
- **funkcje:** `k_edge_components`, `k_edge_subgraphs`, `_k_edge_subgraphs_nodes`, `bridge_components`, `_low_degree_nodes`, `_high_degree_components`, `general_k_edge_subgraphs`, `construct`, `k_edge_components`, `k_edge_subgraphs`, `_recursive_build`

## Opis
Algorithms for finding k-edge-connected components and subgraphs.

A k-edge-connected component (k-edge-cc) is a maximal set of nodes in G, such
that all pairs of node have an edge-connectivity of at least k.

A k-edge-connected subgraph (k-edge-subgraph) is a maximal set of nodes in G,
such that the subgraph of G defined by the nodes has an edge-connectivity at
least k.
