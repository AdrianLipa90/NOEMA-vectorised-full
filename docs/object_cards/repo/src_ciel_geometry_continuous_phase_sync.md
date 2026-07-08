# continuous_phase_sync.py — src/ciel_geometry/continuous_phase_sync.py

## Tożsamość
- **id_karty:** `REPO-CONTINUOUS_PHASE_SYN-DFB3`
- **ścieżka:** `src/ciel_geometry/continuous_phase_sync.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.200`
- **φ (phi):** `4.264`
- **masa_semantyczna:** `0.82`

## Kotwice
- `src/ciel_geometry/continuous_phase_sync.py`

## Atraktor
- **system:** `orbital_bridge_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via orbital_bridge_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.200 |
| φ | 4.264 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.82 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `orbital_bridge_core`.

## PhaseNav
- **operator:** `ADDITION`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.662589`
- **R₃:** `0.614656`
- **R₆:** `0.542851`
- **R₉:** `0.417608`
- **potencjal_kappa:** `0.07638`
- **masa_semantyczna:** `0.206164`
- **rodzaj_karty:** `0.259027`


## Rola
ContinuousPhaseSync — analytic Ott-Antonsen Z(t) for harmonic Kuramoto.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*
- **wyjście:** *wywnioskowane z folderu — podsystem orbital_bridge_core*

## Zawartość
- **klasy:** ContinuousPhaseSync
- **funkcje:** `compute_Z_harmonic`, `compute_all_Z`, `evolve_analytic`, `reconstruct_phi_from_Z`, `compute_R`, `compute_R_harmonic`, `effective_kappa`, `convergence_time`, `snapshot`

## Opis
ContinuousPhaseSync — analytic Ott-Antonsen Z(t) for harmonic Kuramoto.

Replaces discrete Euler integration with the Ott-Antonsen ansatz for the
3-6-9 harmonic Kuramoto surface. Provides closed-form evolution of the
order parameter Z(t) = R(t)·e^{iψ(t)} for each harmonic channel.

Standard Kuramoto with Lorentzian frequency distribution g(ω) = γ/(π(ω²+γ²))
has analytic solution: ∂Z/∂t = (iω₀ − γ)
