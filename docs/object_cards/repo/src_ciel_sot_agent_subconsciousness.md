# subconsciousness.py — src/ciel_sot_agent/subconsciousness.py

## Tożsamość
- **id_karty:** `REPO-SUBCONSCIOUSNESS-76CE`
- **ścieżka:** `src/ciel_sot_agent/subconsciousness.py`
- **ostatni_indeks:** `2026-07-06`
- **poziom_orbitalny:** 1 (CORE)
- **typ_orbitalny:** `F`
- **θ (theta):** `0.100`
- **φ (phi):** `5.937`
- **masa_semantyczna:** `0.90`

## Kotwice
- `src/ciel_sot_agent/subconsciousness.py`

## Atraktor
- **system:** `noema_registry`
- **główny_atraktor:** ent_Mr_Ciel_Apocalyptos (θ=0.0) via noema_registry

## Mechanika orbitalna
| parametr | wartość |
|---|---|
| poziom_orbitalny | 1 (CORE) |
| typ_orbitalny | F |
| θ | 0.100 |
| φ | 5.937 |
| klasa_horyzontu | **TRANSMISSIVE** |
| masa_semantyczna | 0.90 |

## Relacja horyzontu
`TRANSMISSIVE` — poziom orbitalny 1, system `noema_registry`.

## PhaseNav
- **operator:** `UNRUH_DRIVE`
- **odcisk_harmoniczny:** `HLLH`
- **R₁:** `0.695214`
- **R₃:** `0.356299`
- **R₆:** `0.471302`
- **R₉:** `0.535169`
- **potencjal_kappa:** `0.138014`
- **masa_semantyczna:** `0.204514`
- **rodzaj_karty:** `0.244249`


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
