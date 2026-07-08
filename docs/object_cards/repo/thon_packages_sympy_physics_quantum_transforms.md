# transforms.py — .python_packages/sympy/physics/quantum/transforms.py

## Tożsamość
- **id_karty:** `REPO-TRANSFORMS-6FC9`
- **ścieżka:** `.python_packages/sympy/physics/quantum/transforms.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.237`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/physics/quantum/transforms.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.237 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ATTRACTOR`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.476161`
- **R₃:** `0.526498`
- **R₆:** `0.547584`
- **R₉:** `0.472579`
- **potencjal_kappa:** `4.910705`
- **masa_semantyczna:** `13.031004`
- **rodzaj_karty:** `1.5`


## Rola
Transforms that are always applied to quantum expressions.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_transform_expr`, `_transform_bra_ket`, `_transform_ket_bra`, `_transform_ket_ket`, `_transform_bra_bra`, `_transform_op_ket`, `_transform_bra_op`, `_transform_tp_ket`, `_transform_ket_tp`, `_transform_tp_bra`, `_transform_bra_tp`, `_transform_tp_tp`, `_transform_op_op`, `_postprocess_state_mul`, `_postprocess_state_pow`, `_postprocess_tp_pow`

## Opis
Transforms that are always applied to quantum expressions.

This module uses the kind and _constructor_postprocessor_mapping APIs
to transform different combinations of Operators, Bras, and Kets into
Inner/Outer/TensorProducts. These transformations are registered
with the postprocessing API of core classes like `Mul` and `Pow` and
are always applied to any expression involving Bras, Kets, and
Ope
