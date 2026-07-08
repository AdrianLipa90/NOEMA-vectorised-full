# builder.py — .python_packages/mypyc/irbuild/builder.py

## Tożsamość
- **id_karty:** `REPO-BUILDER-9ED7`
- **ścieżka:** `.python_packages/mypyc/irbuild/builder.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.420`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/irbuild/builder.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.420 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `TRANSFORM`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.489274`
- **R₃:** `0.512237`
- **R₆:** `0.547669`
- **R₉:** `0.477906`
- **potencjal_kappa:** `0.124323`
- **masa_semantyczna:** `-0.167832`
- **rodzaj_karty:** `0.281825`


## Rola
Builder class to transform a mypy AST to the IR form.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** IRVisitor, UnsupportedException, IRBuilder
- **funkcje:** `gen_arg_defaults`, `remangle_redefinition_name`, `get_call_target_fullname`, `create_type_params`, `calculate_arg_defaults`, `set_module`, `accept`, `accept`, `accept`, `flush_keep_alives`, `add`, `goto`, `activate_block`, `goto_and_activate`, `self`, `py_get_attr`, `load_str`, `load_bytes_from_str_literal`, `load_int`, `load_float`, `unary_op`, `binary_op`, `coerce`, `none_object`, `none`, `true`, `false`, `new_list_op`, `new_set_op`, `translate_is_op`

## Opis
Builder class to transform a mypy AST to the IR form.

See the docstring of class IRBuilder for more information.
