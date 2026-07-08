# noema_voice_daemon.py — scripts/noema_voice_daemon.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_VOICE_DAEMON-AF27`
- **ścieżka:** `scripts/noema_voice_daemon.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `5.251`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_voice_daemon.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 5.251 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_POSSIBILITY`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.565748`
- **R₃:** `0.628966`
- **R₆:** `0.492583`
- **R₉:** `0.589778`
- **potencjal_kappa:** `0.024081`
- **masa_semantyczna:** `-0.294904`
- **rodzaj_karty:** `0.302592`


## Rola
noema_voice_daemon.py  —  HTTP daemon na porcie 18521

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** VoiceHandler
- **funkcje:** `_mic_mute`, `_say`, `_voice_hb_loop`, `main`, `log_message`, `_respond_json`, `do_GET`, `do_POST`, `_read_json_body`, `_handle_say`, `_handle_chat`

## Opis
noema_voice_daemon.py  —  HTTP daemon na porcie 18521

Serwuje odpowiedzi generowane lokalnie przez Voice (ciel_geometry.voice),
bez LLM, bez internetu. Endpoint /v1/chat/completions (zgodny z OpenAI).

Endpointy:
  GET  /health          → {"service": "noema_voice", "status": "running", "mode": "..."}
  POST /v1/chat/completions  → odpowiedź Voice jako OpenAI-compatible response

Usage:
  .venv/bi
