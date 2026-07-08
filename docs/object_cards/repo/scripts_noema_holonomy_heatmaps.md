# noema_holonomy_heatmaps.py — scripts/noema_holonomy_heatmaps.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_HOLONOMY_HEATM-353E`
- **ścieżka:** `scripts/noema_holonomy_heatmaps.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `5.696`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_holonomy_heatmaps.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 5.696 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `CONDITION`
- **odcisk_harmoniczny:** `HLHL`
- **R₁:** `0.577442`
- **R₃:** `0.440978`
- **R₆:** `0.50908`
- **R₉:** `0.325439`
- **potencjal_kappa:** `-0.091854`
- **masa_semantyczna:** `-0.064427`
- **rodzaj_karty:** `0.305875`


## Rola
NOEMA Catalog Holonomy Heatmap Generator

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `load_skills`, `build_skills_heatmaps`, `parse_plans`, `build_plans_heatmaps`, `parse_functions`, `build_functions_heatmaps`, `main`

## Opis
NOEMA Catalog Holonomy Heatmap Generator
=========================================
Generuje macierze holonomii (co-occurrence) między tagami w 3 katalogach:
  - SKILLS.md (umiejętności)
  - FUNCTIONS.md (funkcje/moduly)
  - PLANS.md (plany)

Wynik: JSON w site/assets/data/heatmaps/ — do wizualizacji w Portalu NOEMA.
