# continuous_propagator.py — src/ciel_geometry/phasenav/continuous_propagator.py

## Tożsamość
- **id_karty:** `REPO-CONTINUOUS_PROPAGATO-2712`
- **ścieżka:** `src/ciel_geometry/phasenav/continuous_propagator.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `4.556`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/phasenav/continuous_propagator.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 4.556 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

## PhaseNav
- **operator:** `SOURCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.591319`
- **R₃:** `0.39689`
- **R₆:** `0.568492`
- **R₉:** `0.527911`
- **potencjal_kappa:** `0.015345`
- **masa_semantyczna:** `-0.142691`
- **rodzaj_karty:** `0.266598`


## Rola
Continuous phase propagator on S¹ — Zeta-Schrödinger evolution.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** —
- **funkcje:** `spline_phi`, `zeta_potential`, `evolve_continuous`, `self_test`

## Opis
Continuous phase propagator on S¹ — Zeta-Schrödinger evolution.

Replaces discrete Kuramoto (36 osc, dt stepping) with a continuous spline
representation. The phase field φ(θ, t) lives on a circle, evolved by:
    i·∂φ/∂t = H·φ + V_zeta(φ)
where V_zeta is Zeta-regularized potential (no collaps, continuous).

Discrete 36 points are kept as B-spline control knots, not oscillators.
