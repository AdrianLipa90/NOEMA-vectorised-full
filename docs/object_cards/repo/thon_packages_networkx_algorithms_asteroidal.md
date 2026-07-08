# asteroidal.py — .python_packages/networkx/algorithms/asteroidal.py

## Tożsamość
- **id_karty:** `REPO-ASTEROIDAL-EA4B`
- **ścieżka:** `.python_packages/networkx/algorithms/asteroidal.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.179`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/networkx/algorithms/asteroidal.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.179 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SOURCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.591319`
- **R₃:** `0.39689`
- **R₆:** `0.568492`
- **R₉:** `0.527911`
- **potencjal_kappa:** `0.015345`
- **masa_semantyczna:** `-0.142691`
- **rodzaj_karty:** `0.266598`


## Rola
Algorithms for asteroidal triples and asteroidal numbers in graphs.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `find_asteroidal_triple`, `is_at_free`, `create_component_structure`

## Opis
Algorithms for asteroidal triples and asteroidal numbers in graphs.

An asteroidal triple in a graph G is a set of three non-adjacent vertices
u, v and w such that there exist a path between any two of them that avoids
closed neighborhood of the third. More formally, v_j, v_k belongs to the same
connected component of G - N[v_i], where N[v_i] denotes the closed neighborhood
of v_i. A graph which d
