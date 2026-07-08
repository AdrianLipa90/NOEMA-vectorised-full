# homomorphisms.py — .python_packages/sympy/polys/agca/homomorphisms.py

## Tożsamość
- **id_karty:** `REPO-HOMOMORPHISMS-001E`
- **ścieżka:** `.python_packages/sympy/polys/agca/homomorphisms.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.285`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/polys/agca/homomorphisms.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.285 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `WARP_DRIFT`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.47403`
- **R₃:** `0.56672`
- **R₆:** `0.57902`
- **R₉:** `0.540967`
- **potencjal_kappa:** `0.057762`
- **masa_semantyczna:** `0.153958`
- **rodzaj_karty:** `0.289083`


## Rola
Computations with homomorphisms of modules and rings.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ModuleHomomorphism, MatrixHomomorphism, FreeModuleHomomorphism, SubModuleHomomorphism
- **funkcje:** `homomorphism`, `kernel`, `image`, `_kernel`, `_image`, `_restrict_domain`, `_restrict_codomain`, `_quotient_domain`, `_quotient_codomain`, `restrict_domain`, `restrict_codomain`, `quotient_domain`, `quotient_codomain`, `_apply`, `_compose`, `_mul_scalar`, `_add`, `_check_hom`, `is_injective`, `is_surjective`, `is_isomorphism`, `is_zero`, `_sympy_matrix`, `_restrict_domain`, `_restrict_codomain`, `_quotient_domain`, `_quotient_codomain`, `_add`, `_mul_scalar`, `_compose`

## Opis
Computations with homomorphisms of modules and rings.

This module implements classes for representing homomorphisms of rings and
their modules. Instead of instantiating the classes directly, you should use
the function ``homomorphism(from, to, matrix)`` to create homomorphism objects.
