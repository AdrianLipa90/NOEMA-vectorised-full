# test_ciel_geometry.py — tests/test_ciel_geometry.py

## Tożsamość
- **id_karty:** `REPO-TEST_CIEL_GEOMETRY-B5B6`
- **ścieżka:** `tests/test_ciel_geometry.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.300`
- **φ (phi):** `0.174`
- **masa_semantyczna:** `0.40`

## Kotwice
- `tests/test_ciel_geometry.py`

## Atraktor
- **system:** `sync_core`
- **główny_atraktor:** orbital_bridge_core → ent_Mr_Ciel_Apocalyptos

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.300 |
| φ | 0.174 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `sync_core`.

## PhaseNav
- **operator:** `COMPOSITION`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.528337`
- **R₃:** `0.492776`
- **R₆:** `0.696453`
- **R₉:** `0.565583`
- **potencjal_kappa:** `0.185923`
- **masa_semantyczna:** `-0.141173`
- **rodzaj_karty:** `0.274318`


## Rola
Tests for ciel_geometry — Foundation Pack P5 geometry engine.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem sync_core*
- **wyjście:** *wywnioskowane z folderu — podsystem sync_core*

## Zawartość
- **klasy:** —
- **funkcje:** `test_poincare_radius_center`, `test_poincare_radius_near_boundary`, `test_poincare_radius_monotone`, `test_sector_to_disk_inside_unit`, `test_entity_to_disk_inside_unit`, `test_entity_to_disk_high_coupling_is_central`, `test_poincare_distance_same_point`, `test_poincare_distance_positive`, `test_geodesic_arc_endpoints`, `test_geodesic_arc_all_inside_disk`, `test_load_sectors_nonempty`, `test_load_sectors_fields`, `test_load_couplings_nonempty`, `test_load_couplings_values_in_range`, `test_load_bridge_state_fields`, `test_build_layout_returns_nodes`, `test_build_layout_sectors_inside_disk`, `test_build_layout_edges`, `test_build_layout_with_entities`, `test_build_layout_metadata`, `test_build_layout_sector_centrality_is_not_inverted`, `test_build_layout_to_json`, `test_renderer_mpl_renders_to_figure`, `test_renderer_mpl_save`, `test_semantic_mass_table_nonempty`, `test_semantic_mass_values_positive`, `test_semantic_mass_sorted_desc`, `test_semantic_mass_kepler_rule`, `test_semantic_mass_entity_radius_inverts_coupling`, `test_subjective_time_nonempty`

## Opis
Tests for ciel_geometry — Foundation Pack P5 geometry engine.
