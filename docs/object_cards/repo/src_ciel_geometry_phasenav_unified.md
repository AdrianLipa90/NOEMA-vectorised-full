# phasenav_unified.py — src/ciel_geometry/phasenav_unified.py

## Tożsamość
- **id_karty:** `REPO-PHASENAV_UNIFIED-65DB`
- **ścieżka:** `src/ciel_geometry/phasenav_unified.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `1.574`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/phasenav_unified.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 1.574 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

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
UnifiedPhaseNavIndex — jeden indeks, wszystkie źródła NOEMA + Linux.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** UnifiedPhaseNavIndex
- **funkcje:** `_build`, `_add`, `_load_skills`, `_load_knowledge_db`, `_load_palace_rooms`, `_load_linux_cards`, `_load_taskplan_db`, `_load_task_queue`, `_load_system_map`, `_text_to_phi`, `_angular_sim`, `count`, `search`, `_search_linux_cards_structured`, `search_by_phi`, `filter_by_source`, `_log_stats`, `stats`, `rebuild`

## Opis
UnifiedPhaseNavIndex — jeden indeks, wszystkie źródła NOEMA + Linux.

Łączy w jednej 36D przestrzeni fazowej:
  - skill_index         (291 skilli PhaseNav 36D)
  - knowledge_db        (15 tabel z noema_knowledge.db)
  - palace_rooms        (snapshoty MemoryPalace)
  - linux_cards         (560+ kart live: CPU, PROC, NET, DISK, SENSOR…)

Każdy wpis ma source_type + source_table.
Szukaj przez 36D ang
