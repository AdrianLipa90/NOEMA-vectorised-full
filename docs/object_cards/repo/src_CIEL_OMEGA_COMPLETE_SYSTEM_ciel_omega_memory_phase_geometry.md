# phase_geometry.py — src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/phase_geometry.py

## Tożsamość
- **id_karty:** `REPO-PHASE_GEOMETRY-47AE`
- **ścieżka:** `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/phase_geometry.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.150`
- **φ (phi):** `1.639`
- **masa_semantyczna:** `0.80`

## Kotwice
- `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/phase_geometry.py`

## Atraktor
- **system:** `ciel_omega_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via ciel_omega_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.150 |
| φ | 1.639 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.80 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `ciel_omega_core`.

## PhaseNav
- **operator:** `ASSERTION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.563342`
- **R₃:** `0.601856`
- **R₆:** `0.54039`
- **R₉:** `0.584219`
- **potencjal_kappa:** `-0.098441`
- **masa_semantyczna:** `0.347732`
- **rodzaj_karty:** `0.261593`


## Rola
CIEL Phase Geometry — CP², Poincaré disk, hypertorus.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem ciel_omega_core*
- **wyjście:** *wywnioskowane z folderu — podsystem ciel_omega_core*

## Zawartość
- **klasy:** CP2State, PoincareDisk, HomotopyClass, HypertorusLattice
- **funkcje:** `cp2_retrieval_weight`, `encoder_result_to_cp2`, `db_row_to_cp2`, `_calibrated_weights`, `from_channels`, `from_phase`, `fubini_study`, `dominant_phase`, `mean_phase`, `channel_coherence`, `to_poincare`, `to_poincare_full`, `mobius`, `poincare_distance`, `in_ball`, `distance`, `retrieval_weight`, `from_winding`, `same_class`, `lattice_distance`, `euler_defect`, `homotopy_affinity`, `from_db_entry`, `euler_violation_from_classes`, `_clamp`

## Opis
CIEL Phase Geometry — CP², Poincaré disk, hypertorus.

Replaces scalar S¹ phase arithmetic with full geometric state space:

  CP² — complex projective plane as 3-channel encoder state space
       (φ_semantic, φ_htri, φ_nonlocal) → [z₀:z₁:z₂] ∈ CP²
       Distance: Fubini-Study metric → geodesic arcs, not flat angles

  Poincaré disk D² — inference volume inside CP²
       Project CP² → D² via st
