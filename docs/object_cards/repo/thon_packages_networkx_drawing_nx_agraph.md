# nx_agraph.py — .python_packages/networkx/drawing/nx_agraph.py

## Tożsamość
- **id_karty:** `REPO-NX_AGRAPH-5D06`
- **ścieżka:** `.python_packages/networkx/drawing/nx_agraph.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.954`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/networkx/drawing/nx_agraph.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.954 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `FORCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.552175`
- **R₃:** `0.435218`
- **R₆:** `0.571397`
- **R₉:** `0.579087`
- **potencjal_kappa:** `0.300939`
- **masa_semantyczna:** `0.016845`
- **rodzaj_karty:** `0.260112`


## Rola
***************

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `from_agraph`, `to_agraph`, `write_dot`, `read_dot`, `graphviz_layout`, `pygraphviz_layout`, `view_pygraphviz`, `update_attrs`, `clean_attrs`, `func`

## Opis
***************
Graphviz AGraph
***************

Interface to pygraphviz AGraph class.

Examples
--------
>>> G = nx.complete_graph(5)
>>> A = nx.nx_agraph.to_agraph(G)
>>> H = nx.nx_agraph.from_agraph(A)

See Also
--------
 - Pygraphviz: http://pygraphviz.github.io/
 - Graphviz:      https://www.graphviz.org
 - DOT Language:  http://www.graphviz.org/doc/info/lang.html
