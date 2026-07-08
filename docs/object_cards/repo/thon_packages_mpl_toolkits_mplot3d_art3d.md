# art3d.py — .python_packages/mpl_toolkits/mplot3d/art3d.py

## Tożsamość
- **id_karty:** `REPO-ART3D-CD13`
- **ścieżka:** `.python_packages/mpl_toolkits/mplot3d/art3d.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.808`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mpl_toolkits/mplot3d/art3d.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.808 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `PAUSE`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.508756`
- **R₃:** `0.557009`
- **R₆:** `0.421727`
- **R₉:** `0.55292`
- **potencjal_kappa:** `-0.020552`
- **masa_semantyczna:** `0.206252`
- **rodzaj_karty:** `0.260435`


## Rola
Module containing 3D artist code and functions to convert 2D

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Text3D, Line3D, Collection3D, Line3DCollection, Patch3D, PathPatch3D, Patch3DCollection, Path3DCollection, Poly3DCollection
- **funkcje:** `_norm_angle`, `_norm_text_angle`, `get_dir_vector`, `_viewlim_mask`, `_scale_invalid_mask`, `text_2d_to_3d`, `line_2d_to_3d`, `_path_to_3d_segment`, `_paths_to_3d_segments`, `_path_to_3d_segment_with_codes`, `_paths_to_3d_segments_with_codes`, `collection_2d_to_3d`, `line_collection_2d_to_3d`, `_get_patch_verts`, `patch_2d_to_3d`, `pathpatch_2d_to_3d`, `_get_data_scale`, `patch_collection_2d_to_3d`, `poly_collection_2d_to_3d`, `juggle_axes`, `rotate_axes`, `_zalpha`, `_all_points_on_plane`, `_generate_normals`, `_shade_colors`, `get_position_3d`, `set_position_3d`, `set_z`, `set_3d_properties`, `draw`

## Opis
Module containing 3D artist code and functions to convert 2D
artists into 3D versions which can be added to an Axes3D.
