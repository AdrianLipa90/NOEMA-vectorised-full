# classdef.py — .python_packages/mypyc/irbuild/classdef.py

## Tożsamość
- **id_karty:** `REPO-CLASSDEF-7DA0`
- **ścieżka:** `.python_packages/mypyc/irbuild/classdef.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.410`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/irbuild/classdef.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.410 |
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
Transform class definitions from the mypy AST form to IR.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ClassBuilder, NonExtClassBuilder, ExtClassBuilder, DataClassBuilder, AttrsClassBuilder
- **funkcje:** `transform_class_def`, `allocate_class`, `make_generic_base_class`, `populate_non_ext_bases`, `find_non_ext_metaclass`, `setup_non_ext_dict`, `add_non_ext_class_attr_ann`, `add_non_ext_class_attr`, `find_attr_initializers`, `generate_attr_defaults_init`, `check_deletable_declaration`, `create_ne_from_eq`, `gen_glue_ne_method`, `load_non_ext_class`, `load_decorated_class`, `cache_class_attrs`, `create_mypyc_attrs_tuple`, `add_dunders_to_non_ext_dict`, `add_method`, `add_attr`, `finalize`, `class_body_obj`, `class_body_obj`, `create_non_ext_info`, `add_method`, `add_attr`, `finalize`, `class_body_obj`, `skip_attr_default`, `add_method`

## Opis
Transform class definitions from the mypy AST form to IR.
