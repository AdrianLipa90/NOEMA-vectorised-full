# backend_cairo.py — .python_packages/matplotlib/backends/backend_cairo.py

## Tożsamość
- **id_karty:** `REPO-BACKEND_CAIRO-A62B`
- **ścieżka:** `.python_packages/matplotlib/backends/backend_cairo.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.192`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/backends/backend_cairo.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.192 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RISK`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.594265`
- **R₃:** `0.468144`
- **R₆:** `0.457554`
- **R₉:** `0.414103`
- **potencjal_kappa:** `0.19508`
- **masa_semantyczna:** `-0.03873`
- **rodzaj_karty:** `0.279007`


## Rola
A Cairo backend for Matplotlib

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** RendererCairo, GraphicsContextCairo, _CairoRegion, FigureCanvasCairo, _BackendCairo
- **funkcje:** `_set_rgba`, `_append_path`, `_cairo_font_args_from_font_prop`, `attr`, `set_context`, `_fill_and_stroke`, `draw_path`, `draw_markers`, `draw_image`, `draw_text`, `_draw_mathtext`, `get_canvas_width_height`, `get_text_width_height_descent`, `new_gc`, `points_to_pixels`, `restore`, `set_alpha`, `set_antialiased`, `get_antialiased`, `set_capstyle`, `set_clip_rectangle`, `set_clip_path`, `set_dashes`, `set_foreground`, `get_rgb`, `set_joinstyle`, `set_linewidth`, `_renderer`, `get_renderer`, `copy_from_bbox`

## Opis
A Cairo backend for Matplotlib
==============================
:Author: Steve Chaplin and others

This backend depends on cairocffi or pycairo.
