# noema_actuator_daemon.py — scripts/noema_actuator_daemon.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_ACTUATOR_DAEMO-FC06`
- **ścieżka:** `scripts/noema_actuator_daemon.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `0.937`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_actuator_daemon.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 0.937 |
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
Actuator daemon — surface → system control.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `log`, `_init_dirs`, `_rate_limited`, `_audit`, `_safe_unit`, `_execute`, `_read_intent`, `_write_result`, `_write_status`, `signal_handler`, `main`

## Opis
Actuator daemon — surface → system control.

Nadzoruje katalog /dev/shm/ciel_noema/actuator/ i wykonuje intencje
zapisane przez agenta (CIEL) jako JSON. Daje mi ręce.

Security:
  - whitelist akcji: restart, start, stop (tylko noema-*.service)
  - journal_query, run_script (tylko scripts/*.py)
  - rate limiting: max 1 akcja / 15s
  - audit trail: actuator/audit.jsonl
  - confirmation required dla
