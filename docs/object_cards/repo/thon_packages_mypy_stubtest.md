# stubtest.py — .python_packages/mypy/stubtest.py

## Tożsamość
- **id_karty:** `REPO-STUBTEST-C41A`
- **ścieżka:** `.python_packages/mypy/stubtest.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.215`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/stubtest.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.215 |
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
Tests for stubs.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Missing, Unrepresentable, StubtestFailure, Error, Signature, _TypeCheckOnlyBaseMapper, _Arguments, SubClass
- **funkcje:** `_style`, `_truncate`, `silent_import_module`, `test_module`, `verify`, `_verify_exported_names`, `_module_symbol_table`, `verify_mypyfile`, `_is_decoratable`, `_verify_final`, `_shape_differs`, `_is_disjoint_base`, `_verify_disjoint_base`, `_verify_metaclass`, `verify_typeinfo`, `_static_lookup_runtime`, `_verify_static_class_methods`, `_verify_arg_name`, `_verify_arg_default_value`, `maybe_strip_cls`, `_verify_signature`, `_is_private_parameter`, `verify_funcitem`, `verify_missing`, `verify_var`, `verify_overloadedfuncdef`, `verify_typevarexpr`, `verify_paramspecexpr`, `_is_django_cached_property`, `_verify_readonly_property`

## Opis
Tests for stubs.

Verify that various things in stubs are consistent with how things behave at runtime.
