# ll_builder.py — .python_packages/mypyc/irbuild/ll_builder.py

## Tożsamość
- **id_karty:** `REPO-LL_BUILDER-C5AF`
- **ścieżka:** `.python_packages/mypyc/irbuild/ll_builder.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.622`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/irbuild/ll_builder.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.622 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SIMULATION_BOUNDARY`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.575665`
- **R₃:** `0.306554`
- **R₆:** `0.381064`
- **R₉:** `0.528951`
- **potencjal_kappa:** `-0.226686`
- **masa_semantyczna:** `-0.021063`
- **rodzaj_karty:** `0.269599`


## Rola
A "low-level" IR builder class.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** LowLevelIRBuilder, ForBuilder
- **funkcje:** `num_positional_args`, `set_module`, `add`, `assign`, `goto`, `activate_block`, `goto_and_activate`, `keep_alive`, `load_mem`, `set_mem`, `get_element`, `load_address`, `load_global`, `load_builtin`, `load_struct_field`, `set_struct_field`, `push_error_handler`, `pop_error_handler`, `self`, `flush_keep_alives`, `debug_print`, `box`, `unbox_or_cast`, `coerce`, `coerce_int_to_fixed_width`, `check_fixed_width_range`, `coerce_tagged_to_fixed_width_with_range_check`, `emit_fixed_width_overflow_error`, `coerce_short_int_to_fixed_width`, `coerce_fixed_width_to_int`

## Opis
A "low-level" IR builder class.

See the docstring of class LowLevelIRBuilder for more information.
