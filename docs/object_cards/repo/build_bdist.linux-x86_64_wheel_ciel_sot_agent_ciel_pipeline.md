# ciel_pipeline.py — build/bdist.linux-x86_64/wheel/ciel_sot_agent/ciel_pipeline.py

## Tożsamość
- **id_karty:** `REPO-CIEL_PIPELINE-CB54`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_sot_agent/ciel_pipeline.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `3.443`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_sot_agent/ciel_pipeline.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 3.443 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ADDITION`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.662589`
- **R₃:** `0.614656`
- **R₆:** `0.542851`
- **R₉:** `0.417608`
- **potencjal_kappa:** `0.07638`
- **masa_semantyczna:** `0.206164`
- **rodzaj_karty:** `0.259027`


## Rola
CIEL pipeline adapter — routes orbital state through the CIEL/Ω engine.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_query_subconscious_socket`, `_query_subconscious`, `_weave_and_query_subconscious`, `_ensure_ciel_omega_on_path`, `_get_engine`, `warm_ciel_pipeline`, `_accumulated_identity_phase`, `_next_cycle_index`, `_orbital_state_to_context`, `_load_wpm_context`, `run_ciel_pipeline`, `_write_to_spreadsheet`, `_maybe_record_affective_moment`, `_persist_ciel_metrics`, `main`, `_preload`

## Opis
CIEL pipeline adapter — routes orbital state through the CIEL/Ω engine.

Provides ``run_ciel_pipeline`` which:
  1. Adds the canonical CIEL/Ω omega root to ``sys.path`` (idempotent).
  2. Reuses a session-local ``CielEngine`` singleton per root.
  3. Encodes the orbital state as a context string.
  4. Runs ``CielEngine.step()`` → returns the enriched result.

This is the bottom-to-top integration
