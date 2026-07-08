# graph.py — .python_packages/networkx/classes/graph.py

## Tożsamość
- **id_karty:** `REPO-GRAPH-BC53`
- **ścieżka:** `.python_packages/networkx/classes/graph.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.156`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/networkx/classes/graph.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.156 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RISK`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.594265`
- **R₃:** `0.468144`
- **R₆:** `0.457554`
- **R₉:** `0.414103`
- **potencjal_kappa:** `0.19508`
- **masa_semantyczna:** `-0.03873`
- **rodzaj_karty:** `0.279007`


## Rola
Base class for undirected graphs.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** _CachedPropertyResetterAdj, _CachedPropertyResetterNode, Graph
- **funkcje:** `to_directed_class`, `to_undirected_class`, `adj`, `name`, `name`, `add_node`, `add_nodes_from`, `remove_node`, `remove_nodes_from`, `nodes`, `number_of_nodes`, `order`, `has_node`, `add_edge`, `add_edges_from`, `add_weighted_edges_from`, `remove_edge`, `remove_edges_from`, `update`, `has_edge`, `neighbors`, `edges`, `get_edge_data`, `adjacency`, `degree`, `clear`, `clear_edges`, `is_multigraph`, `is_directed`, `copy`

## Opis
Base class for undirected graphs.

The Graph class allows any hashable object as a node
and can associate key/value attribute pairs with each undirected edge.

Self-loops are allowed but multiple edges are not (see MultiGraph).

For directed graphs see DiGraph and MultiDiGraph.
