# cnf.py — .python_packages/sympy/assumptions/cnf.py

## Tożsamość
- **id_karty:** `REPO-CNF-1D4D`
- **ścieżka:** `.python_packages/sympy/assumptions/cnf.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.496`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/sympy/assumptions/cnf.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.496 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `AFFECT`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.542195`
- **R₃:** `0.629813`
- **R₆:** `0.534142`
- **R₉:** `0.565106`
- **potencjal_kappa:** `0.141102`
- **masa_semantyczna:** `0.203631`
- **rodzaj_karty:** `0.326785`


## Rola
The classes used here are for the internal use of assumptions system

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Literal, OR, AND, CNF, EncodedCNF
- **funkcje:** `to_NNF`, `distribute_AND_over_OR`, `arg`, `rcall`, `args`, `rcall`, `args`, `rcall`, `add`, `extend`, `copy`, `add_clauses`, `from_prop`, `all_predicates`, `_or`, `_and`, `_not`, `rcall`, `all_or`, `all_and`, `to_CNF`, `CNF_to_cnf`, `from_cnf`, `symbols`, `variables`, `copy`, `add_prop`, `add_from_cnf`, `encode_arg`, `encode`

## Opis
The classes used here are for the internal use of assumptions system
only and should not be used anywhere else as these do not possess the
signatures common to SymPy objects. For general use of logic constructs
please refer to sympy.logic classes And, Or, Not, etc.
