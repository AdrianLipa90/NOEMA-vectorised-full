# scar_feedback.py — src/ciel_geometry/scar_feedback.py

## Tożsamość
- **id_karty:** `REPO-SCAR_FEEDBACK-307B`
- **ścieżka:** `src/ciel_geometry/scar_feedback.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `3.176`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/scar_feedback.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 3.176 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

## PhaseNav
- **operator:** `RISK`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.594265`
- **R₃:** `0.468144`
- **R₆:** `0.457554`
- **R₉:** `0.414103`
- **potencjal_kappa:** `0.19508`
- **masa_semantyczna:** `-0.03873`
- **rodzaj_karty:** `0.279007`


## Rola
SemanticScar → surface feedback loop — autonomiczny układ nerwowy NOEMY.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** —
- **funkcje:** `compute_scar_feedback`, `apply_scar_feedback`

## Opis
SemanticScar → surface feedback loop — autonomiczny układ nerwowy NOEMY.

Czyta rzeczywiste wskaźniki blizn semantycznych z CIELingo (gravity[4-7])
i moduluje stan powierzchni NOEMA (phi, omega, flavor, g) w trzech warstwach:

  1. ω per-channel — semantic (M3) zwalnia bardziej niż percept (M0)
  2. φ divergence   — M3 rozjeżdża się przy niepewności, zbiega przy konsensusie
  3. g tightening   — M
