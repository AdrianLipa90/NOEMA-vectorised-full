# diagram_drawing.py — .python_packages/sympy/categories/diagram_drawing.py

## Tożsamość
- **id_karty:** `REPO-DIAGRAM_DRAWING-BE13`
- **ścieżka:** `.python_packages/sympy/categories/diagram_drawing.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.985`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/categories/diagram_drawing.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.985 |
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
This module contains the functionality to arrange the nodes of a

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** _GrowableGrid, DiagramGrid, ArrowStringDescription, XypicDiagramDrawer
- **funkcje:** `xypic_draw_diagram`, `preview_diagram`, `width`, `height`, `append_row`, `append_column`, `prepend_row`, `prepend_column`, `_simplify_morphisms`, `_merge_premises_conclusions`, `_juxtapose_edges`, `_add_edge_append`, `_build_skeleton`, `_list_triangles`, `_drop_redundant_triangles`, `_morphism_length`, `_compute_triangle_min_sizes`, `_triangle_objects`, `_other_vertex`, `_empty_point`, `_put_object`, `_choose_target_cell`, `_find_triangle_to_weld`, `_weld_triangle`, `_triangle_key`, `_pick_root_edge`, `_drop_irrelevant_triangles`, `_grow_pseudopod`, `_handle_groups`, `_generic_layout`

## Opis
This module contains the functionality to arrange the nodes of a
diagram on an abstract grid, and then to produce a graphical
representation of the grid.

The currently supported back-ends are Xy-pic [Xypic].

Layout Algorithm
================

This section provides an overview of the algorithms implemented in
:class:`DiagramGrid` to lay out diagrams.

The first step of the algorithm is the remova
