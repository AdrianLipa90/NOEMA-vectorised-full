# markers.py — .python_packages/matplotlib/markers.py

## Tożsamość
- **id_karty:** `REPO-MARKERS-84C8`
- **ścieżka:** `.python_packages/matplotlib/markers.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.857`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/markers.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.857 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RETURN`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.642878`
- **R₃:** `0.503912`
- **R₆:** `0.555289`
- **R₉:** `0.707983`
- **potencjal_kappa:** `-0.270999`
- **masa_semantyczna:** `-0.074142`
- **rodzaj_karty:** `0.291714`


## Rola
Functions to handle markers; used by the marker functionality of

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** MarkerStyle
- **funkcje:** `_recache`, `is_filled`, `get_fillstyle`, `_set_fillstyle`, `get_joinstyle`, `get_capstyle`, `get_marker`, `_set_marker`, `get_path`, `get_transform`, `get_alt_path`, `get_alt_transform`, `get_snap_threshold`, `get_user_transform`, `transformed`, `rotated`, `scaled`, `_set_nothing`, `_set_custom_marker`, `_set_path_marker`, `_set_vertices`, `_set_tuple_marker`, `_set_mathtext_path`, `_half_fill`, `_set_circle`, `_set_point`, `_set_pixel`, `_set_triangle`, `_set_triangle_up`, `_set_triangle_down`

## Opis
Functions to handle markers; used by the marker functionality of
`~matplotlib.axes.Axes.plot`, `~matplotlib.axes.Axes.scatter`, and
`~matplotlib.axes.Axes.errorbar`.

All possible markers are defined here:

============================== ====== =========================================
marker                         symbol description
============================== ====== =========================
