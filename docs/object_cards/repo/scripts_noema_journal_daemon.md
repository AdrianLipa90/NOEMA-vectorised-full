# noema_journal_daemon.py — scripts/noema_journal_daemon.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_JOURNAL_DAEMON-53FA`
- **ścieżka:** `scripts/noema_journal_daemon.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.428`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_journal_daemon.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.428 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `UNRUH_DRIVE`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.695214`
- **R₃:** `0.356299`
- **R₆:** `0.471302`
- **R₉:** `0.535169`
- **potencjal_kappa:** `0.138014`
- **masa_semantyczna:** `0.204514`
- **rodzaj_karty:** `0.244249`


## Rola
Journal daemon — journalctl pipe → NOEMA surface.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `log`, `_severity_weight`, `_init_dirs`, `_write_surface`, `process_line`, `journal_feed`, `signal_handler`, `main`

## Opis
Journal daemon — journalctl pipe → NOEMA surface.

Czyta live log systemu przez `journalctl -f -o json`, parsuje,
mapuje severity → emocje, i zapisuje na powierzchnię.

Surface output (/dev/shm/ciel_noema/journal/):
  recent.jsonl  — ostatnie 64 wiadomości
  stats.json    — rate, severity distribution, top units
  alert.json    — najwyższy priorytet w oknie

Integracja:
  - severity → flavor/emoti
