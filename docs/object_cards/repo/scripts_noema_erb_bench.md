# noema_erb_bench.py — scripts/noema_erb_bench.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_ERB_BENCH-A420`
- **ścieżka:** `scripts/noema_erb_bench.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.997`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_erb_bench.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.997 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `ATTRACTOR`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.476161`
- **R₃:** `0.526498`
- **R₆:** `0.547584`
- **R₉:** `0.472579`
- **potencjal_kappa:** `4.910705`
- **masa_semantyczna:** `13.031004`
- **rodzaj_karty:** `1.5`


## Rola
NOEMA ERB metric comparison: g[24×6] vs g[24×24].

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `noema_24x6`, `noema_24x24`, `init_g_24x6`, `init_g_24x24`, `benchmark_speed`, `sweep_kappa`, `experiment_id`, `save_results`, `_estimate_kappa_c`, `_plot_comparison`, `main`

## Opis
NOEMA ERB metric comparison: g[24×6] vs g[24×24].

Tests two hypotheses for the geometry of the nonlocal surface:

  1. g[24×6]  — direct mixing: 24 mass eigenstates → 6 flavor states (CQCL)
  2. g[24×24] — full metric: all-pairs coupling with flavor as projection

Each is benchmarked for speed, bifurcation structure, and numerical stability.

Usage:
    python3 scripts/noema_erb_bench.py
