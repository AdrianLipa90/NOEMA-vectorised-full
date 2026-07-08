# phased_state.py — build/bdist.linux-x86_64/wheel/ciel_sot_agent/phased_state.py

## Tożsamość
- **id_karty:** `REPO-PHASED_STATE-674C`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_sot_agent/phased_state.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.117`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_sot_agent/phased_state.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.117 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_NECESSITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.449701`
- **R₃:** `0.392905`
- **R₆:** `0.402231`
- **R₉:** `0.439135`
- **potencjal_kappa:** `-0.089486`
- **masa_semantyczna:** `-0.210953`
- **rodzaj_karty:** `0.286192`


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
