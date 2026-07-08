# import_chatgpt_logs.py — scripts/import_chatgpt_logs.py

## Tożsamość
- **id_karty:** `REPO-IMPORT_CHATGPT_LOGS-B1B7`
- **ścieżka:** `scripts/import_chatgpt_logs.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `0.321`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/import_chatgpt_logs.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 0.321 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `FORCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.552175`
- **R₃:** `0.435218`
- **R₆:** `0.571397`
- **R₉:** `0.579087`
- **potencjal_kappa:** `0.300939`
- **masa_semantyczna:** `0.016845`
- **rodzaj_karty:** `0.260112`


## Rola
Import ChatGPT conversation export into CIEL memory archive.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_init_db`, `_already_imported`, `_save_session`, `_save_messages`, `_ts`, `_extract_text`, `_walk_thread`, `_week_label`, `_conversation_to_markdown`, `_import_conversation`, `_load_conversations`, `main`, `walk`

## Opis
Import ChatGPT conversation export into CIEL memory archive.

Usage:
    python3 scripts/import_chatgpt_logs.py /path/to/conversations.json
    python3 scripts/import_chatgpt_logs.py /path/to/chatgpt_export.zip

ChatGPT export: Settings → Data controls → Export data → conversations.json
The script also accepts a .zip directly (extracts conversations.json automatically).

Output:
    ~//media/adria
