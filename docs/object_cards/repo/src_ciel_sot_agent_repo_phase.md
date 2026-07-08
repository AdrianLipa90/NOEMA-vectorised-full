# repo_phase.py — src/ciel_sot_agent/repo_phase.py

## Tożsamość
- **id_karty:** `REPO-REPO_PHASE-50CF`
- **ścieżka:** `src/ciel_sot_agent/repo_phase.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `3.700`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/repo_phase.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 3.700 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

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
