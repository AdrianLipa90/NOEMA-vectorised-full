# roadmap.py — src/ciel_lingophysics_lns_repo_v2_3/src/lingophysics/roadmap.py

## Tożsamość
- **id_karty:** `REPO-ROADMAP-772A`
- **ścieżka:** `src/ciel_lingophysics_lns_repo_v2_3/src/lingophysics/roadmap.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.109`
- **masa_semantyczna:** `0.40`

## Kotwice
- `src/ciel_lingophysics_lns_repo_v2_3/src/lingophysics/roadmap.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.109 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `PAUSE`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.508756`
- **R₃:** `0.557009`
- **R₆:** `0.421727`
- **R₉:** `0.55292`
- **potencjal_kappa:** `-0.020552`
- **masa_semantyczna:** `0.206252`
- **rodzaj_karty:** `0.260435`


## Rola
Roadmap helpers for CIELingo.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `load_roadmap`, `validate_roadmap`, `planned_phases`, `next_phase`, `gguf_is_advisory`

## Opis
Roadmap helpers for CIELingo.

The roadmap is intentionally data-driven so future patches can inspect the
stage plan without parsing Markdown. This module performs lightweight checks;
full JSON Schema validation is optional and kept out of the dependency chain.
