# noema_surface_refresh.py — scripts/noema_surface_refresh.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_SURFACE_REFRES-8804`
- **ścieżka:** `scripts/noema_surface_refresh.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `6.214`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_surface_refresh.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 6.214 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `MODAL_OBLIGATION`
- **odcisk_harmoniczny:** `HHHH`
- **R₁:** `0.59271`
- **R₃:** `0.552945`
- **R₆:** `0.534582`
- **R₉:** `0.582078`
- **potencjal_kappa:** `0.23834`
- **masa_semantyczna:** `-0.091456`
- **rodzaj_karty:** `0.276031`


## Rola
noema_surface_refresh.py — Automatyczne odświeżanie mmap dla KAŻDEGO systemu i subsystemu.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `read_existing_system_map`, `run_script`, `read_surface_values`, `refresh_all`

## Opis
noema_surface_refresh.py — Automatyczne odświeżanie mmap dla KAŻDEGO systemu i subsystemu.

Uruchamiany co 15 minut przez systemd timer.
Czyta system_map_v2.json i aktualizuje /dev/shm/ciel_noema/system_map.
Dla każdego daemona/skryptu: uruchamia refresh jesli runtime_file istnieje.
