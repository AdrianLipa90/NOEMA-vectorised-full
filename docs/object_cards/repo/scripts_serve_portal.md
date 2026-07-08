# serve_portal.py — scripts/serve_portal.py

## Tożsamość
- **id_karty:** `REPO-SERVE_PORTAL-9BA7`
- **ścieżka:** `scripts/serve_portal.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `0.419`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/serve_portal.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 0.419 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

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
CIEL Portal Server — serwuje ~/.claude/ciel_site/ przez HTTP.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** CIELHandler
- **funkcje:** `read_live_state`, `read_orbital_data`, `read_geometry_data`, `read_sessions`, `read_memories`, `run_pipeline_step`, `_mime`, `_watch_and_rebuild`, `main`, `log_message`, `do_GET`, `do_POST`

## Opis
CIEL Portal Server — serwuje ~/.claude/ciel_site/ przez HTTP.

Funkcje:
  - Serwuje portal jako http://localhost:7481/
  - /api/live  — live metryki z pickle (cycle, health, ethical, closure, emotion)
  - /api/state — pełny stan orbitalny z ostatniego raportu
  - Wstrzykuje do każdej strony HTML auto-refresh JS (polling /api/live co 8s)
  - Automatycznie przebudowuje portal gdy źródła się zmieniaj
