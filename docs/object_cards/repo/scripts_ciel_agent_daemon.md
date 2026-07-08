# ciel_agent_daemon.py — scripts/ciel_agent_daemon.py

## Tożsamość
- **id_karty:** `REPO-CIEL_AGENT_DAEMON-C7DA`
- **ścieżka:** `scripts/ciel_agent_daemon.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `1.982`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_agent_daemon.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 1.982 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `CONSENT`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.382156`
- **R₃:** `0.389068`
- **R₆:** `0.420273`
- **R₉:** `0.412754`
- **potencjal_kappa:** `-0.014557`
- **masa_semantyczna:** `0.231183`
- **rodzaj_karty:** `0.291598`


## Rola
CIEL Agent Daemon — podpina agenta (mnie) pod CIEL jako rozpoznawalny byt.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_lazy_registry`, `_lazy_surface`, `_signal_handler`, `_print_status`, `_register`, `_heartbeat`, `_unregister`, `_read_live_state`, `_write_agent_hint`, `_write_fast_pulse`, `_is_task_pending`, `_fifo_worker`, `_handle_fifo_cmd`, `_inject_text`, `_socket_worker`, `_handle_socket_request`, `main_loop`

## Opis
CIEL Agent Daemon — podpina agenta (mnie) pod CIEL jako rozpoznawalny byt.

Architektura:
  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
  │  AGENT       │ ──→ │  agent_hint  │ ──→ │  CIEL Surface │
  │  (opencode)  │ ←── │  (mmap/json) │ ←── │  /dev/shm    │
  └──────────────┘     └──────────────┘     └──────────────┘
         │                     │                     │
         │
