# test_orbital_shell.py — tests/test_orbital_shell.py

## Tożsamość
- **id_karty:** `REPO-TEST_ORBITAL_SHELL-592B`
- **ścieżka:** `tests/test_orbital_shell.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.300`
- **φ (phi):** `5.616`
- **masa_semantyczna:** `0.40`

## Kotwice
- `tests/test_orbital_shell.py`

## Atraktor
- **system:** `sync_core`
- **główny_atraktor:** orbital_bridge_core → ent_Mr_Ciel_Apocalyptos

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.300 |
| φ | 5.616 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `sync_core`.

## PhaseNav
- **operator:** `RISK`
- **odcisk_harmoniczny:** `HLLL`
- **R₁:** `0.594265`
- **R₃:** `0.468144`
- **R₆:** `0.457554`
- **R₉:** `0.414103`
- **potencjal_kappa:** `0.19508`
- **masa_semantyczna:** `-0.03873`
- **rodzaj_karty:** `0.279007`


## Rola
Tests for the orbital shell memory model (OrbitalRecord + OrbitalShellIndex).

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem sync_core*
- **wyjście:** *wywnioskowane z folderu — podsystem sync_core*

## Zawartość
- **klasy:** TestPhaseDistance, TestComputeEBind, TestShellFromEBind, TestOrbitalRecord, TestOrbitalShellIndex
- **funkcje:** `_load_orbital_shell`, `test_same_phase_is_zero`, `test_opposite_phases_is_pi`, `test_wrap_symmetry`, `test_negative_for_positive_r`, `test_singularity_clip`, `test_deeper_binding_at_smaller_r`, `test_unbound_maps_to_shell_8`, `test_small_r_maps_to_inner_shell`, `test_large_r_maps_to_outer_shell`, `test_monotone`, `test_from_phase_creates_valid_record`, `test_attractor_at_same_phase_gives_small_r`, `test_modal_hash_in_range`, `_make_idx`, `test_insert_returns_none_when_not_full`, `test_insert_evicts_loosest_when_full`, `test_get_by_id`, `test_get_missing_returns_none`, `test_retrieve_returns_at_most_n`, `test_retrieve_no_duplicates`, `test_shell_summary_counts_correct`, `test_shell_capacity_not_exceeded`, `test_pauli_exclusion_condenses_duplicate`, `test_retrieve_prefers_shell_matching_query_energy`

## Opis
Tests for the orbital shell memory model (OrbitalRecord + OrbitalShellIndex).
