# modules.py — .python_packages/sympy/polys/numberfields/modules.py

## Tożsamość
- **id_karty:** `REPO-MODULES-C5B9`
- **ścieżka:** `.python_packages/sympy/polys/numberfields/modules.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.750`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/polys/numberfields/modules.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.750 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ACTION_REQUEST`
- **odcisk_harmoniczny:** `LLHL`
- **R₁:** `0.419252`
- **R₃:** `0.442825`
- **R₆:** `0.60198`
- **R₉:** `0.41548`
- **potencjal_kappa:** `-0.118614`
- **masa_semantyczna:** `0.191681`
- **rodzaj_karty:** `0.278922`


## Rola
Modules in number fields.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Module, PowerBasis, Submodule, ModuleElement, PowerBasisElement, ModuleHomomorphism, ModuleEndomorphism, InnerEndomorphism, EndomorphismRing
- **funkcje:** `to_col`, `is_sq_maxrank_HNF`, `make_mod_elt`, `find_min_poly`, `n`, `mult_tab`, `parent`, `represent`, `ancestors`, `power_basis_ancestor`, `nearest_common_ancestor`, `number_field`, `is_compat_col`, `starts_with_unity`, `basis_elements`, `zero`, `one`, `element_from_rational`, `submodule_from_gens`, `submodule_from_matrix`, `whole_submodule`, `endomorphism_ring`, `number_field`, `n`, `mult_tab`, `compute_mult_tab`, `represent`, `starts_with_unity`, `element_from_rational`, `element_from_poly`

## Opis
Modules in number fields.

The classes defined here allow us to work with finitely generated, free
modules, whose generators are algebraic numbers.

There is an abstract base class called :py:class:`~.Module`, which has two
concrete subclasses, :py:class:`~.PowerBasis` and :py:class:`~.Submodule`.

Every module is defined by its basis, or set of generators:

* For a :py:class:`~.PowerBasis`, the g
