# tmuv_perturbation.py — src/ciel_geometry/tmuv_perturbation.py

## Tożsamość
- **id_karty:** `REPO-TMUV_PERTURBATION-0326`
- **ścieżka:** `src/ciel_geometry/tmuv_perturbation.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `4.359`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/tmuv_perturbation.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 4.359 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

## PhaseNav
- **operator:** `MODAL_NECESSITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.449701`
- **R₃:** `0.392905`
- **R₆:** `0.402231`
- **R₉:** `0.439135`
- **potencjal_kappa:** `-0.089486`
- **masa_semantyczna:** `-0.210953`
- **rodzaj_karty:** `0.286192`


## Rola
T_μν stress-energy perturbation bridge for CIEL orbital dynamics.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** —
- **funkcje:** `tmuv_total_energy_density`, `mass_perturbation_from_tmuv`, `compute_effective_masses`, `total_stress_energy_scalar`

## Opis
T_μν stress-energy perturbation bridge for CIEL orbital dynamics.

Connects the stress-energy tensor from ciel0_framework.py to the N-body
orbital engine (nbody_gravity.py) via an effective mass perturbation.

The T_μν tensor (matter + intention) from the unified CIEL/0 field theory
modifies each orbital body's effective gravitational mass:

    M_eff = M_sem + α · ΔM_Tμν

where ΔM_Tμν is the inte
