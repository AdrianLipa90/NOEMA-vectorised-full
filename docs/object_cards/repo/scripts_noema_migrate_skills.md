# noema_migrate_skills.py — scripts/noema_migrate_skills.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_MIGRATE_SKILLS-3E73`
- **ścieżka:** `scripts/noema_migrate_skills.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `0.445`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_migrate_skills.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 0.445 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

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
NOEMA Skill Directory Migration

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `load_catalog`, `migrate`

## Opis
NOEMA Skill Directory Migration
================================
Migrates skill directories from flat structure to grouped structure:
  .opencode/skills/{name}/  →  .opencode/skills/{GROUP}/{name}/
  
Z zachowaniem kompatybilności wstecznej przez symlinki.

Użycie:
  python3 scripts/noema_migrate_skills.py --dry-run    # podgląd
  python3 scripts/noema_migrate_skills.py              # wykonaj migr
