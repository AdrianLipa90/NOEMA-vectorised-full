# phase_sweep_analysis.py — src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/phase_sweep_analysis.py

## Tożsamość
- **id_karty:** `REPO-PHASE_SWEEP_ANALYSIS-60F4`
- **ścieżka:** `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/phase_sweep_analysis.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.150`
- **φ (phi):** `1.524`
- **masa_semantyczna:** `0.80`

## Kotwice
- `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/phase_sweep_analysis.py`

## Atraktor
- **system:** `ciel_omega_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via ciel_omega_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.150 |
| φ | 1.524 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.80 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `ciel_omega_core`.

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
CIEL/Ω — Phase Dynamics: Sweep, Correlations, Zeta-Weighted WT (v2)

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem ciel_omega_core*
- **wyjście:** *wywnioskowane z folderu — podsystem ciel_omega_core*

## Zawartość
- **klasy:** —
- **funkcje:** `run_scenario`, `sweep`, `pearson`, `correlations`, `show_sweep`, `show_corr`, `main`, `avg`

## Opis
CIEL/Ω — Phase Dynamics: Sweep, Correlations, Zeta-Weighted WT (v2)
=====================================================================
Poprawki vs v1:
  FIX A: zeta-weighted WT wstrzyknięty do dynamiki przez wt_fn callback
  FIX B: sigma_zeta sweep jest dynamiczny (sigma jest parametrem systemu)
  FIX C: werdykt oznaczony jako "candidate", nie "fakt"
