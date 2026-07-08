# local_nonlocality_fallback.py — src/ciel_sot_agent/local_nonlocality_fallback.py

## Tożsamość
- **id_karty:** `REPO-LOCAL_NONLOCALITY_FA-4F45`
- **ścieżka:** `src/ciel_sot_agent/local_nonlocality_fallback.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `0.205`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/local_nonlocality_fallback.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 0.205 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

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
