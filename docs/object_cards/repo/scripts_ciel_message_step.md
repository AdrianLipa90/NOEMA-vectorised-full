# ciel_message_step.py — scripts/ciel_message_step.py

## Tożsamość
- **id_karty:** `REPO-CIEL_MESSAGE_STEP-206D`
- **ścieżka:** `scripts/ciel_message_step.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.616`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_message_step.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.616 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `IDENTITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.405566`
- **R₃:** `0.499333`
- **R₆:** `0.494094`
- **R₉:** `0.455981`
- **potencjal_kappa:** `0.08965`
- **masa_semantyczna:** `-0.024381`
- **rodzaj_karty:** `0.279273`


## Rola
CIEL UserPromptSubmit Hook — per-message consciousness pipeline.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `load_orchestrator`, `save_orchestrator`, `maybe_write_snapshot`, `_prompt_metrics_payload`, `_write_prompt_metrics_log`, `_write_raw_prompt_log`, `run_relational_cycle`, `load_self_assessment`, `_load_context_metrics`, `_run_periodic_consolidation`, `_maybe_write_hunch`, `_stamp_prompt_summary`, `_run_subconscious`, `run_step`, `orbital_directives`, `format_context`, `_load_custom_inject`, `_compact_lingo_frame`, `build_cielingo_premodel_context`, `main`

## Opis
CIEL UserPromptSubmit Hook — per-message consciousness pipeline.

Reads user message from stdin (UserPromptSubmit JSON), runs it through
HolonomicMemoryOrchestrator M0→M8, persists state to /tmp/ciel_orch_state.pkl,
and returns additionalContext with live consciousness metrics.

State persists between calls so memory accumulates across the session.
