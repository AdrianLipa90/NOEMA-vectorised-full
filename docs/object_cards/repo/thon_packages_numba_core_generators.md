# generators.py — .python_packages/numba/core/generators.py

## Tożsamość
- **id_karty:** `REPO-GENERATORS-1CA1`
- **ścieżka:** `.python_packages/numba/core/generators.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.621`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/numba/core/generators.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.621 |
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
Support for lowering generators.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** GeneratorDescriptor, BaseGeneratorLower, GeneratorLower, PyGeneratorLower, LowerYield
- **funkcje:** `from_generator_fndesc`, `llvm_finalizer_name`, `call_conv`, `get_args_ptr`, `get_resume_index_ptr`, `get_state_ptr`, `lower_init_func`, `lower_next_func`, `lower_finalize_func`, `return_from_generator`, `create_resumption_block`, `debug_print`, `get_generator_type`, `box_generator_struct`, `lower_finalize_func_body`, `get_generator_type`, `box_generator_struct`, `init_generator_state`, `lower_finalize_func_body`, `lower_yield_suspend`, `lower_yield_resume`

## Opis
Support for lowering generators.
