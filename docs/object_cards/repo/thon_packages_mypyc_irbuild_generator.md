# generator.py — .python_packages/mypyc/irbuild/generator.py

## Tożsamość
- **id_karty:** `REPO-GENERATOR-0951`
- **ścieżka:** `.python_packages/mypyc/irbuild/generator.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.460`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/irbuild/generator.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.460 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `WARP_DRIFT`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.47403`
- **R₃:** `0.56672`
- **R₆:** `0.57902`
- **R₉:** `0.540967`
- **potencjal_kappa:** `0.057762`
- **masa_semantyczna:** `0.153958`
- **rodzaj_karty:** `0.289083`


## Rola
Generate IR for generator functions.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `gen_generator_func`, `gen_generator_func_body`, `instantiate_generator_class`, `setup_generator_class`, `create_switch_for_generator_class`, `populate_switch_for_generator_class`, `add_raise_exception_blocks_to_generator_class`, `add_methods_to_generator_class`, `add_helper_to_generator_class`, `add_iter_to_generator_class`, `add_next_to_generator_class`, `add_send_to_generator_class`, `add_throw_to_generator_class`, `add_close_to_generator_class`, `add_await_to_generator_class`, `setup_env_for_generator_class`

## Opis
Generate IR for generator functions.

A generator function is represented by a class that implements the
generator protocol and keeps track of the generator state, including
local variables.

The top-level logic for dealing with generator functions is in
mypyc.irbuild.function.
