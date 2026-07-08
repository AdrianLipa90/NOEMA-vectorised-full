# analog_bus.py — build/bdist.linux-x86_64/wheel/ciel_geometry/analog_bus.py

## Tożsamość
- **id_karty:** `REPO-ANALOG_BUS-2AA0`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_geometry/analog_bus.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `6.109`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_geometry/analog_bus.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 6.109 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `ORDER`
- **odcisk_harmoniczny:** `LHLH`
- **R₁:** `0.408132`
- **R₃:** `0.527143`
- **R₆:** `0.447287`
- **R₉:** `0.516074`
- **potencjal_kappa:** `0.213299`
- **masa_semantyczna:** `0.199346`
- **rodzaj_karty:** `0.279908`


## Rola
NOEMA analog bus — pseudo-analog shared memory for dual-node PhaseNav.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_ensure_dir`, `_create_mmap`, `_open_mmap`, `ensure_bus`, `open_bus`, `blend_phi`

## Opis
NOEMA analog bus — pseudo-analog shared memory for dual-node PhaseNav.

Architecture:
  Two PhaseNav nodes (hot/cold) write independent phi vectors to mmap.
  A blender reads both, weights by temperature, and injects into surface.

Files under /dev/shm/ciel_noema/analog/:
  phi_hot     float64[36]  — hot node phase (fast, wide exploration)
  phi_cold    float64[36]  — cold node phase (slow, focuse
