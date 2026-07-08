# ismags.py — .python_packages/networkx/algorithms/isomorphism/ismags.py

## Tożsamość
- **id_karty:** `REPO-ISMAGS-2D2F`
- **ścieżka:** `.python_packages/networkx/algorithms/isomorphism/ismags.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.626`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/networkx/algorithms/isomorphism/ismags.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.626 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `REFUSAL`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.441725`
- **R₃:** `0.537197`
- **R₆:** `0.362678`
- **R₉:** `0.509166`
- **potencjal_kappa:** `0.077364`
- **masa_semantyczna:** `-0.245874`
- **rodzaj_karty:** `0.27107`


## Rola
ISMAGS Algorithm

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** EdgeLookup, ISMAGS
- **funkcje:** `are_all_equal`, `make_partition`, `node_to_part_ID_dict`, `color_degree_by_node`, `items`, `create_aligned_partitions`, `find_isomorphisms`, `_get_color_degree_candidates`, `largest_common_subgraph`, `analyze_subgraph_symmetry`, `is_isomorphic`, `subgraph_is_isomorphic`, `isomorphisms_iter`, `subgraph_isomorphisms_iter`, `_get_node_color_candidate_sets`, `_refine_node_partition`, `_map_nodes`, `_largest_common_subgraph`, `_remove_node`, `_get_permutations_by_length`, `_refine_opp`, `_find_permutations`, `_process_ordered_pair_partitions`, `equal_color`, `equal_color`, `_load_next_queue_entry`, `sg_match`, `sg_match`, `g_match`, `g_match`

## Opis
ISMAGS Algorithm
================

Provides a Python implementation of the ISMAGS algorithm. [1]_

ISMAGS does a symmetry analysis to find the constraints on isomorphisms if
we preclude yielding isomorphisms that differ by a symmetry of the subgraph.
For example, if the subgraph contains a 4-cycle, every isomorphism would have a
symmetric version with the nodes rotated relative to the original iso
