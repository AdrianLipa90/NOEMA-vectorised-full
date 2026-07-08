# resonance_bridge.py — build/lib/ciel_geometry/resonance_bridge.py

## Tożsamość
- **id_karty:** `REPO-RESONANCE_BRIDGE-4494`
- **ścieżka:** `build/lib/ciel_geometry/resonance_bridge.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.027`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_geometry/resonance_bridge.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.027 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
Dual-surface resonance bridge for NOEMA real and imaginal manifolds.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

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
