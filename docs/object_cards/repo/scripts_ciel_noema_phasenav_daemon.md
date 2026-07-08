# ciel_noema_phasenav_daemon.py — scripts/ciel_noema_phasenav_daemon.py

## Tożsamość
- **id_karty:** `REPO-CIEL_NOEMA_PHASENAV_-AD9A`
- **ścieżka:** `scripts/ciel_noema_phasenav_daemon.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `1.104`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_noema_phasenav_daemon.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 1.104 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `SIMULATION_BOUNDARY`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.575665`
- **R₃:** `0.306554`
- **R₆:** `0.381064`
- **R₉:** `0.528951`
- **potencjal_kappa:** `-0.226686`
- **masa_semantyczna:** `-0.021063`
- **rodzaj_karty:** `0.269599`


## Rola
PhaseNav daemon — dual-node analog bus.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_load_zip_index`, `_load_library_index`, `_vector_phases`, `_library_phases`, `_load_skill_index`, `_skill_phases`, `_operator_phases`, `_concept_phases`, `main`

## Opis
PhaseNav daemon — dual-node analog bus.

Modes:
  --node hot   (fast: 1s interval, 0.8 strength, wide exploration)
  --node cold  (slow: 30s interval, 0.2 strength, focused on system operator)

Both write to /dev/shm/ciel_noema/analog/ (phi_hot or phi_cold + temp).
A separate blender daemon reads the bus and injects into surface phi.

Usage:
    python scripts/ciel_noema_phasenav_daemon.py --node
