# energy_benchmark.py — scripts/sims/energy_benchmark.py

## Tożsamość
- **id_karty:** `REPO-ENERGY_BENCHMARK-D77F`
- **ścieżka:** `scripts/sims/energy_benchmark.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `3.560`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/sims/energy_benchmark.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 3.560 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `PAUSE`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.508756`
- **R₃:** `0.557009`
- **R₆:** `0.421727`
- **R₉:** `0.55292`
- **potencjal_kappa:** `-0.020552`
- **masa_semantyczna:** `0.206252`
- **rodzaj_karty:** `0.260435`


## Rola
CIEL Energy Benchmark — zużycie energii lokalnego pipeline vs Claude API (szacunek).

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `power_W`, `energy_mJ`, `read_proc_stat`, `measure`, `baseline`, `bench_m08`, `bench_pipeline`, `claude_api_estimate`, `main`, `run`, `run`

## Opis
CIEL Energy Benchmark — zużycie energii lokalnego pipeline vs Claude API (szacunek).

Mierzy:
  - M0-M8 per krok (hot, in-process)
  - Full pipeline (cold, subprocess)
  - Szacunek energii sesji 30 wiad.
  - Porównanie z kosztem energetycznym Claude API (server-side)

RAPL wymaga root (intel-rapl:0/energy_uj).
Skrypt używa /proc/stat CPU utilization + model TDP jako proxy.

i7-8750H: TDP=45W, idle
