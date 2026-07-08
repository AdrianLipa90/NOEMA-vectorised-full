# noema_imaginal_server.py — scripts/noema_imaginal_server.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_IMAGINAL_SERVE-129F`
- **ścieżka:** `scripts/noema_imaginal_server.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `3.678`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_imaginal_server.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 3.678 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_PERMISSION`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.453718`
- **R₃:** `0.541785`
- **R₆:** `0.466054`
- **R₉:** `0.529069`
- **potencjal_kappa:** `0.025212`
- **masa_semantyczna:** `0.161862`
- **rodzaj_karty:** `0.285369`


## Rola
NOEMA Imaginal Server — daemony jako operatory 24D na imaginal surface.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_set_daemon_omegas`, `_read_daemon_phases`, `_get_coherence`, `_load_orbital_state`, `main`, `_stop`

## Opis
NOEMA Imaginal Server — daemony jako operatory 24D na imaginal surface.

Używa resonance_bridge.dual_surface_step() jako silnika.
Każdy daemon NOEMY to osobny oscylator na imaginal surface z własną ω.
Real surface = Poincaré section (zamrożony odczyt).

Usage:
    python3 scripts/noema_imaginal_server.py [--interval SEC]
