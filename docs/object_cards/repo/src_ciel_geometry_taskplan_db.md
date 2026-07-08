# taskplan_db.py — src/ciel_geometry/taskplan_db.py

## Tożsamość
- **id_karty:** `REPO-TASKPLAN_DB-78E4`
- **ścieżka:** `src/ciel_geometry/taskplan_db.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `0.126`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/taskplan_db.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 0.126 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

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
taskplan_db.py — Baza tasków, planów i lekcji z LP (liczbą porządkową).

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** TaskPlanDB
- **funkcje:** `_conn`, `_init_schema`, `_ts`, `next_lp`, `add_task`, `update_task`, `get_task`, `list_tasks`, `get_high_priority_tasks`, `delete_task`, `add_plan`, `update_plan`, `get_plan`, `list_plans`, `delete_plan`, `add_lesson`, `get_lesson`, `list_lessons`, `delete_lesson`, `add_decision`, `_next_decision_lp`, `update_decision`, `get_decision`, `list_decisions`, `get_decision_tree`, `_build_subtree`, `delete_decision`, `add_skill`, `update_skill`, `list_skills`

## Opis
taskplan_db.py — Baza tasków, planów i lekcji z LP (liczbą porządkową).

Tabele:
  tasks    — zadania/zadania z LP, status, priorytet, orbital_ref
  plans    — plany z LP, kroki (JSON), status
  lessons  — lekcje z LP (odpowiednik LEARNED_LESSONS.md)
  registry — klucze meta (wersja schematu, ostatni update)
