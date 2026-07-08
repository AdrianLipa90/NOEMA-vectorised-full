# sleep_scheduler.py — runtime/ciel_omega/memory/sleep_scheduler.py

## Tożsamość
- **id_karty:** `REPO-SLEEP_SCHEDULER-D8CB`
- **ścieżka:** `runtime/ciel_omega/memory/sleep_scheduler.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.155`
- **masa_semantyczna:** `0.40`

## Kotwice
- `runtime/ciel_omega/memory/sleep_scheduler.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.155 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_OBLIGATION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.59271`
- **R₃:** `0.552945`
- **R₆:** `0.534582`
- **R₉:** `0.582078`
- **potencjal_kappa:** `0.23834`
- **masa_semantyczna:** `-0.091456`
- **rodzaj_karty:** `0.276031`


## Rola
Cadence scheduler for the sleep-mode consolidation job.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** SleepSchedulerConfig, SleepSchedulerCycle, SleepModeScheduler
- **funkcje:** `_utc_now_iso`, `_normalize_load`, `_idle_gate`, `_existing_paths`, `build_sleep_scheduler`, `as_dict`, `idle_gate`, `should_run`, `run_once`, `run_forever`, `_write_state`

## Opis
Cadence scheduler for the sleep-mode consolidation job.
