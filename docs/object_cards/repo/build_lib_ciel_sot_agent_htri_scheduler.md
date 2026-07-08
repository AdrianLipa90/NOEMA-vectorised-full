# htri_scheduler.py — build/lib/ciel_sot_agent/htri_scheduler.py

## Tożsamość
- **id_karty:** `REPO-HTRI_SCHEDULER-1879`
- **ścieżka:** `build/lib/ciel_sot_agent/htri_scheduler.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.100`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_sot_agent/htri_scheduler.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.100 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_NECESSITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.449701`
- **R₃:** `0.392905`
- **R₆:** `0.402231`
- **R₉:** `0.439135`
- **potencjal_kappa:** `-0.089486`
- **masa_semantyczna:** `-0.210953`
- **rodzaj_karty:** `0.286192`


## Rola
HTRI Scheduler — adaptacyjny dense matrix scheduler.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_htri_path`, `_ram_free_gb`, `_cpu_load`, `_cuda_available`, `_auto_power_mode`, `run`, `get_state`, `get_optimal_threads`

## Opis
HTRI Scheduler — adaptacyjny dense matrix scheduler.

Trzy poziomy mocy:
  cpu   — CPUHtri (12 oscylatorów, ~0.02s) — domyślny
  half  — CPUHtri + GPUHtri 50 kroków (~1s, numpy fallback)
  full  — LocalHTRI CPU+GPU=780 oscylatorów (~5s, numpy fallback / <0.1s z CuPy)

Automatyczna eskalacja: jeśli RAM > 3GB wolnego i brak wysokiego CPU load → half.
Pełna moc tylko na żądanie (power_mode='full') lu
