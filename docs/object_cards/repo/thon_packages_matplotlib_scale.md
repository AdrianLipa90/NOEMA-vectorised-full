# scale.py — .python_packages/matplotlib/scale.py

## Tożsamość
- **id_karty:** `REPO-SCALE-03FE`
- **ścieżka:** `.python_packages/matplotlib/scale.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.044`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/scale.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.044 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SOURCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.591319`
- **R₃:** `0.39689`
- **R₆:** `0.568492`
- **R₉:** `0.527911`
- **potencjal_kappa:** `0.015345`
- **masa_semantyczna:** `-0.142691`
- **rodzaj_karty:** `0.266598`


## Rola
Scales define the distribution of data values on an axis, e.g. a log scaling.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ScaleBase, LinearScale, FuncTransform, FuncScale, LogTransform, InvertedLogTransform, LogScale, FuncScaleLog, SymmetricalLogTransform, InvertedSymmetricalLogTransform, SymmetricalLogScale, AsinhTransform, InvertedAsinhTransform, AsinhScale, LogitTransform, LogisticTransform, LogitScale
- **funkcje:** `_make_axis_parameter_optional`, `get_scale_names`, `scale_factory`, `register_scale`, `_get_scale_docs`, `get_transform`, `set_default_locators_and_formatters`, `limit_range_for_scale`, `val_in_range`, `wrapper`, `set_default_locators_and_formatters`, `get_transform`, `val_in_range`, `transform_non_affine`, `inverted`, `get_transform`, `set_default_locators_and_formatters`, `transform_non_affine`, `inverted`, `transform_non_affine`, `inverted`, `set_default_locators_and_formatters`, `get_transform`, `limit_range_for_scale`, `val_in_range`, `base`, `get_transform`, `transform_non_affine`, `inverted`, `invlinthresh`

## Opis
Scales define the distribution of data values on an axis, e.g. a log scaling.

The mapping is implemented through `.Transform` subclasses.

The following scales are built-in:

.. _builtin_scales:

============= ===================== ================================ =================================
Name          Class                 Transform                        Inverted transform
============
