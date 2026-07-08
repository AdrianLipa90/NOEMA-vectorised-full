# boundary.py — .python_packages/networkx/algorithms/boundary.py

## Tożsamość
- **id_karty:** `REPO-BOUNDARY-BD6C`
- **ścieżka:** `.python_packages/networkx/algorithms/boundary.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.276`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/networkx/algorithms/boundary.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.276 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `IDENTITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.405566`
- **R₃:** `0.499333`
- **R₆:** `0.494094`
- **R₉:** `0.455981`
- **potencjal_kappa:** `0.08965`
- **masa_semantyczna:** `-0.024381`
- **rodzaj_karty:** `0.279273`


## Rola
Routines to find the boundary of a set of nodes.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `edge_boundary`, `node_boundary`

## Opis
Routines to find the boundary of a set of nodes.

An edge boundary is a set of edges, each of which has exactly one
endpoint in a given set of nodes (or, in the case of directed graphs,
the set of edges whose source node is in the set).

A node boundary of a set *S* of nodes is the set of (out-)neighbors of
nodes in *S* that are outside *S*.
