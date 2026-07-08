# hatch.py — .python_packages/matplotlib/hatch.py

## Tożsamość
- **id_karty:** `REPO-HATCH-08AF`
- **ścieżka:** `.python_packages/matplotlib/hatch.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.531`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/hatch.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.531 |
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
Module for generating hatch patterns.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** HatchPatternBase, HorizontalHatch, VerticalHatch, NorthEastHatch, SouthEastHatch, Shapes, Circles, SmallCircles, LargeCircles, SmallFilledCircles, Stars
- **funkcje:** `_validate_hatch_pattern`, `get_path`, `set_vertices_and_codes`, `set_vertices_and_codes`, `set_vertices_and_codes`, `set_vertices_and_codes`, `set_vertices_and_codes`

## Opis
Module for generating hatch patterns.

For examples of using the hatch API, see
:ref:`sphx_glr_gallery_shapes_and_collections_hatch_style_reference.py`.

The following hatching patterns are available, shown here at level 2 density:

.. plot:: _embedded_plots/hatch_classes.py
    :include-source: false
    :alt:
        8 squares, each showing the pattern corresponding to the hatch symbol:
