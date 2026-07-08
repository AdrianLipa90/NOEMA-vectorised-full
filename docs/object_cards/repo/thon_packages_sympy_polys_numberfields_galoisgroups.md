# galoisgroups.py — .python_packages/sympy/polys/numberfields/galoisgroups.py

## Tożsamość
- **id_karty:** `REPO-GALOISGROUPS-E9A3`
- **ścieżka:** `.python_packages/sympy/polys/numberfields/galoisgroups.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.718`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/polys/numberfields/galoisgroups.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.718 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `COMPOSITION`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.528337`
- **R₃:** `0.492776`
- **R₆:** `0.696453`
- **R₉:** `0.565583`
- **potencjal_kappa:** `0.185923`
- **masa_semantyczna:** `-0.141173`
- **rodzaj_karty:** `0.274318`


## Rola
Compute Galois groups of polynomials.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** MaxTriesException
- **funkcje:** `tschirnhausen_transformation`, `has_square_disc`, `_galois_group_degree_3`, `_galois_group_degree_4_root_approx`, `_galois_group_degree_4_lookup`, `_galois_group_degree_5_hybrid`, `_galois_group_degree_5_lookup_ext_factor`, `_galois_group_degree_6_lookup`, `galois_group`, `get_coeff_generator`

## Opis
Compute Galois groups of polynomials.

We use algorithms from [1], with some modifications to use lookup tables for
resolvents.

References
==========

.. [1] Cohen, H. *A Course in Computational Algebraic Number Theory*.
