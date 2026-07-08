# graph_hashing.py — .python_packages/networkx/algorithms/graph_hashing.py

## Tożsamość
- **id_karty:** `REPO-GRAPH_HASHING-AAF6`
- **ścieżka:** `.python_packages/networkx/algorithms/graph_hashing.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.015`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/networkx/algorithms/graph_hashing.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.015 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `BOUNDARY`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.587016`
- **R₃:** `0.481937`
- **R₆:** `0.525424`
- **R₉:** `0.380572`
- **potencjal_kappa:** `-0.130804`
- **masa_semantyczna:** `0.12548`
- **rodzaj_karty:** `0.280526`


## Rola
Functions for hashing graphs to strings.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_hash_label`, `_init_node_labels`, `_neighborhood_aggregate_undirected`, `_neighborhood_aggregate_directed`, `weisfeiler_lehman_graph_hash`, `weisfeiler_lehman_subgraph_hashes`, `weisfeiler_lehman_step`, `weisfeiler_lehman_step`

## Opis
Functions for hashing graphs to strings.
Isomorphic graphs should be assigned identical hashes.
For now, only Weisfeiler-Lehman hashing is implemented.
