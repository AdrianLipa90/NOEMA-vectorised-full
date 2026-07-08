# __init__.py — .python_packages/fontTools/varLib/__init__.py

## Tożsamość
- **id_karty:** `REPO-__INIT__-C1CA`
- **ścieżka:** `.python_packages/fontTools/varLib/__init__.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.628`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/fontTools/varLib/__init__.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.628 |
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
Module for dealing with 'gvar'-style font variations, also known as run-time

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** MasterFinder
- **funkcje:** `_add_fvar`, `_add_avar`, `_add_stat`, `_add_gvar`, `_remove_TTHinting`, `_merge_TTHinting`, `_has_inconsistent_use_my_metrics_flag`, `_unset_inconsistent_use_my_metrics_flags`, `_add_HVAR`, `_add_VVAR`, `_add_VHVAR`, `_get_advance_metrics`, `_add_MVAR`, `_add_BASE`, `_merge_OTL`, `_add_GSUB_feature_variations`, `_add_CFF2`, `_add_COLR`, `load_designspace`, `set_default_weight_width_slant`, `drop_implied_oncurve_points`, `build_many`, `build`, `_open_font`, `load_masters`, `_feature_variations_tags`, `addGSUBFeatureVariations`, `main`, `normalize`

## Opis
Module for dealing with 'gvar'-style font variations, also known as run-time
interpolation.

The ideas here are very similar to MutatorMath.  There is even code to read
MutatorMath .designspace files in the varLib.designspace module.

For now, if you run this file on a designspace file, it tries to find
ttf-interpolatable files for the masters and build a variable-font from
them.  Such ttf-interpo
