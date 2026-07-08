# similarity.py — .python_packages/networkx/algorithms/similarity.py

## Tożsamość
- **id_karty:** `REPO-SIMILARITY-FEDB`
- **ścieżka:** `.python_packages/networkx/algorithms/similarity.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.972`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/networkx/algorithms/similarity.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.972 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ASSERTION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.563342`
- **R₃:** `0.601856`
- **R₆:** `0.54039`
- **R₉:** `0.584219`
- **potencjal_kappa:** `-0.098441`
- **masa_semantyczna:** `0.347732`
- **rodzaj_karty:** `0.261593`


## Rola
Functions measuring similarity using graph edit distance.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** CostMatrix
- **funkcje:** `graph_edit_distance`, `optimal_edit_paths`, `optimize_graph_edit_distance`, `optimize_edit_paths`, `simrank_similarity`, `_simrank_similarity_python`, `_simrank_similarity_numpy`, `_prepare_panther_paths`, `panther_similarity`, `panther_vector_similarity`, `generate_random_paths`, `make_CostMatrix`, `extract_C`, `reduce_C`, `reduce_ind`, `match_edges`, `reduce_Ce`, `get_edit_ops`, `get_edit_paths`, `prune`, `avg_sim`, `sim`

## Opis
Functions measuring similarity using graph edit distance.

The graph edit distance is the number of edge/node changes needed
to make two graphs isomorphic.

The default algorithm/implementation is sub-optimal for some graphs.
The problem of finding the exact Graph Edit Distance (GED) is NP-hard
so it is often slow. If the simple interface `graph_edit_distance`
takes too long for your graph, try `o
