# noema_sot.py — src/ciel_sot_agent/noema_sot.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_SOT-00A0`
- **ścieżka:** `src/ciel_sot_agent/noema_sot.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `3.617`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/noema_sot.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 3.617 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

## PhaseNav
- **operator:** `REFUSAL`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.441725`
- **R₃:** `0.537197`
- **R₆:** `0.362678`
- **R₉:** `0.509166`
- **potencjal_kappa:** `0.077364`
- **masa_semantyczna:** `-0.245874`
- **rodzaj_karty:** `0.27107`


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
