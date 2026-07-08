# legend_handler.py — .python_packages/matplotlib/legend_handler.py

## Tożsamość
- **id_karty:** `REPO-LEGEND_HANDLER-7A29`
- **ścieżka:** `.python_packages/matplotlib/legend_handler.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.046`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/legend_handler.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.046 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ADDITION`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.662589`
- **R₃:** `0.614656`
- **R₆:** `0.542851`
- **R₉:** `0.417608`
- **potencjal_kappa:** `0.07638`
- **masa_semantyczna:** `0.206164`
- **rodzaj_karty:** `0.259027`


## Rola
Default legend handlers.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** HandlerBase, HandlerNpoints, HandlerNpointsYoffsets, HandlerLine2DCompound, HandlerLine2D, HandlerPatch, HandlerStepPatch, HandlerLineCollection, HandlerRegularPolyCollection, HandlerPathCollection, HandlerCircleCollection, HandlerErrorbar, HandlerStem, HandlerTuple, HandlerPolyCollection
- **funkcje:** `update_from_first_child`, `_update_prop`, `_default_update_prop`, `update_prop`, `adjust_drawing_area`, `legend_artist`, `create_artists`, `get_numpoints`, `get_xdata`, `get_ydata`, `create_artists`, `create_artists`, `_create_patch`, `create_artists`, `_create_patch`, `_create_line`, `create_artists`, `get_numpoints`, `_default_update_prop`, `create_artists`, `get_numpoints`, `get_sizes`, `update_prop`, `create_collection`, `create_artists`, `create_collection`, `create_collection`, `get_err_size`, `create_artists`, `get_ydata`

## Opis
Default legend handlers.

.. important::

    This is a low-level legend API, which most end users do not need.

    We recommend that you are familiar with the :ref:`legend guide
    <legend_guide>` before reading this documentation.

Legend handlers are expected to be a callable object with a following
signature::

    legend_handler(legend, orig_handle, fontsize, handlebox)

Where *legend* is t
