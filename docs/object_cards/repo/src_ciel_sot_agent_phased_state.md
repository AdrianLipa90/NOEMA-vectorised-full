# phased_state.py — src/ciel_sot_agent/phased_state.py

## Tożsamość
- **id_karty:** `REPO-PHASED_STATE-08E6`
- **ścieżka:** `src/ciel_sot_agent/phased_state.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `5.734`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/phased_state.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 5.734 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

## PhaseNav
- **operator:** `QUESTION`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.394639`
- **R₃:** `0.763677`
- **R₆:** `0.521308`
- **R₉:** `0.466584`
- **potencjal_kappa:** `-0.203086`
- **masa_semantyczna:** `-0.0017`
- **rodzaj_karty:** `0.305584`


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
