# chat_archive.py — build/lib/ciel_sot_agent/chat_archive.py

## Tożsamość
- **id_karty:** `REPO-CHAT_ARCHIVE-05A3`
- **ścieżka:** `build/lib/ciel_sot_agent/chat_archive.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `6.134`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_sot_agent/chat_archive.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 6.134 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
