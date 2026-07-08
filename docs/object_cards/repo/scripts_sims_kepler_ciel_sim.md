# kepler_ciel_sim.py — scripts/sims/kepler_ciel_sim.py

## Tożsamość
- **id_karty:** `REPO-KEPLER_CIEL_SIM-4724`
- **ścieżka:** `scripts/sims/kepler_ciel_sim.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `3.388`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/sims/kepler_ciel_sim.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 3.388 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `NEGATION`
- **odcisk_harmoniczny:** `LHLL`
- **R₁:** `0.425094`
- **R₃:** `0.614676`
- **R₆:** `0.450577`
- **R₉:** `0.387679`
- **potencjal_kappa:** `0.085998`
- **masa_semantyczna:** `-0.143065`
- **rodzaj_karty:** `0.271614`


## Rola
Kepler emergence simulation under CIEL dynamics.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** OrbitState
- **funkcje:** `poincare_from_bloch`, `bloch_from_poincare`, `V`, `dV_drho`, `_integrate_orbit`, `kepler_period`, `areal_velocity`, `orbit_closure`, `run_simulation`, `print_report`

## Opis
Kepler emergence simulation under CIEL dynamics.

Tests whether Bloch-sphere phase orbits with M_sem inertia reproduce
Kepler's laws when closure_penalty acts as gravitational potential V(r) ~ -k/r.

Physics model:
  - Position: phase angle φ on Bloch sphere → projected to Poincaré disk radius ρ
  - Potential: V(ρ) = -k / ρ  (closure_penalty as effective gravity)
  - Inertia: m_eff = M_sem (semant
