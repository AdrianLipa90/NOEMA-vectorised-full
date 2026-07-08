# mc_holonomic_convergence.py — scripts/mc_holonomic_convergence.py

## Tożsamość
- **id_karty:** `REPO-MC_HOLONOMIC_CONVERG-F4E6`
- **ścieżka:** `scripts/mc_holonomic_convergence.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `3.418`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/mc_holonomic_convergence.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 3.418 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `SOURCE_REQUIRED`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.509375`
- **R₃:** `0.557002`
- **R₆:** `0.453972`
- **R₉:** `0.573802`
- **potencjal_kappa:** `-0.191054`
- **masa_semantyczna:** `-0.307021`
- **rodzaj_karty:** `0.246226`


## Rola
Monte Carlo convergence test for holonomic_system_normalizer_v2.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_sample_state`, `_callbacks`, `_run_with_step_count`, `run_mc`, `_print_summary`, `main`, `counting_rmc`

## Opis
Monte Carlo convergence test for holonomic_system_normalizer_v2.

Samples synthetic states from realistic parameter distributions and measures:
  - steps_to_convergence (out of max_iter=24)
  - fraction_converged
  - fraction_mode_safe
  - median J_final

Usage:
  python scripts/mc_holonomic_convergence.py --baseline    # save baseline
  python scripts/mc_holonomic_convergence.py --compare     # c
