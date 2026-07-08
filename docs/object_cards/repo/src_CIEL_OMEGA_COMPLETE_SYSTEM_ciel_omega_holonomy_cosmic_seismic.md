# holonomy_cosmic_seismic.py — src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/holonomy_cosmic_seismic.py

## Tożsamość
- **id_karty:** `REPO-HOLONOMY_COSMIC_SEIS-7461`
- **ścieżka:** `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/holonomy_cosmic_seismic.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.150`
- **φ (phi):** `1.034`
- **masa_semantyczna:** `0.80`

## Kotwice
- `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/holonomy_cosmic_seismic.py`

## Atraktor
- **system:** `ciel_omega_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via ciel_omega_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.150 |
| φ | 1.034 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.80 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `ciel_omega_core`.

## PhaseNav
- **operator:** `AFFECT`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.542195`
- **R₃:** `0.629813`
- **R₆:** `0.534142`
- **R₉:** `0.565106`
- **potencjal_kappa:** `0.141102`
- **masa_semantyczna:** `0.203631`
- **rodzaj_karty:** `0.326785`


## Rola
Holonomic testbed for cosmic-ray / seismic / solar coupling.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem ciel_omega_core*
- **wyjście:** *wywnioskowane z folderu — podsystem ciel_omega_core*

## Zawartość
- **klasy:** SeriesSpec, EarthquakeSpec, HolonomyConfig
- **funkcje:** `_ensure_datetime_index`, `load_scalar_series`, `load_earthquake_activity`, `bin_series`, `align_series`, `robust_standardize`, `preprocess_signal`, `analytic_phase`, `wrap_angle`, `phase_distance`, `white_thread_amplitude`, `shift_by_days`, `holonomic_defect`, `holonomy_measure`, `euler_closure_error`, `score_tau_scan`, `score_tau_delta_scan`, `save_main_plots`, `run_pipeline`, `parse_args`, `main`

## Opis
Holonomic testbed for cosmic-ray / seismic / solar coupling.

Purpose
-------
Given three time series
    1) cosmic-ray intensity (or its filtered / normalized proxy),
    2) earthquake activity,
    3) solar activity,
compute a phase-holonomy diagnostic inspired by the user's Metatime/CIEL
framework:

    Δ_H(t; τ, δ) = exp(i φ_CR(t))
                 + w_EQ exp(i φ_EQ(t + τ))
                 +
