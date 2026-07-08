# noema_metrics.py — build/lib/ciel_geometry/noema_metrics.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_METRICS-BE43`
- **ścieżka:** `build/lib/ciel_geometry/noema_metrics.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.049`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_geometry/noema_metrics.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.049 |
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
NOEMA Metrics — system metryk z progami, ścieżkami i monitoringiem.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** MetricDef, MetricSample, MetricsRegistry
- **funkcje:** `get_registry`, `collect_all`, `get_metric`, `evaluate_warnings`, `summary`, `_register_defaults`, `register`, `get_def`, `definitions`, `_read_surface`, `_collect_daemons_alive`, `_collect_memory_entries`, `_collect_memory_exchanges`, `_evaluate`, `collect`, `collect_all`, `get_warnings`, `summary`, `history`

## Opis
NOEMA Metrics — system metryk z progami, ścieżkami i monitoringiem.

Każda metryka ma:
  - nazwę i opis
  - źródło danych (ścieżka dostępu)
  - próg ostrzegawczy i krytyczny
  - jednostkę
  - aktualną wartość
  - status (ok/warning/critical/unknown)

Pathways:
  1. Surface mmap — odczyt live z /dev/shm/ciel_noema
  2. CIEL state — z state_db (CIELingo)
  3. Omega Memory — stats z omega_memory_brid
