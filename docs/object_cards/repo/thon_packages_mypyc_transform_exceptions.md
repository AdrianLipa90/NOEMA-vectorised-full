# exceptions.py — .python_packages/mypyc/transform/exceptions.py

## Tożsamość
- **id_karty:** `REPO-EXCEPTIONS-3DDC`
- **ścieżka:** `.python_packages/mypyc/transform/exceptions.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.707`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypyc/transform/exceptions.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.707 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ATTRACTOR`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.476161`
- **R₃:** `0.526498`
- **R₆:** `0.547584`
- **R₉:** `0.472579`
- **potencjal_kappa:** `4.910705`
- **masa_semantyczna:** `13.031004`
- **rodzaj_karty:** `1.5`


## Rola
Transform that inserts error checks after opcodes.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `insert_exception_handling`, `add_default_handler_block`, `split_blocks_at_errors`, `primitive_call`, `adjust_error_kinds`, `insert_overlapping_error_value_check`

## Opis
Transform that inserts error checks after opcodes.

When initially building the IR, the code doesn't perform error checks
for exceptions. This module is used to insert all required error checks
afterwards. Each Op describes how it indicates an error condition (if
at all).

We need to split basic blocks on each error check since branches can
only be placed at the end of a basic block.
