# kuramoto_harmonic_comparison.py — scripts/kuramoto_harmonic_comparison.py

## Tożsamość
- **id_karty:** `REPO-KURAMOTO_HARMONIC_CO-AD83`
- **ścieżka:** `scripts/kuramoto_harmonic_comparison.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `6.030`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/kuramoto_harmonic_comparison.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 6.030 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `ORDER`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.408132`
- **R₃:** `0.527143`
- **R₆:** `0.447287`
- **R₉:** `0.516074`
- **potencjal_kappa:** `0.213299`
- **masa_semantyczna:** `0.199346`
- **rodzaj_karty:** `0.279908`


## Rola
Kuramoto 3-6-9 Harmonic vs Baseline — Controlled Comparison.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `harmonic_order_params`, `harmonic_composite_phase`, `run_meanfield_kuramoto`, `run_harmonic_kuramoto`, `run_detailed`, `compare_sweep`, `save_comparison`, `plot_comparison`

## Opis
Kuramoto 3-6-9 Harmonic vs Baseline — Controlled Comparison.

Hypotheses:
  H0 (null): 3-6-9 harmonic coupling = standard mean-field Kuramoto
  H1 (false): 3-6-9 gives higher global R at same κ
  H2 (true):  3-6-9 creates structured multi-harmonic synchrony where
              different oscillator groups lock to different harmonics

Protocol:
  - N=24 oscillators, dt=1ms, 10,000 steps
  - Intrinsi
