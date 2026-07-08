# continuous_phase_sync.py — build/lib/ciel_geometry/continuous_phase_sync.py

## Tożsamość
- **id_karty:** `REPO-CONTINUOUS_PHASE_SYN-8984`
- **ścieżka:** `build/lib/ciel_geometry/continuous_phase_sync.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.419`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_geometry/continuous_phase_sync.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.419 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_POSSIBILITY`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.565748`
- **R₃:** `0.628966`
- **R₆:** `0.492583`
- **R₉:** `0.589778`
- **potencjal_kappa:** `0.024081`
- **masa_semantyczna:** `-0.294904`
- **rodzaj_karty:** `0.302592`


## Rola
ContinuousPhaseSync — analytic Ott-Antonsen Z(t) for harmonic Kuramoto.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

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
