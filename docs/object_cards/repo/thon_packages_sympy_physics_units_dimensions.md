# dimensions.py — .python_packages/sympy/physics/units/dimensions.py

## Tożsamość
- **id_karty:** `REPO-DIMENSIONS-62A8`
- **ścieżka:** `.python_packages/sympy/physics/units/dimensions.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.895`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/physics/units/dimensions.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.895 |
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
Definition of physical dimensions.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** _QuantityMapper, Dimension, DimensionSystem
- **funkcje:** `set_quantity_dimension`, `set_quantity_scale_factor`, `get_quantity_dimension`, `get_quantity_scale_factor`, `name`, `symbol`, `_eval_power`, `_from_dimensional_dependencies`, `has_integer_powers`, `base_dims`, `derived_dims`, `dimensional_dependencies`, `_get_dimensional_dependencies_for_name`, `get_dimensional_dependencies`, `equivalent_dims`, `extend`, `is_dimensionless`, `list_can_dims`, `inv_can_transf_matrix`, `can_transf_matrix`, `dim_can_vector`, `dim_vector`, `print_dim_base`, `dim`, `is_consistent`, `parse_dim`, `parse_dim_name`, `parse_dict`

## Opis
Definition of physical dimensions.

Unit systems will be constructed on top of these dimensions.

Most of the examples in the doc use MKS system and are presented from the
computer point of view: from a human point, adding length to time is not legal
in MKS but it is in natural system; for a computer in natural system there is
no time dimension (but a velocity dimension instead) - in the basis - s
