# synchronize.py — build/bdist.linux-x86_64/wheel/ciel_sot_agent/synchronize.py

## Tożsamość
- **id_karty:** `REPO-SYNCHRONIZE-D5A5`
- **ścieżka:** `build/bdist.linux-x86_64/wheel/ciel_sot_agent/synchronize.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `1.104`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/bdist.linux-x86_64/wheel/ciel_sot_agent/synchronize.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 1.104 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

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
Synchronise entry point (v1) — builds and emits a sync report to stdout.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `_apply_thermal_noise`, `main`

## Opis
Synchronise entry point (v1) — builds and emits a sync report to stdout.

Reads the repository registry and coupling map from the ``integration/``
directory, calls ``repo_phase.build_sync_report``, and prints the result
as formatted JSON.  Invoked via the ``ciel-sot-sync`` console script.
