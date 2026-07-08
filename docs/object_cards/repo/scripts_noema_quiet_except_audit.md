# noema_quiet_except_audit.py — scripts/noema_quiet_except_audit.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_QUIET_EXCEPT_A-6C14`
- **ścieżka:** `scripts/noema_quiet_except_audit.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `5.044`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_quiet_except_audit.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 5.044 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

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
NOEMA AST audit for quiet exception handlers.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_skip`, `_segment`, `_exception_name`, `_is_logging_or_raise`, `_handler_has_logging_or_raise`, `_body_action`, `_quiet_reason`, `_scope_for`, `_scan_file`, `run_audit`

## Opis
NOEMA AST audit for quiet exception handlers.

The audit does not use grep-like text matching. It parses Python files with
`ast` and reports exception handlers that swallow errors without logging or
raising.
