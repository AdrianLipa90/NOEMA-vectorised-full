# optimize_wij.py — scripts/optimize_wij.py

## Tożsamość
- **id_karty:** `REPO-OPTIMIZE_WIJ-CFCA`
- **ścieżka:** `scripts/optimize_wij.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `4.271`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/optimize_wij.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 4.271 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `MEMORY`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.481637`
- **R₃:** `0.436994`
- **R₆:** `0.50573`
- **R₉:** `0.517955`
- **potencjal_kappa:** `0.179117`
- **masa_semantyczna:** `0.012321`
- **rodzaj_karty:** `0.236997`


## Rola
W_ij coupling optimizer for the CIEL orbital system.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_rh_coherence_score`, `_build_system`, `_coupling_pairs`, `_vec_to_couplings`, `_run_steps`, `make_objective`, `main`, `_ci_full`, `objective`

## Opis
W_ij coupling optimizer for the CIEL orbital system.

Minimizes closure_penalty over the scalar coupling matrix W_ij in
integration/Orbital/main/manifests/couplings_global.json using
scipy L-BFGS-B with bounds W_ij ∈ [0.01, 1.0].

Objective:
    closure_penalty = Σ_i |Σ_j A_ij(W) * τ_j - e^{iφ_i}|²  +  ζ_tetra_weight * ζ_tetra

Usage:
    python scripts/optimize_wij.py [--write] [--steps N] [--max
