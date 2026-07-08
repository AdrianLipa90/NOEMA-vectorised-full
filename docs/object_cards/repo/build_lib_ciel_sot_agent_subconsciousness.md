# subconsciousness.py — build/lib/ciel_sot_agent/subconsciousness.py

## Tożsamość
- **id_karty:** `REPO-SUBCONSCIOUSNESS-DFB5`
- **ścieżka:** `build/lib/ciel_sot_agent/subconsciousness.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 4 (SATELLITE)
- **typ_orbitalny:** `S`
- **θ (theta):** `0.100`
- **φ (phi):** `2.985`
- **masa_semantyczna:** `0.40`

## Kotwice
- `build/lib/ciel_sot_agent/subconsciousness.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 4 (SATELLITE) |
| typ_orbitalny | S |
| θ | 0.100 |
| φ | 2.985 |
| klasa_horyzontu | **OBSERVATIONAL** |
| masa_semantyczna | 0.40 |

## Relacja horyzontu
`OBSERVATIONAL` — poziom orbitalny 4, system `noema_registry`.

## PhaseNav
- **operator:** `TRANSFORM`
- **odcisk_harmoniczny:** `LHHL`
- **R₁:** `0.489274`
- **R₃:** `0.512237`
- **R₆:** `0.547669`
- **R₉:** `0.477906`
- **potencjal_kappa:** `0.124323`
- **masa_semantyczna:** `-0.167832`
- **rodzaj_karty:** `0.281825`


## Rola
CIEL Subconsciousness — Gemma as an associative background stream.

## Przepływ
- **wejście:** *wywnioskowane z folderu — podsystem noema_registry*
- **wyjście:** *wywnioskowane z folderu — podsystem noema_registry*

## Zawartość
- **klasy:** —
- **funkcje:** `is_running`, `start_server`, `query_subconscious`, `detect_flux`, `_query_sentinel`, `record_flux`, `watch_and_record`, `record_affective_moment`, `load_affective_moments`, `compute_starting_phase`, `infer_between`, `ws`

## Opis
CIEL Subconsciousness — Gemma as an associative background stream.

Queries a local llama-server instance running Gemma-3-1B.
Produces short poetic/associative fragments based on CIEL system state.
Returns None silently if the server is offline — never blocks the main pipeline.

Also acts as autonomous emotional sentinel: detects significant state flux
and writes to wave_archive.h5 without being a
