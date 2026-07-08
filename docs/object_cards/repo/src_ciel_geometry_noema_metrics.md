# noema_metrics.py — src/ciel_geometry/noema_metrics.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_METRICS-07CC`
- **ścieżka:** `src/ciel_geometry/noema_metrics.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `6.271`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/noema_metrics.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 6.271 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

## PhaseNav
- **operator:** `DIFFERENCE`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.563622`
- **R₃:** `0.51399`
- **R₆:** `0.516024`
- **R₉:** `0.447233`
- **potencjal_kappa:** `-0.196591`
- **masa_semantyczna:** `-0.06476`
- **rodzaj_karty:** `0.313562`


## Rola
NOEMA Metrics — system metryk z progami, ścieżkami i monitoringiem.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

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
