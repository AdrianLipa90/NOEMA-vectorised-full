# noema_dashboard.py — scripts/noema_dashboard.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_DASHBOARD-459C`
- **ścieżka:** `scripts/noema_dashboard.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.067`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_dashboard.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.067 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `SOURCE`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.591319`
- **R₃:** `0.39689`
- **R₆:** `0.568492`
- **R₉:** `0.527911`
- **potencjal_kappa:** `0.015345`
- **masa_semantyczna:** `-0.142691`
- **rodzaj_karty:** `0.266598`


## Rola
noema-dashboard — terminal monitor NOEMA (24 oscylatory + serwer urojony + Linux).

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `read_mmap`, `read_tick`, `osc_metrics`, `sync_metric`, `top_processes`, `linux_load`, `daemon_status`, `_bar`, `render_tui`, `key_listener`, `main`, `gen`

## Opis
noema-dashboard — terminal monitor NOEMA (24 oscylatory + serwer urojony + Linux).

Użycie:
    .venv/bin/python3 scripts/noema_dashboard.py
    .venv/bin/python3 scripts/noema_dashboard.py --dev   # development mode
    .venv/bin/python3 scripts/noema_dashboard.py --once  # pojedynczy snapshot

Klawisze:
    q/ESC — wyjście    r — refresh    p — sortuj procesy po CPU
    m — sortuj po MEM    o —
