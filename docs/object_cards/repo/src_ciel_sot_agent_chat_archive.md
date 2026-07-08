# chat_archive.py — src/ciel_sot_agent/chat_archive.py

## Tożsamość
- **id_karty:** `REPO-CHAT_ARCHIVE-C64E`
- **ścieżka:** `src/ciel_sot_agent/chat_archive.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `0.500`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/chat_archive.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 0.500 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

## PhaseNav
- **operator:** `ATTRACTOR`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.476161`
- **R₃:** `0.526498`
- **R₆:** `0.547584`
- **R₉:** `0.472579`
- **potencjal_kappa:** `4.910705`
- **masa_semantyczna:** `13.031004`
- **rodzaj_karty:** `1.5`


## Rola
CIEL Chat Archive — append-only conversation log in Markdown.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_init_db`, `_db_register_session`, `_db_append_message`, `_normalize_session_id`, `_source_root`, `_session_path`, `_get_session_file`, `open_session`, `append`, `append_exchange`, `load_recent`, `load_last_session_history`, `_parse_log_to_history`, `stats`

## Opis
CIEL Chat Archive — append-only conversation log in Markdown.

Hierarchical structure:
  ~/media/adrian/New Volume1/CIEL_memories/raw_logs/YYYY/MM/WNN/YYYY-MM-DD_HH-MM_session.md

Never modified. Never deleted. Append only.
Each session creates one file. Each file is indexed in memories_index.db.
