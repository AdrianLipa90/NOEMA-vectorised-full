# ciel_subconscious_supervisor.py — scripts/ciel_subconscious_supervisor.py

## Tożsamość
- **id_karty:** `REPO-CIEL_SUBCONSCIOUS_SU-752C`
- **ścieżka:** `scripts/ciel_subconscious_supervisor.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 3 (RELATIONAL)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `2.583`
- **masa_semantyczna:** `0.65`

## Kotwice
- `scripts/ciel_subconscious_supervisor.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 3 (RELATIONAL) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 2.583 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.65 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 3, system `noema_registry`.

## PhaseNav
- **operator:** `FOLD`
- **odcisk_harmoniczny:** `LHHH`
- **R₁:** `0.351212`
- **R₃:** `0.661831`
- **R₆:** `0.649218`
- **R₉:** `0.522246`
- **potencjal_kappa:** `-0.135067`
- **masa_semantyczna:** `-0.137397`
- **rodzaj_karty:** `0.29302`


## Rola
Persistent supervisor for the CIEL subconscious backend.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_inline_backend_ok`, `get_status`, `run_supervisor`, `main`, `_stop`

## Opis
Persistent supervisor for the CIEL subconscious backend.

This wrapper keeps the real subconscious server alive. The actual inference
logic lives in `ciel_sot_agent.subconsciousness`; this file only ensures the
server is started and kept running in the background when SessionStart fires.
