# unified_memory.py — src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/monolith/unified_memory.py

## Tożsamość
- **id_karty:** `REPO-UNIFIED_MEMORY-F749`
- **ścieżka:** `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/monolith/unified_memory.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.150`
- **φ (phi):** `4.019`
- **masa_semantyczna:** `0.80`

## Kotwice
- `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/memory/monolith/unified_memory.py`

## Atraktor
- **system:** `ciel_omega_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via ciel_omega_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.150 |
| φ | 4.019 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.80 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `ciel_omega_core`.

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
CIEL-Memory Monolith (Pro Core) — single-file edition

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem ciel_omega_core*
- **wyjście:** *wywnioskowane z folderu — podsystem ciel_omega_core*

## Zawartość
- **klasy:** MemoriseD, DataVector, RuleHeuristicsEngine, TMPKernel, TSMWriterSQL, WPMWriterHDF5, BraidLedgerJSONL, UnifiedMemoryOrchestrator
- **funkcje:** `is_iso8601`, `validate_timestamp`, `clamp`, `spectral_categories`, `gamma_from_categories`, `capture_wave`, `_cli_status`, `_cli_run`, `_cli_verify`, `_cli_backup`, `_cli_export`, `_cli_wavesave`, `main`, `_load_json`, `ethical_gate`, `weight`, `first_analysis`, `second_analysis`, `process`, `_connect`, `_init_schema`, `save`, `attach_wpm_ref`, `read_meta`, `_detect_hdf5_support`, `_record_payload`, `_save_jsonl_fallback`, `save`, `save_with_wave`, `append`

## Opis
CIEL-Memory Monolith (Pro Core) — single-file edition
Author(s): Adrian Lipa, CIEL  |  Affiliation: Intention Lab (project patronage)
License: MIT (see LICENSE if split to repo)

Includes:
- TMP logic (A1/A2), RULE/HEUR with immutable/user/self + spectral multiplier γ in [-1,1] → [0,2]
- Durable: TSM (SQLite) + WPM (HDF5) with wave snapshots (amplitude/phase) + attrs
- Unified Orchestrator (captur
