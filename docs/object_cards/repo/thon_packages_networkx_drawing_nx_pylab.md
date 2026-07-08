# nx_pylab.py — .python_packages/networkx/drawing/nx_pylab.py

## Tożsamość
- **id_karty:** `REPO-NX_PYLAB-789F`
- **ścieżka:** `.python_packages/networkx/drawing/nx_pylab.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.765`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/networkx/drawing/nx_pylab.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.765 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `NEGATION`
- **odcisk_harmoniczny:** `LHLL`
- **R₁:** `0.425094`
- **R₃:** `0.614676`
- **R₆:** `0.450577`
- **R₉:** `0.387679`
- **potencjal_kappa:** `0.085998`
- **masa_semantyczna:** `-0.143065`
- **rodzaj_karty:** `0.271614`


## Rola
**********

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** CurvedArrowTextBase, FancyArrowFactory, CurvedArrowText, ConnectionStyleFactory, CurvedArrowText
- **funkcje:** `apply_matplotlib_colors`, `display`, `draw`, `draw_networkx`, `draw_networkx_nodes`, `draw_networkx_edges`, `draw_networkx_labels`, `draw_networkx_edge_labels`, `draw_bipartite`, `draw_circular`, `draw_kamada_kawai`, `draw_random`, `draw_spectral`, `draw_spring`, `draw_shell`, `draw_planar`, `draw_forceatlas2`, `apply_alpha`, `do_map`, `_get_arrow_path_disp`, `_update_text_pos_angle`, `draw`, `node_property_sequence`, `compute_colors`, `collection_compatible`, `edge_property_sequence`, `get_edge_attr`, `get_node_attr`, `self_loop`, `to_marker_edge`

## Opis
**********
Matplotlib
**********

Draw networks with matplotlib.

Examples
--------
>>> G = nx.complete_graph(5)
>>> nx.draw(G)

See Also
--------
 - :doc:`matplotlib <matplotlib:index>`
 - :func:`matplotlib.pyplot.scatter`
 - :obj:`matplotlib.patches.FancyArrowPatch`
