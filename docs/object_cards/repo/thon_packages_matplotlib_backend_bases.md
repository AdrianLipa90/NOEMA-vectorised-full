# backend_bases.py — .python_packages/matplotlib/backend_bases.py

## Tożsamość
- **id_karty:** `REPO-BACKEND_BASES-C680`
- **ścieżka:** `.python_packages/matplotlib/backend_bases.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.463`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/backend_bases.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.463 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_OBLIGATION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.59271`
- **R₃:** `0.552945`
- **R₆:** `0.534582`
- **R₉:** `0.582078`
- **potencjal_kappa:** `0.23834`
- **masa_semantyczna:** `-0.091456`
- **rodzaj_karty:** `0.276031`


## Rola
Abstract base classes define the primitives that renderers and

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** RendererBase, GraphicsContextBase, TimerBase, Event, DrawEvent, ResizeEvent, CloseEvent, LocationEvent, MouseButton, MouseEvent, PickEvent, KeyEvent, FigureCanvasBase, NonGuiException, FigureManagerBase, _Mode, NavigationToolbar2, ToolContainerBase, _Backend, ShowBase
- **funkcje:** `register_backend`, `get_registered_canvas_class`, `_key_handler`, `_mouse_handler`, `_get_renderer`, `_no_output_draw`, `_is_non_interactive_terminal_ipython`, `_allow_interrupt`, `key_press_handler`, `button_press_handler`, `scroll_handler`, `open_group`, `close_group`, `draw_path`, `draw_markers`, `draw_path_collection`, `draw_quad_mesh`, `draw_gouraud_triangles`, `_iter_collection_raw_paths`, `_iter_collection_uses_per_path`, `_iter_collection`, `get_image_magnification`, `draw_image`, `option_image_nocomposite`, `option_scale_image`, `draw_tex`, `draw_text`, `_draw_text_as_path`, `get_text_width_height_descent`, `flipy`

## Opis
Abstract base classes define the primitives that renderers and
graphics contexts must implement to serve as a Matplotlib backend.

`RendererBase`
    An abstract base class to handle drawing/rendering operations.

`FigureCanvasBase`
    The abstraction layer that separates the `.Figure` from the backend
    specific details like a user interface drawing area.

`GraphicsContextBase`
    An abstract
