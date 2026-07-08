# env_class.py — .python_packages/mypyc/irbuild/env_class.py

## Tożsamość
- **id_karty:** `REPO-ENV_CLASS-E6FF`
- **ścieżka:** `.python_packages/mypyc/irbuild/env_class.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.991`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/irbuild/env_class.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.991 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `BOUNDARY`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.587016`
- **R₃:** `0.481937`
- **R₆:** `0.525424`
- **R₉:** `0.380572`
- **potencjal_kappa:** `-0.130804`
- **masa_semantyczna:** `0.12548`
- **rodzaj_karty:** `0.280526`


## Rola
Generate classes representing function environments (+ related operations).

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `setup_env_class`, `finalize_env_class`, `instantiate_env_class`, `load_env_registers`, `load_outer_env`, `load_outer_envs`, `num_bitmap_args`, `add_args_to_env`, `add_vars_to_env`, `setup_func_for_recursive_call`, `is_free_variable`

## Opis
Generate classes representing function environments (+ related operations).

If we have a nested function that has non-local (free) variables, access to the
non-locals is via an instance of an environment class. Example:

    def f() -> int:
        x = 0  # Make 'x' an attribute of an environment class instance

        def g() -> int:
            # We have access to the environment class instanc
