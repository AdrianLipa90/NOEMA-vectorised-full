# classic.py — .python_packages/networkx/generators/classic.py

## Tożsamość
- **id_karty:** `REPO-CLASSIC-4F97`
- **ścieżka:** `.python_packages/networkx/generators/classic.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.733`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/networkx/generators/classic.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.733 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SCOPE`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.516458`
- **R₃:** `0.452404`
- **R₆:** `0.493743`
- **R₉:** `0.465851`
- **potencjal_kappa:** `0.026123`
- **masa_semantyczna:** `0.147985`
- **rodzaj_karty:** `0.241584`


## Rola
Generators for some classic graphs.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_tree_edges`, `full_rary_tree`, `kneser_graph`, `balanced_tree`, `barbell_graph`, `binomial_tree`, `complete_graph`, `circular_ladder_graph`, `circulant_graph`, `cycle_graph`, `dorogovtsev_goltsev_mendes_graph`, `empty_graph`, `ladder_graph`, `lollipop_graph`, `null_graph`, `path_graph`, `star_graph`, `tadpole_graph`, `trivial_graph`, `turan_graph`, `wheel_graph`, `complete_multipartite_graph`

## Opis
Generators for some classic graphs.

The typical graph builder function is called as follows:

>>> G = nx.complete_graph(100)

returning the complete graph on n nodes labeled 0, .., 99
as a simple graph. Except for `empty_graph`, all the functions
in this module return a Graph class (i.e. a simple, undirected graph).
