# phase_control.py — src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/orbital/phase_control.py

## Tożsamość
- **id_karty:** `REPO-PHASE_CONTROL-1DE9`
- **ścieżka:** `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/orbital/phase_control.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.150`
- **φ (phi):** `4.274`
- **masa_semantyczna:** `0.80`

## Kotwice
- `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/orbital/phase_control.py`

## Atraktor
- **system:** `ciel_omega_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via ciel_omega_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.150 |
| φ | 4.274 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.80 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `ciel_omega_core`.

## PhaseNav
- **operator:** `FOLD`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.351212`
- **R₃:** `0.661831`
- **R₆:** `0.649218`
- **R₉:** `0.522246`
- **potencjal_kappa:** `-0.135067`
- **masa_semantyczna:** `-0.137397`
- **rodzaj_karty:** `0.29302`


## Rola
Phase control — canonical mode selection for the CIEL orbital layer.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem ciel_omega_core*
- **wyjście:** *wywnioskowane z folderu — podsystem ciel_omega_core*

## Zawartość
- **klasy:** —
- **funkcje:** `_obs`, `coherence_index_from_snapshot`, `topological_charge_global`, `phase_lock_error`, `mode_norm`, `_mode_from_psi`, `_continuous_params`, `recommend_control`, `build_state_manifest`, `build_health_manifest`, `effective_rh`

## Opis
Phase control — canonical mode selection for the CIEL orbital layer.

Mode norm  ψ = (1 − ci) + γ · penalty / penalty_max
maps the full system state onto a single scalar in [0, 1]:

  ψ < _PSI_DEEP      → "deep"     full autonomy, write-back open
  ψ < _PSI_STANDARD  → "standard" cautious, write-back gated
  ψ ≥ _PSI_STANDARD  → "safe"     read-only, ask before any change

Continuous parameters (d
