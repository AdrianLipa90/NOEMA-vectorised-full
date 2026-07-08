# axes3d.py — .python_packages/mpl_toolkits/mplot3d/axes3d.py

## Tożsamość
- **id_karty:** `REPO-AXES3D-A481`
- **ścieżka:** `.python_packages/mpl_toolkits/mplot3d/axes3d.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.852`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mpl_toolkits/mplot3d/axes3d.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.852 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `NEGATION`
- **odcisk_harmoniczny:** `LHLL`
- **R₁:** `0.425094`
- **R₃:** `0.614676`
- **R₆:** `0.450577`
- **R₉:** `0.387679`
- **potencjal_kappa:** `0.085998`
- **masa_semantyczna:** `-0.143065`
- **rodzaj_karty:** `0.271614`


## Rola
axes3d.py, original mplot3d version by John Porter

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Axes3D, _Quaternion
- **funkcje:** `get_test_data`, `set_axis_off`, `set_axis_on`, `convert_zunits`, `set_top_view`, `_init_axis`, `get_zaxis`, `_transformed_cube`, `_update_transScale`, `set_aspect`, `_equal_aspect_axis_indices`, `set_box_aspect`, `apply_aspect`, `draw`, `get_axis_position`, `update_datalim`, `get_zmargin`, `set_zmargin`, `margins`, `autoscale`, `auto_scale_xyz`, `_autoscale_axis`, `autoscale_view`, `get_w_lims`, `_set_bound3d`, `set_xbound`, `set_ybound`, `set_zbound`, `_set_lim3d`, `set_xlim`

## Opis
axes3d.py, original mplot3d version by John Porter
Created: 23 Sep 2005

Parts fixed by Reinier Heeres <reinier@heeres.eu>
Minor additions by Ben Axelrod <baxelrod@coroware.com>
Significant updates and revisions by Ben Root <ben.v.root@gmail.com>

Module containing Axes3D, an object which can plot 3D objects on a
2D matplotlib figure.

Coordinate Systems
------------------
3D plotting involves sev
