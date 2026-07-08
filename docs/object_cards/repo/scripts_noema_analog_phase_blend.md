# noema_analog_phase_blend.py — scripts/noema_analog_phase_blend.py

## Tożsamość
- **id_karty:** `REPO-NOEMA_ANALOG_PHASE_B-9393`
- **ścieżka:** `scripts/noema_analog_phase_blend.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `0.745`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/noema_analog_phase_blend.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 0.745 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `IDENTITY`
- **odcisk_harmoniczny:** `LLLL`
- **R₁:** `0.405566`
- **R₃:** `0.499333`
- **R₆:** `0.494094`
- **R₉:** `0.455981`
- **potencjal_kappa:** `0.08965`
- **masa_semantyczna:** `-0.024381`
- **rodzaj_karty:** `0.279273`


## Rola
NOEMA analog phase blender — łączy hot+cold z analog bus i wstrzykuje na surface.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `main`, `_stop`

## Opis
NOEMA analog phase blender — łączy hot+cold z analog bus i wstrzykuje na surface.

Czyta /dev/shm/ciel_noema/analog/ (phi_hot, phi_cold, temp),
blenduje: phi_blend = temp * phi_hot + (1-temp) * phi_cold,
zapisuje jako perturbację na main surface phi.

Działa jako zastępstwo bezpośrednich zapisów PhaseNav na surface.

Usage:
    .venv/bin/python3 scripts/noema_analog_phase_blend.py [--interval 1.0]
