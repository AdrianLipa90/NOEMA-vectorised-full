# htri_daemon.py — src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/htri/htri_daemon.py

## Tożsamość
- **id_karty:** `REPO-HTRI_DAEMON-1F4E`
- **ścieżka:** `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/htri/htri_daemon.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 2 (STRUCTURE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.150`
- **φ (phi):** `3.589`
- **masa_semantyczna:** `0.80`

## Kotwice
- `src/CIEL_OMEGA_COMPLETE_SYSTEM/ciel_omega/htri/htri_daemon.py`

## Atraktor
- **system:** `ciel_omega_core`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via ciel_omega_core

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 2 (STRUCTURE) |
| typ_orbitalny | S |
| θ | 0.150 |
| φ | 3.589 |
| klasa_horyzontu | **POROUS** |
| masa_semantyczna | 0.80 |

## Relacja horyzontu
`POROUS` — poziom orbitalny 2, system `ciel_omega_core`.

## PhaseNav
- **operator:** `COMPOSITION`
- **odcisk_harmoniczny:** `HLHH`
- **R₁:** `0.528337`
- **R₃:** `0.492776`
- **R₆:** `0.696453`
- **R₉:** `0.565583`
- **potencjal_kappa:** `0.185923`
- **masa_semantyczna:** `-0.141173`
- **rodzaj_karty:** `0.274318`


## Rola
HTRI Daemon — trwały background process na i7-8750H + GTX 1050 Ti.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem ciel_omega_core*
- **wyjście:** *wywnioskowane z folderu — podsystem ciel_omega_core*

## Zawartość
- **klasy:** —
- **funkcje:** `_handle_signal`, `_write_state`, `run_daemon`, `read_state`, `is_running`

## Opis
HTRI Daemon — trwały background process na i7-8750H + GTX 1050 Ti.

Działa non-stop, zapisuje metryki do ~/.claude/ciel_state.db co cycle_interval sekund.
Uruchamiany przez systemd lub autostart.

Usage:
    python3 htri_daemon.py          # foreground (do testów)
    python3 htri_daemon.py --daemon # background
