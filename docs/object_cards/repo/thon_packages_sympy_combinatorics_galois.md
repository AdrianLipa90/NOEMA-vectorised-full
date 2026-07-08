# galois.py — .python_packages/sympy/combinatorics/galois.py

## Tożsamość
- **id_karty:** `REPO-GALOIS-88F8`
- **ścieżka:** `.python_packages/sympy/combinatorics/galois.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.410`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/combinatorics/galois.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.410 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ADDITION`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.662589`
- **R₃:** `0.614656`
- **R₆:** `0.542851`
- **R₉:** `0.417608`
- **potencjal_kappa:** `0.07638`
- **masa_semantyczna:** `0.206164`
- **rodzaj_karty:** `0.259027`


## Rola
Construct transitive subgroups of symmetric groups, useful in Galois theory.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** S1TransitiveSubgroups, S2TransitiveSubgroups, S3TransitiveSubgroups, S4TransitiveSubgroups, S5TransitiveSubgroups, S6TransitiveSubgroups
- **funkcje:** `four_group`, `M20`, `S3_in_S6`, `A4_in_S6`, `S4m`, `S4p`, `A4xC2`, `S4xC2`, `G18`, `G36m`, `G36p`, `G72`, `PSL2F5`, `PGL2F5`, `find_transitive_subgroups_of_S6`, `get_perm_group`, `get_perm_group`, `get_perm_group`, `get_perm_group`, `get_perm_group`, `get_perm_group`, `elts_by_order`, `order_profile`, `search`, `match_known_group`, `finish_up`

## Opis
Construct transitive subgroups of symmetric groups, useful in Galois theory.

Besides constructing instances of the :py:class:`~.PermutationGroup` class to
represent the transitive subgroups of $S_n$ for small $n$, this module provides
*names* for these groups.

In some applications, it may be preferable to know the name of a group,
rather than receive an instance of the :py:class:`~.PermutationGr
