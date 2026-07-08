# htri_scheduler.py — src/ciel_sot_agent/htri_scheduler.py

## Tożsamość
- **id_karty:** `REPO-HTRI_SCHEDULER-2379`
- **ścieżka:** `src/ciel_sot_agent/htri_scheduler.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `3.373`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/htri_scheduler.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 3.373 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

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
HTRI Scheduler — adaptacyjny dense matrix scheduler.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_htri_path`, `_gpu_runtime`, `_ram_free_gb`, `_cpu_load`, `_auto_power_mode`, `run`, `get_state`, `get_optimal_threads`

## Opis
HTRI Scheduler — adaptacyjny dense matrix scheduler.

Trzy poziomy mocy:
  cpu   — CPUHtri (12 oscylatorów, ~0.02s) — domyślny
  half  — CPUHtri + GPUHtri 50 kroków (~1s, numpy fallback)
  full  — LocalHTRI CPU+GPU=780 oscylatorów (~5s, numpy fallback / <0.1s z CuPy)

Automatyczna eskalacja: jeśli RAM > 3GB wolnego i brak wysokiego CPU load → half.
Pełna moc tylko na żądanie (power_mode='full') lu
