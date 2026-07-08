# repo_phase.py — build/lib/ciel_sot_agent/repo_phase.py

## Tożsamość
- **id_karty:** `REPO-REPO_PHASE-13EE`
- **ścieżka:** `build/lib/ciel_sot_agent/repo_phase.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.654`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_sot_agent/repo_phase.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.654 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
Repository phase state and synchronisation report builder.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** RepositoryState
- **funkcje:** `load_registry`, `load_couplings`, `weighted_euler_vector`, `weighted_euler_vector_numpy`, `closure_defect`, `euler_residual`, `pairwise_tension_matrix`, `j_repo`, `pairwise_tension`, `all_pairwise_tensions`, `build_sync_report`

## Opis
Repository phase state and synchronisation report builder.

Models each repository as a phase-carrying identity with a complex spin,
mass, and role.  Exposes ``build_sync_report`` which loads the repository
registry and coupling map, computes the weighted Euler vector and closure
defect, and returns a machine-readable synchronisation report.
