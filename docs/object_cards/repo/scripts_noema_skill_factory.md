# noema_skill_factory.py — scripts/noema_skill_factory.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_SKILL_FACTORY-FF60`
- **ścieżka:** `scripts/noema_skill_factory.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.740`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_skill_factory.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.740 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `RETURN`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.642878`
- **R₃:** `0.503912`
- **R₆:** `0.555289`
- **R₉:** `0.707983`
- **potencjal_kappa:** `-0.270999`
- **masa_semantyczna:** `-0.074142`
- **rodzaj_karty:** `0.291714`


## Rola
NOEMA Skill Factory — batch conversion of .md docs + source enrichment.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `log`, `extract_title`, `extract_formulas`, `extract_bullets`, `extract_code_blocks`, `extract_definitions`, `extract_tables`, `extract_sections`, `make_skill_name`, `catname_from_source`, `generate_skill_md`, `process_md_file`, `write_skill`, `scan_directory`, `rebuild_index`, `main`, `cat_for_skill`

## Opis
NOEMA Skill Factory — batch conversion of .md docs + source enrichment.
Usage:
    python3 scripts/noema_skill_factory.py [--dry-run] [--verbose] [--reindex]
    
Modes:
  --dry-run    Preview only
  --verbose    Full logging
  --reindex    Only rebuild 00-INDEX (skip doc processing)

Processes:
  - ciel_lingophysics_lns_repo_v2_3/docs/  (46 docs)
  - ciel_lingophysics_lns_repo_v2_3/reports/ (16 r
