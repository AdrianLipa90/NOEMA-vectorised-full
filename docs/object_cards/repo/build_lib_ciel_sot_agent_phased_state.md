# phased_state.py — build/lib/ciel_sot_agent/phased_state.py

## Tożsamość
- **id_karty:** `REPO-PHASED_STATE-935E`
- **ścieżka:** `build/lib/ciel_sot_agent/phased_state.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.924`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_sot_agent/phased_state.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.924 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
Phased-state model for repository and file-level identity scoring.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** FileState
- **funkcje:** `sha256_seed`, `frac64`, `f_size`, `_require_finite_real`, `_require_hash_fraction`, `_require_connection_count`, `_require_non_negative_count`, `_require_positive_weight`, `f_conn`, `f_anchor`, `f_flow`, `weight_type`, `weight_layer`, `relational_relevance`, `compute_raw_energy`, `normalize`, `compute_phase`, `build_states`

## Opis
Phased-state model for repository and file-level identity scoring.

Computes a deterministic identity phase for each file/node from its
hash-derived fraction and computes selection energy from explicit
relational metadata such as size, type, layer, connectivity, anchors,
and upstream/downstream structure. Used by the holonomic normalizer and
index-validation pipeline.

Domain contracts:
- ``comput
