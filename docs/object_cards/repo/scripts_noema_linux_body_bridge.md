# noema_linux_body_bridge.py — scripts/noema_linux_body_bridge.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_LINUX_BODY_BRI-410A`
- **ścieżka:** `scripts/noema_linux_body_bridge.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `6.199`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_linux_body_bridge.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 6.199 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `DIFFERENCE`
- **odcisk_harmoniczny:** `HHHL`
- **R₁:** `0.563622`
- **R₃:** `0.51399`
- **R₆:** `0.516024`
- **R₉:** `0.447233`
- **potencjal_kappa:** `-0.196591`
- **masa_semantyczna:** `-0.06476`
- **rodzaj_karty:** `0.313562`


## Rola
NOEMA Linux Body Bridge — PhaseEncoder → sensor_raw → kuramoto daemon.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_read_json`, `build_linux_text`, `build_sensor_raw`, `write_sensor_raw`, `daemon_loop`, `main`, `_stop`

## Opis
NOEMA Linux Body Bridge — PhaseEncoder → sensor_raw → kuramoto daemon.

Używa CIELingo PhaseEncoder do mapowania stanu Linux na 36D konfigurację
fazową przez fast_encode_text(). Daemon czyta sensor_raw co cykl (0.2s)
i blenduje 15% do phi.

Usage:
    python3 scripts/noema_linux_body_bridge.py            # oneshot
    python3 scripts/noema_linux_body_bridge.py --daemon   # co 2s
