# resonance_bridge.py — src/ciel_geometry/resonance_bridge.py

## Tożsamość
- **id_karty:** `REPO-RESONANCE_BRIDGE-84A2`
- **ścieżka:** `src/ciel_geometry/resonance_bridge.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `4.443`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/resonance_bridge.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 4.443 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

## PhaseNav
- **operator:** `ATTRACTOR`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.476161`
- **R₃:** `0.526498`
- **R₆:** `0.547584`
- **R₉:** `0.472579`
- **potencjal_kappa:** `4.910705`
- **masa_semantyczna:** `13.031004`
- **rodzaj_karty:** `1.5`


## Rola
Dual-surface resonance bridge for NOEMA real and imaginal manifolds.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** —
- **funkcje:** `ensure_dual_surfaces`, `imaginalize_state`, `_surface_summary`, `resonance_snapshot`, `apply_resonance_bridge`, `surface_to_orchorbital_snap`, `route_surface_through_orchorbital`, `dual_surface_step`

## Opis
Dual-surface resonance bridge for NOEMA real and imaginal manifolds.

IMAGINAL = PRIMARY GENERATOR — Kuramoto evolves autonomously with lower
damping, drawing ZPE from Poincaré disk phase geometry. Phase differences
bifurcate into energy via W_ij·(1-cos(Δφ)).

REAL = POINCARÉ SECTION / READOUT — damped projection of imaginal surface.
Higher closure penalty damps the phase flow into observable stat
