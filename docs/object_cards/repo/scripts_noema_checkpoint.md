# noema_checkpoint.py — scripts/noema_checkpoint.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_CHECKPOINT-2C31`
- **ścieżka:** `scripts/noema_checkpoint.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `0.463`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_checkpoint.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 0.463 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `RETURN`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.642878`
- **R₃:** `0.503912`
- **R₆:** `0.555289`
- **R₉:** `0.707983`
- **potencjal_kappa:** `-0.270999`
- **masa_semantyczna:** `-0.074142`
- **rodzaj_karty:** `0.291714`


## Rola
NOEMA Checkpoint System — interaktywna checklista przed odpowiedzią.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_ok`, `_warn`, `_fail`, `_check_surface`, `_check_files`, `_check_task_queue`, `_check_agent_hint`, `_check_state_files`, `_check_lessons_reminder`, `run_checkpoint`

## Opis
NOEMA Checkpoint System — interaktywna checklista przed odpowiedzią.

Usage:
    python3 scripts/noema_checkpoint.py          # pełny checkpoint
    python3 scripts/noema_checkpoint.py --quick   # szybki (tylko krytyczne)
    python3 scripts/noema_checkpoint.py --json    # JSON output dla agenta
