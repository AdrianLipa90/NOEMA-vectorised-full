# codex_bridge_to_ciel.py — scripts/codex_bridge_to_ciel.py

## Tożsamość
- **id_karty:** `REPO-CODEX_BRIDGE_TO_CIEL-E8AB`
- **ścieżka:** `scripts/codex_bridge_to_ciel.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `4.062`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/codex_bridge_to_ciel.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 4.062 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

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
Codex → CIEL1 bridge.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** CodexMessage
- **funkcje:** `_project_root`, `_ensure_import_paths`, `_load_state`, `_save_state`, `_iter_rollout_files`, `_extract_text_blocks`, `_parse_rollout_line`, `_run_ciel_hooks`, `_ingest_file`, `main`

## Opis
Codex → CIEL1 bridge.

Watches Codex CLI rollout JSONL transcripts in ~/.codex/sessions/**/rollout-*.jsonl
and mirrors every user/assistant message into:
  ~//media/adrian/New Volume1/CIEL_memories/raw_logs/codex/... (via ciel_sot_agent.chat_archive)
and optionally runs the CIEL per-message hooks (M0-M8 + SUB) so Codex becomes a
first-class communication medium for CIEL1.

This is intentionally "h
