# ciel_agent_backend.py — scripts/ciel_agent_backend.py

## Tożsamość
- **id_karty:** `REPO-CIEL_AGENT_BACKEND-E33B`
- **ścieżka:** `scripts/ciel_agent_backend.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `4.776`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_agent_backend.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 4.776 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_PERMISSION`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.453718`
- **R₃:** `0.541785`
- **R₆:** `0.466054`
- **R₉:** `0.529069`
- **potencjal_kappa:** `0.025212`
- **masa_semantyczna:** `0.161862`
- **rodzaj_karty:** `0.285369`


## Rola
ciel_agent_backend — zero-model HTTP agent for memory consolidation.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** AgentHandler
- **funkcje:** `_tokenize`, `_ngrams`, `_extract_content`, `extract_themes`, `detect_affect`, `extract_anchors`, `extract_essence`, `generate_hunch`, `process_content`, `run_once`, `_agent_hb_loop`, `run_daemon`, `info_density`, `do_GET`, `do_POST`, `_handle_chat`, `_handle_query`, `_respond`, `log_message`, `_stop`

## Opis
ciel_agent_backend — zero-model HTTP agent for memory consolidation.

Replaces llama-server/GGUF with keyword+pattern extraction.
OpenAI-compatible /v1/chat/completions on port 18520.

Usage:
  python3 ciel_agent_backend.py            # daemon (default port 18520)
  python3 ciel_agent_backend.py --port 18521
  python3 ciel_agent_backend.py --once "file content here"
