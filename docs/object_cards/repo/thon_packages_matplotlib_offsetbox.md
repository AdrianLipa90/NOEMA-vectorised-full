# offsetbox.py — .python_packages/matplotlib/offsetbox.py

## Tożsamość
- **id_karty:** `REPO-OFFSETBOX-007F`
- **ścieżka:** `.python_packages/matplotlib/offsetbox.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.839`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/offsetbox.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.839 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_PERMISSION`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.453718`
- **R₃:** `0.541785`
- **R₆:** `0.466054`
- **R₉:** `0.529069`
- **potencjal_kappa:** `0.025212`
- **masa_semantyczna:** `0.161862`
- **rodzaj_karty:** `0.285369`


## Rola
Container classes for `.Artist`\s.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** OffsetBox, PackerBase, VPacker, HPacker, PaddedBox, DrawingArea, TextArea, AuxTransformBox, AnchoredOffsetbox, AnchoredText, OffsetImage, AnnotationBbox, DraggableBase, DraggableOffsetBox, DraggableAnnotation
- **funkcje:** `_compat_get_offset`, `_bbox_artist`, `_get_packed_offsets`, `_get_aligned_offsets`, `_get_anchored_bbox`, `get_offset`, `set_figure`, `axes`, `contains`, `set_offset`, `get_offset`, `set_width`, `set_height`, `get_visible_children`, `get_children`, `_get_bbox_and_child_offsets`, `get_bbox`, `get_window_extent`, `draw`, `_get_bbox_and_child_offsets`, `_get_bbox_and_child_offsets`, `_get_bbox_and_child_offsets`, `draw`, `update_frame`, `draw_frame`, `clip_children`, `clip_children`, `get_transform`, `set_transform`, `set_offset`

## Opis
Container classes for `.Artist`\s.

`OffsetBox`
    The base of all container artists defined in this module.

`AnchoredOffsetbox`, `AnchoredText`
    Anchor and align an arbitrary `.Artist` or a text relative to the parent
    axes or a specific anchor point.

`DrawingArea`
    A container with fixed width and height. Children have a fixed position
    inside the container and may be clipped.

`H
