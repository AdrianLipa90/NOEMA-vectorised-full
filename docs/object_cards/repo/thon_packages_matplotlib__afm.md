# _afm.py — .python_packages/matplotlib/_afm.py

## Tożsamość
- **id_karty:** `REPO-_AFM-528E`
- **ścieżka:** `.python_packages/matplotlib/_afm.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.292`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/_afm.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.292 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_NECESSITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.449701`
- **R₃:** `0.392905`
- **R₆:** `0.402231`
- **R₉:** `0.439135`
- **potencjal_kappa:** `-0.089486`
- **masa_semantyczna:** `-0.210953`
- **rodzaj_karty:** `0.286192`


## Rola
A Python interface to Adobe Font Metrics Files.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** FontMetricsHeader, CharMetrics, CompositePart, AFM
- **funkcje:** `_to_int`, `_to_float`, `_to_str`, `_to_list_of_ints`, `_to_list_of_floats`, `_to_bool`, `_parse_header`, `_parse_char_metrics`, `_parse_kern_pairs`, `_parse_composites`, `_parse_optional`, `get_str_bbox_and_descent`, `get_glyph_name`, `get_char_index`, `get_width_char`, `get_width_from_char_name`, `get_kern_dist_from_name`, `get_fontname`, `postscript_name`, `get_fullname`, `get_familyname`, `family_name`, `get_weight`, `get_angle`, `get_ascender`, `get_capheight`, `get_descender`, `get_xheight`, `get_underline_thickness`

## Opis
A Python interface to Adobe Font Metrics Files.

Although a number of other Python implementations exist, and may be more
complete than this, it was decided not to go with them because they were
either:

1) copyrighted or used a non-BSD compatible license
2) had too many dependencies and a free standing lib was needed
3) did more than needed and it was easier to write afresh rather than
   figure
