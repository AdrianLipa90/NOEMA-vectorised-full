# continuous_propagator.py — build/bdist.linux-x86_64/wheel/ciel_geometry/phasenav/continuous_propagator.py

## Tożsamość
- **id_karty:** `REPO-CONTINUOUS_PROPAGATO-3214`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_geometry/phasenav/continuous_propagator.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `5.572`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_geometry/phasenav/continuous_propagator.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 5.572 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONSENT_REQUIRED`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.458017`
- **R₃:** `0.48995`
- **R₆:** `0.569953`
- **R₉:** `0.575041`
- **potencjal_kappa:** `-0.194917`
- **masa_semantyczna:** `0.103166`
- **rodzaj_karty:** `0.278924`


## Rola
Continuous phase propagator on S¹ — Zeta-Schrödinger evolution.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `spline_phi`, `zeta_potential`, `evolve_continuous`, `self_test`

## Opis
Continuous phase propagator on S¹ — Zeta-Schrödinger evolution.

Replaces discrete Kuramoto (24 osc, dt stepping) with a continuous spline
representation. The phase field φ(θ, t) lives on a circle, evolved by:
    i·∂φ/∂t = H·φ + V_zeta(φ)
where V_zeta is Zeta-regularized potential (no collaps, continuous).

Discrete 24 points are kept as B-spline control knots, not oscillators.
