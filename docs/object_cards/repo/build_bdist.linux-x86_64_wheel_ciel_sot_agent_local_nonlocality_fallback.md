# local_nonlocality_fallback.py — build/bdist.linux-x86_64/wheel/ciel_sot_agent/local_nonlocality_fallback.py

## Tożsamość
- **id_karty:** `REPO-LOCAL_NONLOCALITY_FA-C067`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_sot_agent/local_nonlocality_fallback.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `6.091`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_sot_agent/local_nonlocality_fallback.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 6.091 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
Local Nonlocality Fallback — PC state as hidden-channel phase source.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_read_cpu_percent`, `_read_mem_percent`, `_read_load_avg`, `_read_process_count`, `_read_disk_bytes`, `_read_net_bytes`, `_time_of_day_phase`, `read_pc_phases`, `_run_eba_with_hidden`, `_aggregate_eba`, `run_local_nonlocality_fallback`, `merge_with_canonical`, `save_report`, `load_last_report`, `main`, `_sample`, `_n`

## Opis
Local Nonlocality Fallback — PC state as hidden-channel phase source.

When the canonical HolonomicMemoryOrchestrator produces low nonlocal_coherent_fraction
(< 0.40), this module derives 8 hidden-state phases from live PC metrics and re-runs
EBA loop evaluation with these richer hidden states.

PC metrics → memory channel phase mapping (M0-M7):
    M0 Perceptual      ← CPU usage %
    M1 Working
