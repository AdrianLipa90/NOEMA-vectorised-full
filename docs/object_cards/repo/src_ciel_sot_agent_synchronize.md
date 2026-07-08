# synchronize.py — src/ciel_sot_agent/synchronize.py

## Tożsamość
- **id_karty:** `REPO-SYNCHRONIZE-1A05`
- **ścieżka:** `src/ciel_sot_agent/synchronize.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `5.545`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/synchronize.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 5.545 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

## PhaseNav
- **operator:** `UNCERTAINTY`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.435049`
- **R₃:** `0.572136`
- **R₆:** `0.544042`
- **R₉:** `0.477522`
- **potencjal_kappa:** `0.159902`
- **masa_semantyczna:** `-0.053674`
- **rodzaj_karty:** `0.279085`


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
