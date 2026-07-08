# image.py — .python_packages/matplotlib/image.py

## Tożsamość
- **id_karty:** `REPO-IMAGE-3480`
- **ścieżka:** `.python_packages/matplotlib/image.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.130`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/image.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.130 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `FOLD`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.351212`
- **R₃:** `0.661831`
- **R₆:** `0.649218`
- **R₉:** `0.522246`
- **potencjal_kappa:** `-0.135067`
- **masa_semantyczna:** `-0.137397`
- **rodzaj_karty:** `0.29302`


## Rola
The image module supports basic image loading, rescaling and display

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** _ImageBase, AxesImage, NonUniformImage, PcolorImage, FigureImage, BboxImage
- **funkcje:** `composite_images`, `_draw_list_compositing_images`, `_resample`, `_rgb_to_rgba`, `imread`, `imsave`, `pil_to_array`, `_pil_png_to_float_array`, `thumbnail`, `get_size`, `get_shape`, `set_alpha`, `_get_scalar_alpha`, `changed`, `_make_image`, `make_image`, `_check_unsampled_image`, `draw`, `contains`, `write_png`, `_normalize_image_array`, `set_data`, `set_array`, `get_interpolation`, `set_interpolation`, `get_interpolation_stage`, `set_interpolation_stage`, `can_composite`, `set_resample`, `get_resample`

## Opis
The image module supports basic image loading, rescaling and display
operations.
