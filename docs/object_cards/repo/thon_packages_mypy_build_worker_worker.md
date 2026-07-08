# worker.py — .python_packages/mypy/build_worker/worker.py

## Tożsamość
- **id_karty:** `REPO-WORKER-3FCA`
- **ścieżka:** `.python_packages/mypy/build_worker/worker.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `4.902`
- **masa_semantyczna:** `0.40`

## Kotwice
- `.python_packages/mypy/build_worker/worker.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 4.902 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `CONSENT_REQUIRED`
- **odcisk_harmoniczny:** `LLHH`
- **R₁:** `0.458017`
- **R₃:** `0.48995`
- **R₆:** `0.569953`
- **R₉:** `0.575041`
- **potencjal_kappa:** `-0.194917`
- **masa_semantyczna:** `0.103166`
- **rodzaj_karty:** `0.278924`


## Rola
Mypy parallel build worker.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** ServerContext
- **funkcje:** `main`, `should_shutdown`, `serve`, `timed_send`, `load_states`, `setup_worker_manager`, `console_entry`, `flush_errors`

## Opis
Mypy parallel build worker.

The protocol of communication with the coordinator is as following:
* Read (pickled) build options from command line.
* Populate status file with pid and socket address.
* Receive build sources from coordinator.
* Initialize build manager with the sources, and send ack to coordinator.
* Receive build graph from coordinator, and ack it.
* Receive SCC structure from coor
