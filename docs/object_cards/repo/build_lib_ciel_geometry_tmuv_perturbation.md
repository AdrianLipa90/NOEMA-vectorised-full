# tmuv_perturbation.py — build/lib/ciel_geometry/tmuv_perturbation.py

## Tożsamość
- **id_karty:** `REPO-TMUV_PERTURBATION-0915`
- **ścieżka:** `build/lib/ciel_geometry/tmuv_perturbation.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.333`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_geometry/tmuv_perturbation.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.333 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `FORCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.552175`
- **R₃:** `0.435218`
- **R₆:** `0.571397`
- **R₉:** `0.579087`
- **potencjal_kappa:** `0.300939`
- **masa_semantyczna:** `0.016845`
- **rodzaj_karty:** `0.260112`


## Rola
T_μν stress-energy perturbation bridge for CIEL orbital dynamics.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

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
