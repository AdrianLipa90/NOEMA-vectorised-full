# scope.py — .python_packages/mypy/scope.py

## Tożsamość
- **id_karty:** `REPO-SCOPE-8FCA`
- **ścieżka:** `.python_packages/mypy/scope.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.190`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/scope.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.190 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `COMPOSITION`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.528337`
- **R₃:** `0.492776`
- **R₆:** `0.696453`
- **R₉:** `0.565583`
- **potencjal_kappa:** `0.185923`
- **masa_semantyczna:** `-0.141173`
- **rodzaj_karty:** `0.274318`


## Rola
Track current scope to easily calculate the corresponding fine-grained target.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** Scope
- **funkcje:** `current_module_id`, `current_target`, `current_full_target`, `current_type_name`, `current_function_name`, `module_scope`, `function_scope`, `outer_functions`, `enter_class`, `leave_class`, `class_scope`, `save`, `saved_scope`

## Opis
Track current scope to easily calculate the corresponding fine-grained target.

TODO: Use everywhere where we track targets, including in mypy.errors.
