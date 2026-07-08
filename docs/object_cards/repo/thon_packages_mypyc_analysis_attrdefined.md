# attrdefined.py — .python_packages/mypyc/analysis/attrdefined.py

## Tożsamość
- **id_karty:** `REPO-ATTRDEFINED-A376`
- **ścieżka:** `.python_packages/mypyc/analysis/attrdefined.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.232`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/analysis/attrdefined.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.232 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ASSERTION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.563342`
- **R₃:** `0.601856`
- **R₆:** `0.54039`
- **R₉:** `0.584219`
- **potencjal_kappa:** `-0.098441`
- **masa_semantyczna:** `0.347732`
- **rodzaj_karty:** `0.261593`


## Rola
Always defined attribute analysis.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** AttributeMaybeDefinedVisitor, AttributeMaybeUndefinedVisitor
- **funkcje:** `analyze_always_defined_attrs`, `analyze_always_defined_attrs_in_class`, `find_always_defined_attributes`, `find_sometimes_defined_attributes`, `mark_attr_initialization_ops`, `attributes_initialized_by_init_call`, `attributes_maybe_initialized_by_init_call`, `analyze_maybe_defined_attrs_in_init`, `analyze_maybe_undefined_attrs_in_init`, `update_always_defined_attrs_using_subclasses`, `detect_undefined_bitmap`, `visit_branch`, `visit_return`, `visit_unreachable`, `visit_register_op`, `visit_assign`, `visit_assign_multi`, `visit_set_mem`, `visit_branch`, `visit_return`, `visit_unreachable`, `visit_register_op`, `visit_assign`, `visit_assign_multi`, `visit_set_mem`

## Opis
Always defined attribute analysis.

An always defined attribute has some statements in __init__ or the
class body that cause the attribute to be always initialized when an
instance is constructed. It must also not be possible to read the
attribute before initialization, and it can't be deletable.

We can assume that the value is always defined when reading an always
defined attribute. Otherwise we
