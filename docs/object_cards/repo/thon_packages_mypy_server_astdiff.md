# astdiff.py — .python_packages/mypy/server/astdiff.py

## Tożsamość
- **id_karty:** `REPO-ASTDIFF-C5F8`
- **ścieżka:** `.python_packages/mypy/server/astdiff.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.616`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/server/astdiff.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.616 |
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
Utilities for comparing two versions of a module symbol table.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** SnapshotTypeVisitor
- **funkcje:** `compare_symbol_table_snapshots`, `snapshot_symbol_table`, `snapshot_definition`, `snapshot_type`, `snapshot_optional_type`, `snapshot_types`, `snapshot_simple_type`, `encode_optional_str`, `snapshot_untyped_signature`, `visit_unbound_type`, `visit_any`, `visit_none_type`, `visit_uninhabited_type`, `visit_erased_type`, `visit_deleted_type`, `visit_instance`, `visit_type_var`, `visit_param_spec`, `visit_type_var_tuple`, `visit_unpack_type`, `visit_parameters`, `visit_callable_type`, `normalize_callable_variables`, `visit_tuple_type`, `visit_typeddict_type`, `visit_literal_type`, `visit_union_type`, `visit_overloaded`, `visit_partial_type`, `visit_type_type`

## Opis
Utilities for comparing two versions of a module symbol table.

The goal is to find which AST nodes have externally visible changes, so
that we can fire triggers and re-process other parts of the program
that are stale because of the changes.

Only look at detail at definitions at the current module -- don't
recurse into other modules.

A summary of the module contents:

* snapshot_symbol_table(..
