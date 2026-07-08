# noema_metrics.py — build/bdist.linux-x86_64/wheel/ciel_geometry/noema_metrics.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_METRICS-AF16`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_geometry/noema_metrics.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.456`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_geometry/noema_metrics.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.456 |
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
