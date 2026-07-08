# taskplan_db.py — build/bdist.linux-x86_64/wheel/ciel_geometry/taskplan_db.py

## Tożsamość
- **id_karty:** `REPO-TASKPLAN_DB-6647`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_geometry/taskplan_db.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `0.880`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_geometry/taskplan_db.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 0.880 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `SCOPE`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.516458`
- **R₃:** `0.452404`
- **R₆:** `0.493743`
- **R₉:** `0.465851`
- **potencjal_kappa:** `0.026123`
- **masa_semantyczna:** `0.147985`
- **rodzaj_karty:** `0.241584`


## Rola
taskplan_db.py — Baza tasków, planów i lekcji z LP (liczbą porządkową).

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

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
