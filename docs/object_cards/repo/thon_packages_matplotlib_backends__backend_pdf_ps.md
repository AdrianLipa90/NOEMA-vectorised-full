# _backend_pdf_ps.py — .python_packages/matplotlib/backends/_backend_pdf_ps.py

## Tożsamość
- **id_karty:** `REPO-_BACKEND_PDF_PS-A8FA`
- **ścieżka:** `.python_packages/matplotlib/backends/_backend_pdf_ps.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.188`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/backends/_backend_pdf_ps.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.188 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SIMULATION_BOUNDARY`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.575665`
- **R₃:** `0.306554`
- **R₆:** `0.381064`
- **R₉:** `0.528951`
- **potencjal_kappa:** `-0.226686`
- **masa_semantyczna:** `-0.021063`
- **rodzaj_karty:** `0.269599`


## Rola
Common functionality between the PDF and PS backends.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** GlyphMap, CharacterTracker, RendererPDFPSBase
- **funkcje:** `_cached_get_afm_from_fname`, `get_glyphs_subset`, `font_as_file`, `get`, `iget`, `add`, `track`, `track_glyph`, `subset_to_unicode`, `flipy`, `option_scale_image`, `option_image_nocomposite`, `get_canvas_width_height`, `_get_font_height_metrics`, `get_text_width_height_descent`, `_get_font_afm`, `_get_font_ttf`

## Opis
Common functionality between the PDF and PS backends.
