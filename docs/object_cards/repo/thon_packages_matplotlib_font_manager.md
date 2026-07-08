# font_manager.py — .python_packages/matplotlib/font_manager.py

## Tożsamość
- **id_karty:** `REPO-FONT_MANAGER-B3E6`
- **ścieżka:** `.python_packages/matplotlib/font_manager.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.730`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/font_manager.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.730 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `TRANSFORM`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.489274`
- **R₃:** `0.512237`
- **R₆:** `0.547669`
- **R₉:** `0.477906`
- **potencjal_kappa:** `0.124323`
- **masa_semantyczna:** `-0.167832`
- **rodzaj_karty:** `0.281825`


## Rola
A module for finding, managing, and using fonts across platforms.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** FontPath, FontEntry, FontProperties, _JSONEncoder, FontManager
- **funkcje:** `_normalize_weight`, `get_fontext_synonyms`, `list_fonts`, `win32FontDirectory`, `_get_win32_installed_fonts`, `_get_fontconfig_fonts`, `_get_macos_fonts`, `findSystemFonts`, `ttfFontProperty`, `_get_font_alt_names`, `afmFontProperty`, `_cleanup_fontproperties_init`, `_json_decode`, `json_dump`, `json_load`, `is_opentype_cff_font`, `_get_font`, `_cached_realpath`, `get_font`, `_load_fontmanager`, `path`, `face_index`, `_as_tuple`, `_repr_html_`, `_repr_png_`, `get_weight`, `_weight_from_subfam`, `_try_add`, `wrapper`, `_from_any`

## Opis
A module for finding, managing, and using fonts across platforms.

This module provides a single `FontManager` instance, ``fontManager``, that can
be shared across backends and platforms.  The `findfont`
function returns the best TrueType (TTF) font file in the local or
system font path that matches the specified `FontProperties`
instance.  The `FontManager` also handles Adobe Font Metrics
(AFM) f
