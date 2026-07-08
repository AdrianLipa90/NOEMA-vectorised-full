# dag.py — .python_packages/networkx/algorithms/dag.py

## Tożsamość
- **id_karty:** `REPO-DAG-C6C0`
- **ścieżka:** `.python_packages/networkx/algorithms/dag.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.423`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/networkx/algorithms/dag.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.423 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_POSSIBILITY`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.565748`
- **R₃:** `0.628966`
- **R₆:** `0.492583`
- **R₉:** `0.589778`
- **potencjal_kappa:** `0.024081`
- **masa_semantyczna:** `-0.294904`
- **rodzaj_karty:** `0.302592`


## Rola
Algorithms for directed acyclic graphs (DAGs).

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `descendants`, `ancestors`, `has_cycle`, `is_directed_acyclic_graph`, `topological_generations`, `topological_sort`, `lexicographical_topological_sort`, `all_topological_sorts`, `is_aperiodic`, `transitive_closure`, `transitive_closure_dag`, `transitive_reduction`, `antichains`, `dag_longest_path`, `dag_longest_path_length`, `root_to_leaf_paths`, `dag_to_branching`, `v_structures`, `colliders`, `create_tuple`, `key`

## Opis
Algorithms for directed acyclic graphs (DAGs).

Note that most of these functions are only guaranteed to work for DAGs.
In general, these functions do not check for acyclic-ness, so it is up
to the user to check for that.
