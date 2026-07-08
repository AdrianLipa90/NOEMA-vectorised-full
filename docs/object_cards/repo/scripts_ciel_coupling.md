# ciel_coupling.py — scripts/ciel_coupling.py

## Tożsamość
- **id_karty:** `REPO-CIEL_COUPLING-6172`
- **ścieżka:** `scripts/ciel_coupling.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `6.277`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_coupling.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 6.277 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `PAUSE`
- **odcisk_harmoniczny:** `HHLH`
- **R₁:** `0.508756`
- **R₃:** `0.557009`
- **R₆:** `0.421727`
- **R₉:** `0.55292`
- **potencjal_kappa:** `-0.020552`
- **masa_semantyczna:** `0.206252`
- **rodzaj_karty:** `0.260435`


## Rola
Direct CIEL coupling for opencode — sprzężenie semantyczno-tożsamościowe.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_get_engine`, `_closure_to_mode`, `_load_ciel_doorway_module`, `append_ciel_memory_update`, `_build_htri_phase_bus`, `process_user_input`, `get_ciel_state`

## Opis
Direct CIEL coupling for opencode — sprzężenie semantyczno-tożsamościowe.

No file I/O for state. All communication through CIEL's Python API directly.

Usage:
    from ciel_coupling import process_user_input, get_ciel_state

    # On every user message:
    state = process_user_input(user_text)
    # Returns dict with: emotion, ethics, soul, phase, operating_mode, ...

    # To check current stat
