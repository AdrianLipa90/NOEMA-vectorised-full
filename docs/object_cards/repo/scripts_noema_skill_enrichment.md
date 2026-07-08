# noema_skill_enrichment.py — scripts/noema_skill_enrichment.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_SKILL_ENRICHME-AD6C`
- **ścieżka:** `scripts/noema_skill_enrichment.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `0.937`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_skill_enrichment.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 0.937 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

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
NOEMA Skill Enrichment & Catalog Generator

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `extract_primary_orbital`, `compute_semantic_mass`, `classify_skill`, `generate_description`, `get_script_ref`, `get_type_group_name`, `get_app_group_name`, `build_catalog`, `generate_skills_md`, `main`

## Opis
NOEMA Skill Enrichment & Catalog Generator
===========================================
Przetwarza wszystkie 293 skille w .opencode/skills/:
  1. Nadaje numery katalogowe (SK-XXX)
  2. Klasyfikuje do grup typów i zastosowań
  3. Przypisuje tagi holonomii semantycznej
  4. Generuje opis zastosowania + odnośniki
  5. Aktualizuje SKILLS.md z pełnym katalogiem

Użycie:
  python3 scripts/noema_skill_enr
