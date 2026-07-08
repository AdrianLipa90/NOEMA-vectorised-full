# multiline_adjlist.py — .python_packages/networkx/readwrite/multiline_adjlist.py

## Tożsamość
- **id_karty:** `REPO-MULTILINE_ADJLIST-A600`
- **ścieżka:** `.python_packages/networkx/readwrite/multiline_adjlist.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.606`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/networkx/readwrite/multiline_adjlist.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.606 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_NECESSITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.449701`
- **R₃:** `0.392905`
- **R₆:** `0.402231`
- **R₉:** `0.439135`
- **potencjal_kappa:** `-0.089486`
- **masa_semantyczna:** `-0.210953`
- **rodzaj_karty:** `0.286192`


## Rola
*************************

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `generate_multiline_adjlist`, `write_multiline_adjlist`, `parse_multiline_adjlist`, `read_multiline_adjlist`

## Opis
*************************
Multi-line Adjacency List
*************************
Read and write NetworkX graphs as multi-line adjacency lists.

The multi-line adjacency list format is useful for graphs with
nodes that can be meaningfully represented as strings.  With this format
simple edge data can be stored but node or graph data is not.

Format
------
The first label in a line is the source node l
