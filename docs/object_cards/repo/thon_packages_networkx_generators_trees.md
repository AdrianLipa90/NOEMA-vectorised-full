# trees.py — .python_packages/networkx/generators/trees.py

## Tożsamość
- **id_karty:** `REPO-TREES-2D35`
- **ścieżka:** `.python_packages/networkx/generators/trees.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.948`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/networkx/generators/trees.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.948 |
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
Functions for generating trees.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `prefix_tree`, `prefix_tree_recursive`, `random_labeled_tree`, `random_labeled_rooted_tree`, `random_labeled_rooted_forest`, `_to_nx`, `_num_rooted_trees`, `_select_jd_trees`, `_random_unlabeled_rooted_tree`, `random_unlabeled_rooted_tree`, `_num_rooted_forests`, `_select_jd_forests`, `_random_unlabeled_rooted_forest`, `random_unlabeled_rooted_forest`, `_num_trees`, `_bicenter`, `_random_unlabeled_tree`, `random_unlabeled_tree`, `get_children`, `_helper`, `_select_k`

## Opis
Functions for generating trees.

The functions sampling trees at random in this module come
in two variants: labeled and unlabeled. The labeled variants
sample from every possible tree with the given number of nodes
uniformly at random. The unlabeled variants sample from every
possible *isomorphism class* of trees with the given number
of nodes uniformly at random.

To understand the difference, c
