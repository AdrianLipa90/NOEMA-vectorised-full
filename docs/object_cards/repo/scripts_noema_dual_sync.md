# noema_dual_sync.py — scripts/noema_dual_sync.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_DUAL_SYNC-18D3`
- **ścieżka:** `scripts/noema_dual_sync.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `3.087`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_dual_sync.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 3.087 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

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
NOEMA Dual-Surface Sync Monitor — continuous real↔imaginal bridge.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_sync_phi`, `_sync_g_and_omega`, `_bind_phase_memory`, `_bind_fields`, `sync_once`, `daemon_loop`, `status`, `_stop`

## Opis
NOEMA Dual-Surface Sync Monitor — continuous real↔imaginal bridge.

Pushes real surface state (phi, g, omega) to imaginal surface,
keeping the dual surfaces co-evolving. Logs sync metrics.

Usage:
    .venv/bin/python3 scripts/noema_dual_sync.py              # single sync step
    .venv/bin/python3 scripts/noema_dual_sync.py --loop        # continuous daemon
    .venv/bin/python3 scripts/noema_dua
