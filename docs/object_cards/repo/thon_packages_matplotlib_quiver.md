# quiver.py — .python_packages/matplotlib/quiver.py

## Tożsamość
- **id_karty:** `REPO-QUIVER-EE79`
- **ścieżka:** `.python_packages/matplotlib/quiver.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.946`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/matplotlib/quiver.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.946 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `FORCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.552175`
- **R₃:** `0.435218`
- **R₆:** `0.571397`
- **R₉:** `0.579087`
- **potencjal_kappa:** `0.300939`
- **masa_semantyczna:** `0.016845`
- **rodzaj_karty:** `0.260112`


## Rola
Support for plotting vector fields.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** QuiverKey, Quiver, Barbs
- **funkcje:** `_parse_args`, `_check_consistent_shapes`, `labelsep`, `_init`, `_text_shift`, `draw`, `_set_transform`, `set_figure`, `contains`, `_init`, `get_datalim`, `draw`, `set_UVC`, `_dots_per_unit`, `_set_transform`, `_angles_lengths`, `_make_verts`, `_h_arrows`, `_find_tails`, `_make_barbs`, `set_UVC`, `set_offsets`

## Opis
Support for plotting vector fields.

Presently this contains Quiver and Barb. Quiver plots an arrow in the
direction of the vector, with the size of the arrow related to the
magnitude of the vector.

Barbs are like quiver in that they point along a vector, but
the magnitude of the vector is given schematically by the presence of barbs
or flags on the barb.

This will also become a home for things
