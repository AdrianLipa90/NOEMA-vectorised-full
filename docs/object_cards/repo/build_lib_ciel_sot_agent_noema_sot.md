# noema_sot.py — build/lib/ciel_sot_agent/noema_sot.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_SOT-04C4`
- **ścieżka:** `build/lib/ciel_sot_agent/noema_sot.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.622`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_sot_agent/noema_sot.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.622 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `RISK`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.594265`
- **R₃:** `0.468144`
- **R₆:** `0.457554`
- **R₉:** `0.414103`
- **potencjal_kappa:** `0.19508`
- **masa_semantyczna:** `-0.03873`
- **rodzaj_karty:** `0.279007`


## Rola
NOEMA SoT — Global Source of Truth Matrix.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_load_pipeline_state`, `_load_catalog_summary`, `_load_py_catalog_summary`, `_load_jokeheal_summary`, `_project_memory_field`, `collect`, `compute_global`, `export_to_context`, `run`, `_weighted_mean`

## Opis
NOEMA SoT — Global Source of Truth Matrix.

Zbiera metryki ze wszystkich subsystemów Poziomu 1 i ustala:
  - global_coherence  — ważona średnia coherence per subsystem
  - global_health     — min(health) po lv=1
  - tag_matrix        — słownik tagów globalnych z aktualnymi wartościami
  - priority_order    — kolejność subsystemów wg M_sem
  - file_mass_summary — agregat z file_universal_catalog.js
