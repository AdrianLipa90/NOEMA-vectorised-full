# generate_site.py — scripts/generate_site.py

## Tożsamość
- **id_karty:** `REPO-GENERATE_SITE-70E9`
- **ścieżka:** `scripts/generate_site.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `4.509`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/generate_site.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 4.509 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `UNRUH_DRIVE`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.695214`
- **R₃:** `0.356299`
- **R₆:** `0.471302`
- **R₉:** `0.535169`
- **potencjal_kappa:** `0.138014`
- **masa_semantyczna:** `0.204514`
- **rodzaj_karty:** `0.244249`


## Rola
CIEL Site Generator — generuje statyczną stronę HTML z danych CIEL.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `load_pipeline_report`, `section_ciel_omega`, `load_mindflow`, `load_intentions`, `load_entity_cards`, `load_orbital_final`, `load_entity_orbital`, `load_phase_history`, `_svg_sparkline`, `load_cache_entries`, `load_snapshots`, `load_wpm_memories`, `load_diary_entries`, `_parse_frontmatter`, `load_project_memory`, `load_object_cards`, `_inline`, `md_to_html`, `esc`, `_nav_html`, `_page`, `spin_color`, `defect_color`, `section_identity`, `section_mindflow`, `section_entities`, `_entity_sector_name`, `section_intentions`, `section_diary`, `section_wpm`

## Opis
CIEL Site Generator — generuje statyczną stronę HTML z danych CIEL.

Źródła:
  ~/.claude/ciel_mindflow.yaml     → Przemyślenia, pytania, napięcia
  ~/.claude/ciel_intentions.md     → Agenda / intencje
  ~/.claude/ciel_snapshots/        → Historia sesji
  ~/.claude/projects/.../memory/prompt_cache.md → Log sesji
  integration/registries/ciel_entity_cards.yaml → Mapa relacyjna
  integration/Orbital/
