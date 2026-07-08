# opencode_raw_sessions_to_cielingo.py — scripts/opencode_raw_sessions_to_cielingo.py

## Tożsamość
- **id_karty:** `REPO-OPENCODE_RAW_SESSION-F1E1`
- **ścieżka:** `scripts/opencode_raw_sessions_to_cielingo.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `4.206`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/opencode_raw_sessions_to_cielingo.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 4.206 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `RETURN`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.642878`
- **R₃:** `0.503912`
- **R₆:** `0.555289`
- **R₉:** `0.707983`
- **potencjal_kappa:** `-0.270999`
- **masa_semantyczna:** `-0.074142`
- **rodzaj_karty:** `0.291714`


## Rola
Ingest OpenCode raw-session logs into CIELingo live raw memory.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_utc`, `_load_json`, `_write_json`, `_iter_session_dirs`, `_read_chat_records`, `_message_roles`, `_text_parts`, `_ensure_ingest_columns`, `_store_message`, `ingest_once`, `main`

## Opis
Ingest OpenCode raw-session logs into CIELingo live raw memory.
