# callable_class.py — .python_packages/mypyc/irbuild/callable_class.py

## Tożsamość
- **id_karty:** `REPO-CALLABLE_CLASS-3BEF`
- **ścieżka:** `.python_packages/mypyc/irbuild/callable_class.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.896`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/irbuild/callable_class.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.896 |
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
Generate a class that represents a nested function.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `setup_callable_class`, `add_coroutine_properties`, `add_call_to_callable_class`, `add_get_to_callable_class`, `instantiate_callable_class`, `get_func_wrapper`

## Opis
Generate a class that represents a nested function.

The class defines __call__ for calling the function and allows access to
non-local variables defined in outer scopes.
