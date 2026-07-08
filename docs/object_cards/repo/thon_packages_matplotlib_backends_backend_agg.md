# backend_agg.py — .python_packages/matplotlib/backends/backend_agg.py

## Tożsamość
- **id_karty:** `REPO-BACKEND_AGG-4D4D`
- **ścieżka:** `.python_packages/matplotlib/backends/backend_agg.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.584`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/backends/backend_agg.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.584 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `QUESTION`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.394639`
- **R₃:** `0.763677`
- **R₆:** `0.521308`
- **R₉:** `0.466584`
- **potencjal_kappa:** `-0.203086`
- **masa_semantyczna:** `-0.0017`
- **rodzaj_karty:** `0.305584`


## Rola
An `Anti-Grain Geometry`_ (AGG) backend.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** RendererAgg, FigureCanvasAgg, _BackendAgg
- **funkcje:** `get_hinting_flag`, `_update_methods`, `draw_path`, `_draw_text_glyphs_and_boxes`, `draw_mathtext`, `draw_text`, `get_text_width_height_descent`, `draw_tex`, `get_canvas_width_height`, `_prepare_font`, `points_to_pixels`, `buffer_rgba`, `tostring_argb`, `clear`, `option_image_nocomposite`, `option_scale_image`, `restore_region`, `start_filter`, `stop_filter`, `copy_from_bbox`, `restore_region`, `draw`, `get_renderer`, `tostring_argb`, `buffer_rgba`, `print_raw`, `_print_pil`, `print_png`, `print_to_buffer`, `print_gif`

## Opis
An `Anti-Grain Geometry`_ (AGG) backend.

Features that are implemented:

* capstyles and join styles
* dashes
* linewidth
* lines, rectangles, ellipses
* clipping to a rectangle
* output to RGBA and Pillow-supported image formats
* alpha blending
* DPI scaling properly - everything scales properly (dashes, linewidths, etc)
* draw polygon
* freetype2 w/ ft2font

Still TODO:

* integrate screen dpi
