# phasenav_unified.py — build/bdist.linux-x86_64/wheel/ciel_geometry/phasenav_unified.py

## Tożsamość
- **id_karty:** `REPO-PHASENAV_UNIFIED-51B9`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_geometry/phasenav_unified.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.664`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_geometry/phasenav_unified.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.664 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `IDENTITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.405566`
- **R₃:** `0.499333`
- **R₆:** `0.494094`
- **R₉:** `0.455981`
- **potencjal_kappa:** `0.08965`
- **masa_semantyczna:** `-0.024381`
- **rodzaj_karty:** `0.279273`


## Rola
UnifiedPhaseNavIndex — jeden indeks, wszystkie źródła NOEMA + Linux.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

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
