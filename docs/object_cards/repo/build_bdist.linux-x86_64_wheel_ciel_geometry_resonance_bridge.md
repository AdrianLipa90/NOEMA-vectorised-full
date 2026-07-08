# resonance_bridge.py — build/bdist.linux-x86_64/wheel/ciel_geometry/resonance_bridge.py

## Tożsamość
- **id_karty:** `REPO-RESONANCE_BRIDGE-266C`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_geometry/resonance_bridge.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.267`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_geometry/resonance_bridge.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.267 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ORDER`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.408132`
- **R₃:** `0.527143`
- **R₆:** `0.447287`
- **R₉:** `0.516074`
- **potencjal_kappa:** `0.213299`
- **masa_semantyczna:** `0.199346`
- **rodzaj_karty:** `0.279908`


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
