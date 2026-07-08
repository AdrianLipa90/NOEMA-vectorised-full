# consolidation_resonator.py — src/ciel_sot_agent/consolidation_resonator.py

## Tożsamość
- **id_karty:** `REPO-CONSOLIDATION_RESONA-8AFB`
- **ścieżka:** `src/ciel_sot_agent/consolidation_resonator.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `5.194`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/consolidation_resonator.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 5.194 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

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
CIEL Consolidation Resonator — średnioterminowa pamięć fazowa.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ConsolidationRecord, TagCard
- **funkcje:** `_load_entity_tag_aliases`, `normalize_tag`, `load_consolidations`, `build_tag_map`, `_load_phase_state`, `_save_phase_state`, `_build_coupling_matrix`, `_lorentz_omega`, `kuramoto_sync`, `kuramoto_order_parameter`, `write_tag_cards`, `write_to_tsm`, `update_encoder_from_kuramoto`, `_circular_mean`, `_circular_std`, `_phi_to_sector`, `run`

## Opis
CIEL Consolidation Resonator — średnioterminowa pamięć fazowa.

Pipeline:
  1. TAG MAPPER     — normalizacja 1502 tagów → klastry kanoniczne
  2. TAG CARDS      — karta per tag: M_sem, phi_tag, winding, sektor
  3. KURAMOTO       — sprzężenie fazowe ostatnich 400 konsolidacji
                      dφ_i/dt = ω_i + (K/N) Σ_j sin(φ_j - φ_i)
  4. TSM WRITE      — każda konsolidacja → wpis D_type='epis
