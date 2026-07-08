# dviread.py — .python_packages/matplotlib/dviread.py

## Tożsamość
- **id_karty:** `REPO-DVIREAD-8E2D`
- **ścieżka:** `.python_packages/matplotlib/dviread.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.448`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/dviread.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.448 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ORDER`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.408132`
- **R₃:** `0.527143`
- **R₆:** `0.447287`
- **R₉:** `0.516074`
- **potencjal_kappa:** `0.213299`
- **masa_semantyczna:** `0.199346`
- **rodzaj_karty:** `0.279908`


## Rola
A module for reading dvi files output by TeX. Several limitations make

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Text, Dvi, DviFont, Vf, TexMetrics, Tfm, TtfMetrics, PsfontsMap, _LuatexKpsewhich
- **funkcje:** `_dispatch`, `_mul1220`, `_parse_enc`, `find_tex_file`, `_fontfile`, `index`, `glyph_name_or_index`, `_as_unicode_or_name`, `decorate`, `close`, `_output`, `_read`, `_read_arg`, `_set_char_immediate`, `_set_char`, `_set_rule`, `_put_char`, `_put_char_real`, `_put_rule`, `_put_rule_real`, `_nop`, `_bop`, `_eop`, `_push`, `_pop`, `_right`, `_right_w`, `_right_x`, `_down`, `_down_y`

## Opis
A module for reading dvi files output by TeX. Several limitations make
this not (currently) useful as a general-purpose dvi preprocessor, but
it is currently used by the pdf backend for processing usetex text.

Interface::

  with Dvi(filename, 72) as dvi:
      # iterate over pages:
      for page in dvi:
          w, h, d = page.width, page.height, page.descent
          for x, y, font, glyph, w
